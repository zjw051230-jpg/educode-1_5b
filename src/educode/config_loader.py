from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json_config(path: str | Path) -> dict[str, Any]:
    config_path = Path(path)

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    if config_path.suffix.lower() != ".json":
        raise ValueError(f"Config file must be a .json file: {config_path}")

    with config_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError("Top-level JSON value must be an object")

    return data


def summarize_config(config: dict[str, Any]) -> dict[str, Any]:
    hardware = config.get("hardware") if isinstance(config.get("hardware"), dict) else {}
    tokenizer = config.get("tokenizer") if isinstance(config.get("tokenizer"), dict) else {}
    model = config.get("model") if isinstance(config.get("model"), dict) else {}
    training = config.get("training") if isinstance(config.get("training"), dict) else {}
    profiling = config.get("profiling") if isinstance(config.get("profiling"), dict) else {}
    run = config.get("run") if isinstance(config.get("run"), dict) else {}

    return {
        "run_name": run.get("run_name"),
        "hardware.target": hardware.get("target"),
        "hardware.dtype": hardware.get("dtype"),
        "tokenizer.type": tokenizer.get("type"),
        "tokenizer.vocab_size": tokenizer.get("vocab_size"),
        "model.architecture": model.get("architecture"),
        "model.vocab_size": model.get("vocab_size"),
        "model.context_length": model.get("context_length"),
        "model.num_layers": model.get("num_layers"),
        "model.d_model": model.get("d_model"),
        "model.num_heads": model.get("num_heads"),
        "model.d_ff": model.get("d_ff"),
        "training.max_steps": training.get("max_steps"),
        "training.batch_size": training.get("batch_size"),
        "training.gradient_accumulation_steps": training.get("gradient_accumulation_steps"),
        "profiling.attention_backend": profiling.get("attention_backend"),
    }


def pretty_print_summary(summary: dict[str, Any]) -> None:
    print("Config summary:")
    for key, value in summary.items():
        print(f"- {key}: {value}")
