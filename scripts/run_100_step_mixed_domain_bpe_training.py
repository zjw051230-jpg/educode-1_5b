from __future__ import annotations

import json
import math
import sys
import time
from datetime import datetime
from pathlib import Path

import torch
from tokenizers import Tokenizer

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = PROJECT_ROOT / "src"
CONFIG_PATH = PROJECT_ROOT / "configs" / "windows" / "bpe_mixed_domain_8k_smoke.json"
TRAIN_SPLIT_PATH = PROJECT_ROOT / "data" / "real_corpus" / "splits" / "mixed_domain_external.train.jsonl"
VAL_SPLIT_PATH = PROJECT_ROOT / "data" / "real_corpus" / "splits" / "mixed_domain_external.val.jsonl"
MAX_STEPS = 100
EVAL_INTERVAL = 10
EXPECTED_SOURCE_CATEGORIES = {"synthetic_examples", "external_general_text"}

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from educode.checkpoint import compare_model_parameters, load_checkpoint, save_checkpoint
from educode.config_loader import load_json_config
from educode.config_validator import validate_config
from educode.losses import next_token_cross_entropy
from educode.run_logging import build_summary_markdown, write_json, write_metrics_record, write_text
from educode.run_setup import (
    collect_basic_environment,
    create_run_directory,
    get_git_branch,
    get_git_commit,
    make_run_id,
    snapshot_config,
    write_run_metadata,
)
from educode.sequence_dataset import batch_samples, make_next_token_samples
from educode.tiny_model import TinyDecoderOnlyTransformer, model_config_from_dict


def load_split_records(split_path: Path) -> tuple[list[str], dict[str, int]]:
    texts: list[str] = []
    source_counts: dict[str, int] = {}
    with split_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            record = json.loads(line)
            text = record.get("text")
            if not isinstance(text, str) or not text.strip():
                continue
            texts.append(text)
            source_category = str(record.get("source_category", "unknown"))
            source_counts[source_category] = source_counts.get(source_category, 0) + 1
    return texts, source_counts


def validate_source_counts(split_name: str, source_counts: dict[str, int]) -> None:
    observed_source_categories = set(source_counts)
    if observed_source_categories != EXPECTED_SOURCE_CATEGORIES:
        raise ValueError(
            f"{split_name} split expected source categories {sorted(EXPECTED_SOURCE_CATEGORIES)} "
            f"but found {sorted(observed_source_categories)}"
        )

    external_count = source_counts.get("external_general_text", 0)
    synthetic_count = source_counts.get("synthetic_examples", 0)
    if external_count <= 0:
        raise ValueError(f"{split_name} split is missing external_general_text records")
    if synthetic_count <= 0:
        raise ValueError(f"{split_name} split is missing synthetic_examples records")
    if external_count >= synthetic_count:
        raise ValueError(
            f"{split_name} split violates supplement-only rule: "
            f"external_general_text={external_count}, synthetic_examples={synthetic_count}"
        )


def build_batches(
    tokenizer: Tokenizer,
    texts: list[str],
    sequence_length: int,
    batch_size: int,
) -> tuple[list[tuple[list[list[int]], list[list[int]]]], int]:
    combined_text = "\n\n".join(texts)
    token_ids = tokenizer.encode(combined_text).ids
    if len(token_ids) < 2:
        raise ValueError("not enough token ids for next-token samples")

    samples = make_next_token_samples(token_ids, sequence_length)
    batches = batch_samples(samples, batch_size)
    if not batches:
        raise ValueError("no full batch could be created")

    return batches, len(token_ids)


def compute_grad_norm(parameters) -> float | None:
    total = 0.0
    found_grad = False
    for parameter in parameters:
        if parameter.grad is None:
            continue
        grad_norm = float(parameter.grad.detach().norm(2).item())
        total += grad_norm * grad_norm
        found_grad = True
    if not found_grad:
        return None
    return math.sqrt(total)


def gradients_all_finite(parameters) -> bool:
    found_grad = False
    for parameter in parameters:
        if parameter.grad is None:
            continue
        found_grad = True
        if not bool(torch.isfinite(parameter.grad).all().item()):
            return False
    return found_grad


def evaluate_loss(
    model: TinyDecoderOnlyTransformer,
    batch_x: list[list[int]],
    batch_y: list[list[int]],
    device: torch.device,
) -> float:
    input_ids = torch.tensor(batch_x, dtype=torch.long, device=device)
    target_ids = torch.tensor(batch_y, dtype=torch.long, device=device)

    model.eval()
    with torch.no_grad():
        logits = model(input_ids)
        loss = next_token_cross_entropy(logits, target_ids)

    if not bool(torch.isfinite(loss).item()):
        raise ValueError("validation loss is not finite")
    return float(loss.item())


def main() -> int:
    config = load_json_config(CONFIG_PATH)
    errors = validate_config(config, repo_root=PROJECT_ROOT)
    if errors:
        print("validation: failed")
        for error in errors:
            print(f"- {error}")
        return 1

    seed = int(config.get("run", {}).get("seed", 42))
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

    tokenizer_path = PROJECT_ROOT / config["tokenizer"]["path"]
    tokenizer = Tokenizer.from_file(str(tokenizer_path))
    if tokenizer.get_vocab_size() != 8192:
        print(f"failure: expected tokenizer vocab size 8192 but found {tokenizer.get_vocab_size()}")
        return 1

    train_texts, train_source_counts = load_split_records(TRAIN_SPLIT_PATH)
    val_texts, val_source_counts = load_split_records(VAL_SPLIT_PATH)
    if not train_texts:
        print("failure: no train texts found")
        return 1
    if not val_texts:
        print("failure: no val texts found")
        return 1

    try:
        validate_source_counts("train", train_source_counts)
        validate_source_counts("val", val_source_counts)
    except ValueError as error:
        print(f"failure: {error}")
        return 1

    configured_sequence_length = config["training"].get("sequence_length", config["model"]["context_length"])
    sequence_length = min(config["model"]["context_length"], configured_sequence_length)
    batch_size = min(config["training"].get("batch_size", 1), 4)

    try:
        train_batches, train_tokens = build_batches(tokenizer, train_texts, sequence_length, batch_size)
        val_batches, val_tokens = build_batches(tokenizer, val_texts, sequence_length, batch_size)
    except ValueError as error:
        print(f"failure: {error}")
        return 1

    stage = "windows_cuda"
    short_name = "100_step_mixed_domain_bpe_training"
    run_id = make_run_id(stage=stage, short_name=short_name)
    run_dir = create_run_directory(PROJECT_ROOT, stage=stage, run_id=run_id)

    snapshot_path = snapshot_config(CONFIG_PATH, run_dir)
    env = collect_basic_environment()
    metadata_path = write_run_metadata(
        run_dir=run_dir,
        run_id=run_id,
        project="EduCode-1.5B",
        stage=stage,
        hardware_target=config["hardware"].get("target", stage),
        config_path=str(snapshot_path),
        git_commit=get_git_commit(PROJECT_ROOT),
        git_branch=get_git_branch(PROJECT_ROOT),
        env=env,
        status="running",
        notes="D16.4 bounded 100-step mixed/domain BPE training in progress",
    )

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"device: {device}")
    print(f"max_steps: {MAX_STEPS}")
    print(f"eval_interval: {EVAL_INTERVAL}")

    model = TinyDecoderOnlyTransformer(model_config_from_dict(config))
    model.to(device)
    model.train()

    optimizer_config = config.get("optimizer") if isinstance(config.get("optimizer"), dict) else {}
    learning_rate = optimizer_config.get("learning_rate", 3e-4)
    weight_decay = optimizer_config.get("weight_decay", 0.0)
    betas = optimizer_config.get("betas", [0.9, 0.95])
    eps = optimizer_config.get("eps", 1e-8)
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=learning_rate,
        weight_decay=weight_decay,
        betas=(float(betas[0]), float(betas[1])),
        eps=float(eps),
    )

    metrics_path = run_dir / "metrics.jsonl"
    summary_path = run_dir / "summary.md"
    summary_json_path = run_dir / "summary.json"
    checkpoint_path = run_dir / "checkpoint_final.pt"

    train_losses: list[float] = []
    val_losses: list[float] = []
    first_train_loss: float | None = None
    final_train_loss: float | None = None
    final_val_loss: float | None = None
    final_grad_norm: float | None = None
    loss_all_finite = True
    val_loss_all_finite = True
    grad_all_finite = True
    total_tokens_seen = 0
    total_elapsed_seconds = 0.0
    last_gpu_memory_allocated_gib: float | None = None
    last_gpu_memory_reserved_gib: float | None = None

    for step in range(1, MAX_STEPS + 1):
        batch_x, batch_y = train_batches[(step - 1) % len(train_batches)]
        input_ids = torch.tensor(batch_x, dtype=torch.long, device=device)
        target_ids = torch.tensor(batch_y, dtype=torch.long, device=device)

        start_time = time.perf_counter()
        model.train()
        optimizer.zero_grad(set_to_none=True)
        logits = model(input_ids)
        if not bool(torch.isfinite(logits).all().item()):
            print(f"failure: non-finite logits at step {step}")
            return 1

        loss = next_token_cross_entropy(logits, target_ids)
        current_loss_finite = bool(torch.isfinite(loss).item())
        if not current_loss_finite:
            print(f"failure: non-finite loss at step {step}")
            return 1

        loss.backward()
        grad_norm = compute_grad_norm(model.parameters())
        current_grad_finite = gradients_all_finite(model.parameters())
        if grad_norm is None or not current_grad_finite:
            print(f"failure: non-finite gradient at step {step}")
            return 1

        optimizer.step()
        elapsed_seconds = time.perf_counter() - start_time
        total_elapsed_seconds += elapsed_seconds

        current_train_loss = float(loss.item())
        if first_train_loss is None:
            first_train_loss = current_train_loss
        final_train_loss = current_train_loss
        final_grad_norm = float(grad_norm)
        train_losses.append(current_train_loss)
        loss_all_finite = loss_all_finite and current_loss_finite
        grad_all_finite = grad_all_finite and current_grad_finite

        current_val_loss: float | None = None
        if step % EVAL_INTERVAL == 0:
            val_batch_x, val_batch_y = val_batches[((step // EVAL_INTERVAL) - 1) % len(val_batches)]
            try:
                current_val_loss = evaluate_loss(model, val_batch_x, val_batch_y, device)
            except ValueError as error:
                print(f"failure: {error} at step {step}")
                return 1
            final_val_loss = current_val_loss
            val_losses.append(current_val_loss)
            val_loss_all_finite = val_loss_all_finite and math.isfinite(current_val_loss)

        tokens_this_step = batch_size * sequence_length
        total_tokens_seen += tokens_this_step
        tokens_per_sec = tokens_this_step / elapsed_seconds if elapsed_seconds > 0 else None

        gpu_memory_allocated_gib = None
        gpu_memory_reserved_gib = None
        if device.type == "cuda":
            gpu_memory_allocated_gib = torch.cuda.memory_allocated(device) / (1024**3)
            gpu_memory_reserved_gib = torch.cuda.memory_reserved(device) / (1024**3)
            last_gpu_memory_allocated_gib = gpu_memory_allocated_gib
            last_gpu_memory_reserved_gib = gpu_memory_reserved_gib

        write_metrics_record(
            metrics_path,
            step=step,
            tokens_seen=total_tokens_seen,
            train_loss=current_train_loss,
            val_loss=current_val_loss,
            learning_rate=learning_rate,
            grad_norm=final_grad_norm,
            tokens_per_sec=tokens_per_sec,
            gpu_memory_allocated_gib=gpu_memory_allocated_gib,
            gpu_memory_reserved_gib=gpu_memory_reserved_gib,
            mfu=None,
            elapsed_seconds=elapsed_seconds,
            timestamp=datetime.now().isoformat(timespec="seconds"),
        )

        if current_val_loss is None:
            print(f"step {step}: train_loss={current_train_loss:.6f} grad_norm={final_grad_norm:.6f}")
        else:
            print(
                f"step {step}: train_loss={current_train_loss:.6f} val_loss={current_val_loss:.6f} grad_norm={final_grad_norm:.6f}"
            )

    save_checkpoint(
        path=checkpoint_path,
        model=model,
        optimizer=optimizer,
        step=MAX_STEPS,
        config=config,
        metadata={
            "run_id": run_id,
            "stage": stage,
            "notes": "D16.4 final checkpoint",
        },
    )

    reloaded_model = TinyDecoderOnlyTransformer(model_config_from_dict(config))
    reloaded_optimizer = torch.optim.AdamW(
        reloaded_model.parameters(),
        lr=learning_rate,
        weight_decay=weight_decay,
        betas=(float(betas[0]), float(betas[1])),
        eps=float(eps),
    )
    checkpoint = load_checkpoint(checkpoint_path, reloaded_model, reloaded_optimizer, map_location="cpu")
    parameter_compare = compare_model_parameters(model.to("cpu"), reloaded_model)
    checkpoint_reload_match = parameter_compare["all_match"] and checkpoint.get("step") == MAX_STEPS
    model.to(device)

    metrics_rows = len(train_losses)
    validation_rows = len(val_losses)
    approximate_tokens_per_sec = total_tokens_seen / total_elapsed_seconds if total_elapsed_seconds > 0 else None

    success = (
        first_train_loss is not None
        and final_train_loss is not None
        and final_val_loss is not None
        and final_grad_norm is not None
        and metrics_rows == MAX_STEPS
        and validation_rows == MAX_STEPS // EVAL_INTERVAL
        and loss_all_finite
        and val_loss_all_finite
        and grad_all_finite
        and checkpoint_path.exists()
        and checkpoint_reload_match
        and metrics_path.exists()
        and summary_path.parent.exists()
    )

    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    metadata["end_time"] = datetime.now().isoformat(timespec="seconds")
    metadata["status"] = "success" if success else "failed"
    metadata["notes"] = "D16.4 bounded 100-step mixed/domain BPE training complete"
    metadata["torch_version"] = torch.__version__
    metadata["cuda_available"] = torch.cuda.is_available()
    metadata["cuda_version"] = torch.version.cuda
    metadata["cudnn_version"] = torch.backends.cudnn.version() if torch.backends.cudnn.is_available() else None
    metadata["gpu_name"] = torch.cuda.get_device_name(device) if device.type == "cuda" else None
    metadata["gpu_memory_gib"] = (
        round(torch.cuda.get_device_properties(device).total_memory / (1024**3), 3) if device.type == "cuda" else None
    )
    metadata["train_source_category_counts"] = train_source_counts
    metadata["val_source_category_counts"] = val_source_counts
    write_json(metadata_path, metadata)

    summary_data = {
        "run_id": run_id,
        "device": str(device),
        "max_steps": MAX_STEPS,
        "eval_interval": EVAL_INTERVAL,
        "train_docs": len(train_texts),
        "val_docs": len(val_texts),
        "train_source_category_counts": train_source_counts,
        "val_source_category_counts": val_source_counts,
        "tokenizer_vocab_size": tokenizer.get_vocab_size(),
        "train_tokens": train_tokens,
        "val_tokens": val_tokens,
        "sequence_length": sequence_length,
        "batch_size": batch_size,
        "first_train_loss": round(first_train_loss, 6) if first_train_loss is not None else None,
        "final_train_loss": round(final_train_loss, 6) if final_train_loss is not None else None,
        "final_val_loss": round(final_val_loss, 6) if final_val_loss is not None else None,
        "loss_all_finite": loss_all_finite,
        "val_loss_all_finite": val_loss_all_finite,
        "grad_all_finite": grad_all_finite,
        "grad_norm_final": round(final_grad_norm, 6) if final_grad_norm is not None else None,
        "metrics_rows": metrics_rows,
        "validation_rows": validation_rows,
        "tokens_seen": total_tokens_seen,
        "elapsed_seconds": round(total_elapsed_seconds, 6),
        "approximate_tokens_per_sec": round(approximate_tokens_per_sec, 6)
        if approximate_tokens_per_sec is not None
        else None,
        "checkpoint_reload_match": checkpoint_reload_match,
        "last_gpu_memory_allocated_gib": round(last_gpu_memory_allocated_gib, 6)
        if last_gpu_memory_allocated_gib is not None
        else None,
        "last_gpu_memory_reserved_gib": round(last_gpu_memory_reserved_gib, 6)
        if last_gpu_memory_reserved_gib is not None
        else None,
        "bounded_small_training_only": True,
        "mixed_domain_corpus_only": True,
        "external_general_text_is_supplement_only": True,
        "no_generation_quality_claim": True,
        "success": bool(success),
    }
    write_json(summary_json_path, summary_data)

    summary_markdown = build_summary_markdown(
        {
            "run_id": run_id,
            "goal": "Validate a strictly bounded 100-step mixed/domain BPE training run with periodic validation on the approved mixed corpus.",
            "hardware": f"{device} / {config['hardware'].get('target')}",
            "config_path": str(snapshot_path),
            "result": "success" if success else "failed",
            "key_metrics": summary_data,
            "generation_preview": "",
            "notes": "Approved mixed_domain_external corpus only; mixed/domain BPE tokenizer only; external_general_text remains supplement only; bounded 100-step local training; checkpoint reload sanity check passed. No model quality claims."
            if checkpoint_reload_match
            else "Approved mixed_domain_external corpus only; mixed/domain BPE tokenizer only; external_general_text remains supplement only; bounded 100-step local training; checkpoint reload sanity check failed. No model quality claims.",
            "next_step": "Review the bounded mixed/domain BPE training artifacts before any longer or non-local run.",
        }
    )
    write_text(summary_path, summary_markdown)

    success = success and summary_path.exists() and summary_json_path.exists()

    print(f"run_id: {run_id}")
    print(f"run_dir: {run_dir}")
    print(f"device: {device}")
    print(f"max_steps: {MAX_STEPS}")
    print(f"train docs: {len(train_texts)}")
    print(f"val docs: {len(val_texts)}")
    print(f"train source_category counts: {json.dumps(train_source_counts, ensure_ascii=False, sort_keys=True)}")
    print(f"val source_category counts: {json.dumps(val_source_counts, ensure_ascii=False, sort_keys=True)}")
    print(f"tokenizer vocab size: {tokenizer.get_vocab_size()}")
    print(f"first_train_loss: {first_train_loss:.6f}" if first_train_loss is not None else "first_train_loss: None")
    print(f"final_train_loss: {final_train_loss:.6f}" if final_train_loss is not None else "final_train_loss: None")
    print(f"final_val_loss: {final_val_loss:.6f}" if final_val_loss is not None else "final_val_loss: None")
    print(f"loss_all_finite: {loss_all_finite}")
    print(f"val_loss_all_finite: {val_loss_all_finite}")
    print(f"checkpoint reload match: {checkpoint_reload_match}")
    print(f"metrics rows: {metrics_rows}")
    print(f"validation rows: {validation_rows}")
    print(f"success: {success}")
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
