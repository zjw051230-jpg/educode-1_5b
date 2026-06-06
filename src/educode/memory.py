from __future__ import annotations

from dataclasses import asdict, dataclass

import torch
from torch import nn
from torch.utils.checkpoint import checkpoint


@dataclass(frozen=True)
class MemoryKnobsConfig:
    activation_checkpointing: bool = False
    checkpoint_segments: int = 1
    preserve_rng_state: bool = True

    def __post_init__(self) -> None:
        if self.checkpoint_segments <= 0:
            raise ValueError("checkpoint_segments must be positive")

    def to_dict(self) -> dict:
        return asdict(self)


def validate_memory_knobs(config: MemoryKnobsConfig) -> dict:
    return {
        "status": "valid",
        "activation_checkpointing": config.activation_checkpointing,
        "checkpoint_segments": config.checkpoint_segments,
        "preserve_rng_state": config.preserve_rng_state,
        "default_enabled": False,
    }


def checkpoint_module_forward(
    module: nn.Module, x: torch.Tensor, config: MemoryKnobsConfig
) -> torch.Tensor:
    if not config.activation_checkpointing:
        return module(x)

    def run(input_tensor: torch.Tensor) -> torch.Tensor:
        return module(input_tensor)

    return checkpoint(
        run,
        x,
        preserve_rng_state=config.preserve_rng_state,
        use_reentrant=False,
    )
