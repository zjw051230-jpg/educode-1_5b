from __future__ import annotations

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
from educode.config_loader import load_json_config
from educode.config_validator import validate_config
from educode.generation import generate_text
from educode.losses import next_token_cross_entropy
from educode.run_logging import (
    build_summary_markdown,
    write_generation_sample,
    write_metrics_record,
    write_text,
)
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
    short_name = "logging_integration"
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
        status="success",
        notes="Logging integration check for W10.11",
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

    start_time = time.perf_counter()
    model.eval()
    with torch.no_grad():
        logits = model(input_ids)
        loss = next_token_cross_entropy(logits, target_ids)
    elapsed_seconds = time.perf_counter() - start_time

    metrics_path = run_dir / "metrics.jsonl"
    generation_samples_path = run_dir / "generation_samples.jsonl"
    summary_path = run_dir / "summary.md"

    gpu_memory_allocated_gib = None
    gpu_memory_reserved_gib = None
    if device.type == "cuda":
        gpu_memory_allocated_gib = torch.cuda.memory_allocated(device) / (1024**3)
        gpu_memory_reserved_gib = torch.cuda.memory_reserved(device) / (1024**3)

    write_metrics_record(
        metrics_path,
        step=0,
        tokens_seen=batch_size * sequence_length,
        train_loss=loss.item(),
        val_loss=None,
        learning_rate=None,
        grad_norm=None,
        tokens_per_sec=None,
        gpu_memory_allocated_gib=gpu_memory_allocated_gib,
        gpu_memory_reserved_gib=gpu_memory_reserved_gib,
        mfu=None,
        elapsed_seconds=elapsed_seconds,
        timestamp=datetime.now().isoformat(timespec="seconds"),
    )

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
        step=0,
        prompt=prompt,
        output=generated_preview,
        max_new_tokens=16,
        temperature=1.0,
        top_k=64,
        top_p=None,
        checkpoint_path=None,
        timestamp=datetime.now().isoformat(timespec="seconds"),
    )

    summary_markdown = build_summary_markdown(
        {
            "run_id": run_id,
            "goal": "Validate standard run logging files for a minimal forward/loss/generation path.",
            "hardware": f"{device} / {config['hardware'].get('target')}",
            "config_path": str(snapshot_path),
            "result": "success",
            "key_metrics": {
                "train_loss": round(loss.item(), 6),
                "tokens_seen": batch_size * sequence_length,
                "elapsed_seconds": round(elapsed_seconds, 6),
            },
            "generation_preview": generated_preview[:200],
            "notes": "W10.11 logging integration check only.",
            "next_step": "W10.12 one-step smoke run",
        }
    )
    write_text(summary_path, summary_markdown)

    success = (
        metadata_path.exists()
        and snapshot_path.exists()
        and metrics_path.exists()
        and generation_samples_path.exists()
        and summary_path.exists()
        and bool(torch.isfinite(loss).item())
    )

    print(f"run_id: {run_id}")
    print(f"run_dir: {run_dir}")
    print(f"run_metadata.json exists: {metadata_path.exists()}")
    print(f"run_config.json exists: {snapshot_path.exists()}")
    print(f"metrics.jsonl exists: {metrics_path.exists()}")
    print(f"generation_samples.jsonl exists: {generation_samples_path.exists()}")
    print(f"summary.md exists: {summary_path.exists()}")
    print(f"loss value: {loss.item():.6f}")
    print(f"generated preview: {generated_preview[:120]}")
    print(f"success: {success}")
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
