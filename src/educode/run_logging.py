from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


def write_json(path: str | Path, data: Any) -> None:
    target_path = Path(path)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def append_jsonl(path: str | Path, record: dict[str, Any]) -> None:
    target_path = Path(path)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    with target_path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record, ensure_ascii=False) + "\n")


def write_text(path: str | Path, text: str) -> None:
    target_path = Path(path)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(text, encoding="utf-8")


def write_metrics_record(path: str | Path, **kwargs: Any) -> None:
    record = {
        "step": kwargs.get("step"),
        "tokens_seen": kwargs.get("tokens_seen"),
        "train_loss": kwargs.get("train_loss"),
        "val_loss": kwargs.get("val_loss"),
        "learning_rate": kwargs.get("learning_rate"),
        "grad_norm": kwargs.get("grad_norm"),
        "tokens_per_sec": kwargs.get("tokens_per_sec"),
        "gpu_memory_allocated_gib": kwargs.get("gpu_memory_allocated_gib"),
        "gpu_memory_reserved_gib": kwargs.get("gpu_memory_reserved_gib"),
        "mfu": kwargs.get("mfu"),
        "elapsed_seconds": kwargs.get("elapsed_seconds"),
        "timestamp": kwargs.get("timestamp", datetime.now().isoformat(timespec="seconds")),
    }
    append_jsonl(path, record)


def write_generation_sample(path: str | Path, **kwargs: Any) -> None:
    record = {
        "step": kwargs.get("step"),
        "prompt": kwargs.get("prompt"),
        "output": kwargs.get("output"),
        "max_new_tokens": kwargs.get("max_new_tokens"),
        "temperature": kwargs.get("temperature"),
        "top_k": kwargs.get("top_k"),
        "top_p": kwargs.get("top_p"),
        "checkpoint_path": kwargs.get("checkpoint_path"),
        "timestamp": kwargs.get("timestamp", datetime.now().isoformat(timespec="seconds")),
    }
    append_jsonl(path, record)


def build_summary_markdown(summary: dict[str, Any]) -> str:
    key_metrics = summary.get("key_metrics") or {}
    metrics_lines = "\n".join(f"- {key}: {value}" for key, value in key_metrics.items()) or "- None"

    lines = [
        f"# Run Summary: {summary.get('run_id')}",
        "",
        "## Goal",
        str(summary.get("goal", "")),
        "",
        "## Hardware",
        str(summary.get("hardware", "")),
        "",
        "## Config Path",
        str(summary.get("config_path", "")),
        "",
        "## Result",
        str(summary.get("result", "")),
        "",
        "## Key Metrics",
        metrics_lines,
        "",
        "## Generation Preview",
        str(summary.get("generation_preview", "")),
        "",
        "## Notes",
        str(summary.get("notes", "")),
        "",
        "## Next Step",
        str(summary.get("next_step", "")),
    ]
    return "\n".join(lines) + "\n"
