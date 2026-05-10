from __future__ import annotations

from pathlib import Path
from typing import Any

import torch
from torch import nn
from torch.optim import Optimizer


def save_checkpoint(
    path: str | Path,
    model: nn.Module,
    optimizer: Optimizer,
    step: int,
    config: dict,
    metadata: dict | None = None,
) -> None:
    checkpoint_path = Path(path)
    checkpoint_path.parent.mkdir(parents=True, exist_ok=True)

    checkpoint = {
        "model_state_dict": model.state_dict(),
        "optimizer_state_dict": optimizer.state_dict(),
        "step": step,
        "config": config,
        "metadata": metadata or {},
    }
    torch.save(checkpoint, checkpoint_path)


def load_checkpoint(
    path: str | Path,
    model: nn.Module,
    optimizer: Optimizer | None = None,
    map_location: str | torch.device = "cpu",
) -> dict[str, Any]:
    checkpoint_path = Path(path)
    if not checkpoint_path.exists():
        raise FileNotFoundError(f"Checkpoint file not found: {checkpoint_path}")

    checkpoint = torch.load(checkpoint_path, map_location=map_location, weights_only=True)
    if not isinstance(checkpoint, dict):
        raise ValueError("Checkpoint must be a dictionary")
    if "model_state_dict" not in checkpoint:
        raise KeyError("Checkpoint is missing model_state_dict")

    model.load_state_dict(checkpoint["model_state_dict"])

    optimizer_state = checkpoint.get("optimizer_state_dict")
    if optimizer is not None and optimizer_state is not None:
        optimizer.load_state_dict(optimizer_state)

    return checkpoint


def compare_model_parameters(model_a: nn.Module, model_b: nn.Module) -> dict[str, Any]:
    model_a_state = model_a.state_dict()
    model_b_state = model_b.state_dict()

    num_parameters_compared = 0
    all_match = True
    max_abs_diff = 0.0
    first_mismatch_name: str | None = None

    with torch.no_grad():
        for name, tensor_a in model_a_state.items():
            if name not in model_b_state:
                raise KeyError(f"Parameter missing from model_b state_dict: {name}")

            tensor_b = model_b_state[name]
            if tensor_a.shape != tensor_b.shape:
                raise ValueError(f"Parameter shape mismatch for {name}: {tuple(tensor_a.shape)} != {tuple(tensor_b.shape)}")

            num_parameters_compared += tensor_a.numel()
            diff = (tensor_a.detach().to("cpu") - tensor_b.detach().to("cpu")).abs()
            current_max_abs_diff = float(diff.max().item()) if diff.numel() > 0 else 0.0
            max_abs_diff = max(max_abs_diff, current_max_abs_diff)

            if not torch.equal(tensor_a, tensor_b):
                all_match = False
                if first_mismatch_name is None:
                    first_mismatch_name = name

    return {
        "num_parameters_compared": num_parameters_compared,
        "all_match": all_match,
        "max_abs_diff": max_abs_diff,
        "first_mismatch_name": first_mismatch_name,
    }
