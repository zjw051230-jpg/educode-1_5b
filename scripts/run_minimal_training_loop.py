from __future__ import annotations

import json
import math
import sys
import time
from datetime import datetime
from pathlib import Path

import torch

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = PROJECT_ROOT / "src"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from educode.byte_tokenizer import ByteTokenizer
from educode.checkpoint import compare_model_parameters, load_checkpoint, save_checkpoint
from educode.config_loader import load_json_config
from educode.config_validator import validate_config
from educode.generation import generate_text
from educode.losses import next_token_cross_entropy
from educode.run_logging import build_summary_markdown, write_generation_sample, write_json, write_metrics_record, write_text
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
from educode.toy_data import get_toy_corpus, join_corpus


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


def main() -> int:
    config_path = PROJECT_ROOT / "configs" / "windows" / "smoke_cuda_10m.json"
    config = load_json_config(config_path)

    errors = validate_config(config)
    if errors:
        print("validation: failed")
        for error in errors:
            print(f"- {error}")
        return 1

    stage = "windows_cuda"
    short_name = "minimal_training_loop"
    run_id = make_run_id(stage=stage, short_name=short_name)
    run_dir = create_run_directory(PROJECT_ROOT, stage=stage, run_id=run_id)

    snapshot_path = snapshot_config(config_path, run_dir)
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
        notes="Minimal training loop for W11.1",
    )

    tokenizer = ByteTokenizer()
    text = join_corpus(get_toy_corpus())
    token_ids = tokenizer.encode(text)

    model_context_length = config["model"].get("context_length")
    sequence_length = min(model_context_length, 16)
    batch_size = min(config["training"].get("batch_size", 1), 4)
    max_steps = min(config["training"].get("max_steps", 10), 10)

    samples = make_next_token_samples(token_ids, sequence_length)
    batches = batch_samples(samples, batch_size)
    if not batches:
        print("failure: no full batch could be created from the toy corpus")
        return 1

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"device: {device}")
    print(f"max_steps: {max_steps}")

    model = TinyDecoderOnlyTransformer(model_config_from_dict(config))
    model.to(device)
    model.train()

    optimizer_config = config.get("optimizer") if isinstance(config.get("optimizer"), dict) else {}
    learning_rate = optimizer_config.get("learning_rate", 3e-4)
    weight_decay = optimizer_config.get("weight_decay", 0.0)
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate, weight_decay=weight_decay)

    metrics_path = run_dir / "metrics.jsonl"
    generation_samples_path = run_dir / "generation_samples.jsonl"
    summary_path = run_dir / "summary.md"
    checkpoint_path = run_dir / "checkpoint_final.pt"

    first_loss: float | None = None
    final_loss: float | None = None
    final_grad_norm: float | None = None
    loss_all_finite = True
    grad_all_finite = True
    total_tokens_seen = 0

    for step in range(1, max_steps + 1):
        batch_x, batch_y = batches[(step - 1) % len(batches)]
        input_ids = torch.tensor(batch_x, dtype=torch.long, device=device)
        target_ids = torch.tensor(batch_y, dtype=torch.long, device=device)

        start_time = time.perf_counter()
        optimizer.zero_grad(set_to_none=True)
        logits = model(input_ids)
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

        if first_loss is None:
            first_loss = float(loss.item())
        final_loss = float(loss.item())
        final_grad_norm = float(grad_norm)
        loss_all_finite = loss_all_finite and current_loss_finite
        grad_all_finite = grad_all_finite and current_grad_finite

        tokens_this_step = batch_size * sequence_length
        total_tokens_seen += tokens_this_step
        tokens_per_sec = tokens_this_step / elapsed_seconds if elapsed_seconds > 0 else None

        gpu_memory_allocated_gib = None
        gpu_memory_reserved_gib = None
        if device.type == "cuda":
            gpu_memory_allocated_gib = torch.cuda.memory_allocated(device) / (1024**3)
            gpu_memory_reserved_gib = torch.cuda.memory_reserved(device) / (1024**3)

        write_metrics_record(
            metrics_path,
            step=step,
            tokens_seen=total_tokens_seen,
            train_loss=final_loss,
            val_loss=None,
            learning_rate=learning_rate,
            grad_norm=final_grad_norm,
            tokens_per_sec=tokens_per_sec,
            gpu_memory_allocated_gib=gpu_memory_allocated_gib,
            gpu_memory_reserved_gib=gpu_memory_reserved_gib,
            mfu=None,
            elapsed_seconds=elapsed_seconds,
            timestamp=datetime.now().isoformat(timespec="seconds"),
        )

        print(f"step {step}: loss={final_loss:.6f} grad_norm={final_grad_norm:.6f}")

    save_checkpoint(
        path=checkpoint_path,
        model=model,
        optimizer=optimizer,
        step=max_steps,
        config=config,
        metadata={
            "run_id": run_id,
            "stage": stage,
            "notes": "W11.1 final checkpoint",
        },
    )

    reloaded_model = TinyDecoderOnlyTransformer(model_config_from_dict(config))
    reloaded_optimizer = torch.optim.AdamW(reloaded_model.parameters(), lr=learning_rate, weight_decay=weight_decay)
    checkpoint = load_checkpoint(checkpoint_path, reloaded_model, reloaded_optimizer, map_location="cpu")
    parameter_compare = compare_model_parameters(model.to("cpu"), reloaded_model)
    checkpoint_reload_match = parameter_compare["all_match"] and checkpoint.get("step") == max_steps
    model.to(device)

    prompt = "hello"
    generated_preview = generate_text(
        model=model,
        tokenizer=tokenizer,
        prompt=prompt,
        max_new_tokens=16,
        device=device,
        temperature=1.0,
        top_k=64,
    )
    write_generation_sample(
        generation_samples_path,
        step=max_steps,
        prompt=prompt,
        output=generated_preview,
        max_new_tokens=16,
        temperature=1.0,
        top_k=64,
        top_p=None,
        checkpoint_path=str(checkpoint_path),
        timestamp=datetime.now().isoformat(timespec="seconds"),
    )

    success = (
        first_loss is not None
        and final_loss is not None
        and final_grad_norm is not None
        and loss_all_finite
        and grad_all_finite
        and checkpoint_path.exists()
        and checkpoint_reload_match
        and metrics_path.exists()
        and generation_samples_path.exists()
    )

    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    metadata["end_time"] = datetime.now().isoformat(timespec="seconds")
    metadata["status"] = "success" if success else "failed"
    metadata["notes"] = "W11.1 minimal training loop complete"
    metadata["torch_version"] = torch.__version__
    metadata["cuda_available"] = torch.cuda.is_available()
    metadata["cuda_version"] = torch.version.cuda
    metadata["cudnn_version"] = torch.backends.cudnn.version() if torch.backends.cudnn.is_available() else None
    metadata["gpu_name"] = torch.cuda.get_device_name(device) if device.type == "cuda" else None
    metadata["gpu_memory_gib"] = (
        round(torch.cuda.get_device_properties(device).total_memory / (1024**3), 3) if device.type == "cuda" else None
    )
    write_json(metadata_path, metadata)

    summary_markdown = build_summary_markdown(
        {
            "run_id": run_id,
            "goal": "Validate a strictly bounded toy-data minimal training loop on Windows.",
            "hardware": f"{device} / {config['hardware'].get('target')}",
            "config_path": str(snapshot_path),
            "result": "success" if success else "failed",
            "key_metrics": {
                "max_steps": max_steps,
                "first_loss": round(first_loss, 6) if first_loss is not None else None,
                "final_loss": round(final_loss, 6) if final_loss is not None else None,
                "loss_all_finite": loss_all_finite,
                "grad_norm_final": round(final_grad_norm, 6) if final_grad_norm is not None else None,
            },
            "generation_preview": generated_preview[:200],
            "notes": "Toy data only; ByteTokenizer temporary path; checkpoint reload sanity check passed."
            if checkpoint_reload_match
            else "Toy data only; ByteTokenizer temporary path; checkpoint reload sanity check failed.",
            "next_step": "W11.2 minimal training loop review",
        }
    )
    write_text(summary_path, summary_markdown)

    print(f"run_id: {run_id}")
    print(f"run_dir: {run_dir}")
    print(f"device: {device}")
    print(f"max_steps: {max_steps}")
    print(f"first_loss: {first_loss:.6f}" if first_loss is not None else "first_loss: None")
    print(f"final_loss: {final_loss:.6f}" if final_loss is not None else "final_loss: None")
    print(f"loss_all_finite: {loss_all_finite}")
    print(f"grad_all_finite: {grad_all_finite}")
    print(f"checkpoint exists: {checkpoint_path.exists()}")
    print(f"checkpoint reload match: {checkpoint_reload_match}")
    print(f"generation preview: {generated_preview[:120]}")
    print(f"metrics.jsonl exists: {metrics_path.exists()}")
    print(f"generation_samples.jsonl exists: {generation_samples_path.exists()}")
    print(f"summary.md exists: {summary_path.exists()}")
    print(f"success: {success}")
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
