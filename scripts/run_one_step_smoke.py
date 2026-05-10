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
    short_name = "one_step_smoke"
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
        notes="One-step smoke run for W10.12",
    )

    tokenizer = ByteTokenizer()
    text = join_corpus(get_toy_corpus())
    token_ids = tokenizer.encode(text)

    model_context_length = config["model"].get("context_length")
    sequence_length = min(model_context_length, 16)
    batch_size = min(config["training"].get("batch_size", 1), 4)

    samples = make_next_token_samples(token_ids, sequence_length)
    batches = batch_samples(samples, batch_size)
    if not batches:
        print("failure: no full batch could be created from the toy corpus")
        return 1

    batch_x, batch_y = batches[0]
    input_ids = torch.tensor(batch_x, dtype=torch.long)
    target_ids = torch.tensor(batch_y, dtype=torch.long)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = TinyDecoderOnlyTransformer(model_config_from_dict(config))
    model.to(device)
    input_ids = input_ids.to(device)
    target_ids = target_ids.to(device)

    optimizer_config = config.get("optimizer") if isinstance(config.get("optimizer"), dict) else {}
    learning_rate = optimizer_config.get("learning_rate", 3e-4)
    weight_decay = optimizer_config.get("weight_decay", 0.0)
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate, weight_decay=weight_decay)

    metrics_path = run_dir / "metrics.jsonl"
    generation_samples_path = run_dir / "generation_samples.jsonl"
    summary_path = run_dir / "summary.md"
    checkpoint_path = run_dir / "checkpoint.pt"

    start_time = time.perf_counter()
    model.train()
    optimizer.zero_grad(set_to_none=True)
    logits = model(input_ids)
    loss = next_token_cross_entropy(logits, target_ids)
    loss.backward()
    grad_norm = compute_grad_norm(model.parameters())
    optimizer.step()
    elapsed_seconds = time.perf_counter() - start_time

    checkpoint_metadata = {
        "run_id": run_id,
        "stage": stage,
        "notes": "W10.12 one-step smoke checkpoint",
    }
    save_checkpoint(
        path=checkpoint_path,
        model=model,
        optimizer=optimizer,
        step=1,
        config=config,
        metadata=checkpoint_metadata,
    )

    reloaded_model = TinyDecoderOnlyTransformer(model_config_from_dict(config))
    reloaded_optimizer = torch.optim.AdamW(reloaded_model.parameters(), lr=learning_rate, weight_decay=weight_decay)
    checkpoint = load_checkpoint(checkpoint_path, reloaded_model, reloaded_optimizer, map_location="cpu")
    parameter_compare = compare_model_parameters(model.to("cpu"), reloaded_model)
    model.to(device)

    prompt = "hello"
    generation_config = config.get("generation") if isinstance(config.get("generation"), dict) else {}
    max_new_tokens = min(int(generation_config.get("max_new_tokens", 16)), 16)
    temperature = float(generation_config.get("temperature", 1.0))
    top_k = int(generation_config.get("top_k", 64))
    generated_preview = generate_text(
        model=model,
        tokenizer=tokenizer,
        prompt=prompt,
        max_new_tokens=max_new_tokens,
        device=device,
        temperature=temperature,
        top_k=top_k,
    )

    gpu_memory_allocated_gib = None
    gpu_memory_reserved_gib = None
    if device.type == "cuda":
        gpu_memory_allocated_gib = torch.cuda.memory_allocated(device) / (1024**3)
        gpu_memory_reserved_gib = torch.cuda.memory_reserved(device) / (1024**3)

    tokens_seen = batch_size * sequence_length
    tokens_per_sec = tokens_seen / elapsed_seconds if elapsed_seconds > 0 else None

    write_metrics_record(
        metrics_path,
        step=1,
        tokens_seen=tokens_seen,
        train_loss=loss.item(),
        val_loss=None,
        learning_rate=learning_rate,
        grad_norm=grad_norm,
        tokens_per_sec=tokens_per_sec,
        gpu_memory_allocated_gib=gpu_memory_allocated_gib,
        gpu_memory_reserved_gib=gpu_memory_reserved_gib,
        mfu=None,
        elapsed_seconds=elapsed_seconds,
        timestamp=datetime.now().isoformat(timespec="seconds"),
    )

    write_generation_sample(
        generation_samples_path,
        step=1,
        prompt=prompt,
        output=generated_preview,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        top_k=top_k,
        top_p=None,
        checkpoint_path=str(checkpoint_path),
        timestamp=datetime.now().isoformat(timespec="seconds"),
    )

    success = (
        metadata_path.exists()
        and snapshot_path.exists()
        and checkpoint_path.exists()
        and metrics_path.exists()
        and generation_samples_path.exists()
        and bool(torch.isfinite(loss).item())
        and grad_norm is not None
        and parameter_compare["all_match"]
        and checkpoint.get("step") == 1
    )

    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    metadata["end_time"] = datetime.now().isoformat(timespec="seconds")
    metadata["status"] = "success" if success else "failed"
    metadata["notes"] = "W10.12 one-step smoke run complete"
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
            "goal": "Validate one closed-loop smoke step with forward, loss, backward, optimizer, checkpoint, generation, and logging.",
            "hardware": f"{device} / {config['hardware'].get('target')}",
            "config_path": str(snapshot_path),
            "result": "success" if success else "failed",
            "key_metrics": {
                "train_loss": round(loss.item(), 6),
                "tokens_seen": tokens_seen,
                "grad_norm": round(grad_norm, 6) if grad_norm is not None else None,
                "elapsed_seconds": round(elapsed_seconds, 6),
            },
            "generation_preview": generated_preview[:200],
            "notes": f"Checkpoint saved to {checkpoint_path}",
            "next_step": "W10.13 multi-step smoke loop",
        }
    )
    write_text(summary_path, summary_markdown)

    print(f"run_id: {run_id}")
    print(f"run_dir: {run_dir}")
    print(f"device: {device}")
    print(f"input_ids shape: {tuple(input_ids.shape)}")
    print(f"target_ids shape: {tuple(target_ids.shape)}")
    print(f"loss value: {loss.item():.6f}")
    print(f"grad_norm: {grad_norm:.6f}" if grad_norm is not None else "grad_norm: None")
    print(f"checkpoint exists: {checkpoint_path.exists()}")
    print(f"checkpoint step: {checkpoint.get('step')}")
    print(f"checkpoint parameter all_match: {parameter_compare['all_match']}")
    print(f"run_metadata.json exists: {metadata_path.exists()}")
    print(f"run_config.json exists: {snapshot_path.exists()}")
    print(f"metrics.jsonl exists: {metrics_path.exists()}")
    print(f"generation_samples.jsonl exists: {generation_samples_path.exists()}")
    print(f"summary.md exists: {summary_path.exists()}")
    print(f"generated preview: {generated_preview[:120]}")
    print(f"success: {success}")
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
