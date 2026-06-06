from __future__ import annotations

from collections.abc import Iterable
from typing import Any

import torch

SUPPORTED_OPTIMIZERS = ("adamw", "muon_experimental")
DEFAULT_OPTIMIZER = "adamw"


class ExperimentalOptimizerUnavailable(RuntimeError):
    """Raised when an experimental optimizer path is selected before implementation."""


def normalize_optimizer_name(name: str | None) -> str:
    optimizer_name = DEFAULT_OPTIMIZER if name is None else str(name).strip().lower()
    if optimizer_name not in SUPPORTED_OPTIMIZERS:
        allowed = ", ".join(SUPPORTED_OPTIMIZERS)
        raise ValueError(f"unsupported optimizer {name!r}; expected one of: {allowed}")
    return optimizer_name


def _adamw_kwargs(config: dict[str, Any]) -> dict[str, Any]:
    betas = config.get("betas", (0.9, 0.95))
    if not isinstance(betas, (list, tuple)) or len(betas) != 2:
        raise ValueError("optimizer.betas must contain exactly two numeric values")
    return {
        "lr": float(config.get("learning_rate", config.get("lr", 3e-4))),
        "weight_decay": float(config.get("weight_decay", 0.0)),
        "betas": (float(betas[0]), float(betas[1])),
        "eps": float(config.get("eps", 1e-8)),
    }


def create_optimizer(
    parameters: Iterable[torch.nn.Parameter],
    config: dict[str, Any] | None = None,
    *,
    allow_experimental: bool = False,
) -> torch.optim.Optimizer:
    optimizer_config = config or {}
    optimizer_name = normalize_optimizer_name(optimizer_config.get("name"))

    if optimizer_name == "adamw":
        return torch.optim.AdamW(parameters, **_adamw_kwargs(optimizer_config))

    if not allow_experimental:
        raise ExperimentalOptimizerUnavailable(
            "muon_experimental is guarded and disabled by default; set allow_experimental=True only in a dedicated experiment"
        )

    raise ExperimentalOptimizerUnavailable(
        "muon_experimental is declared for future experiments but is not implemented or training-validated yet"
    )
