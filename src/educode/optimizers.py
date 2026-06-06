from __future__ import annotations

from collections.abc import Iterable
from typing import Any

import torch

from educode.muon import MuonExperimental

SUPPORTED_OPTIMIZERS = ("adamw", "muon_experimental")
DEFAULT_OPTIMIZER = "adamw"


def normalize_optimizer_name(name: str | None) -> str:
    optimizer_name = DEFAULT_OPTIMIZER if name is None else str(name).strip().lower()
    if optimizer_name not in SUPPORTED_OPTIMIZERS:
        allowed = ", ".join(SUPPORTED_OPTIMIZERS)
        raise ValueError(f"unsupported optimizer {name!r}; expected one of: {allowed}")
    return optimizer_name


def _adamw_kwargs(config: dict[str, Any]) -> dict[str, Any]:
    betas = config.get("betas", (0.9, 0.95))
    if not isinstance(betas, (list, tuple)) or len(betas) != 2:
        raise ValueError("optimizer.betas must contain exactly two values")
    return {
        "lr": float(config.get("learning_rate", config.get("lr", 3e-4))),
        "weight_decay": float(config.get("weight_decay", 0.0)),
        "betas": (float(betas[0]), float(betas[1])),
        "eps": float(config.get("eps", 1e-8)),
    }


def create_optimizer(parameters: Iterable[torch.nn.Parameter], config: dict[str, Any] | None = None):
    optimizer_config = config or {}
    name = normalize_optimizer_name(optimizer_config.get("name"))
    if name == "adamw":
        return torch.optim.AdamW(parameters, **_adamw_kwargs(optimizer_config))
    if optimizer_config.get("experimental_ack_required") is not True:
        raise ValueError("muon_experimental requires optimizer.experimental_ack_required=true")
    return MuonExperimental(
        parameters,
        lr=float(optimizer_config.get("learning_rate", optimizer_config.get("lr", 0.02))),
        momentum=float(optimizer_config.get("momentum", 0.95)),
        ns_steps=int(optimizer_config.get("newton_schulz_steps", 5)),
    )
