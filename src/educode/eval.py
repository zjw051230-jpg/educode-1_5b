from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import torch

from educode.losses import next_token_cross_entropy


def evaluate_next_token_loss(model, input_ids: torch.Tensor, target_ids: torch.Tensor, device: torch.device | str = "cpu") -> dict[str, float]:
    if not isinstance(input_ids, torch.Tensor) or not isinstance(target_ids, torch.Tensor):
        raise TypeError("input_ids and target_ids must be torch tensors")
    model.eval()
    input_ids = input_ids.to(device=device, dtype=torch.long)
    target_ids = target_ids.to(device=device, dtype=torch.long)
    with torch.no_grad():
        logits = model(input_ids)
        loss = next_token_cross_entropy(logits, target_ids)
    loss_value = float(loss.item())
    if not math.isfinite(loss_value):
        raise ValueError("evaluation loss must be finite")
    return {
        "loss": loss_value,
        "perplexity": float(math.exp(loss_value)) if loss_value < 80 else float("inf"),
        "tokens_evaluated": int(target_ids.numel()),
    }


def checkpoint_metadata_summary(path: str | Path, max_json_bytes: int = 1_000_000) -> dict[str, Any]:
    checkpoint_path = Path(path)
    if not checkpoint_path.exists():
        raise FileNotFoundError(f"checkpoint metadata path not found: {checkpoint_path}")
    size_bytes = checkpoint_path.stat().st_size
    summary: dict[str, Any] = {
        "path": checkpoint_path.as_posix(),
        "size_bytes": size_bytes,
        "metadata_loaded": False,
        "loads_model_weights": False,
    }
    if checkpoint_path.suffix.lower() != ".json":
        summary["note"] = "non-json checkpoint path was inspected by metadata only; tensor weights were not loaded"
        return summary
    if size_bytes > max_json_bytes:
        raise ValueError("checkpoint metadata json is too large for local metadata-only loading")

    payload = json.loads(checkpoint_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("checkpoint metadata json must be an object")
    summary["metadata_loaded"] = True
    summary["metadata"] = payload.get("metadata", payload)
    return summary
