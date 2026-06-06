from __future__ import annotations

from dataclasses import asdict, dataclass

import torch
from torch import nn
from torch.utils.checkpoint import checkpoint


VALID_GRANULARITIES = {"none", "block", "attention", "mlp"}


@dataclass(frozen=True)
class ActivationCheckpointConfig:
    enabled: bool = False
    granularity: str = "none"
    preserve_rng_state: bool = True
    experimental_ack: bool = False

    def __post_init__(self) -> None:
        if self.granularity not in VALID_GRANULARITIES:
            raise ValueError("unknown activation checkpoint granularity")
        if self.enabled and self.granularity == "none":
            raise ValueError("enabled checkpointing requires non-none granularity")
        if self.enabled and not self.experimental_ack:
            raise ValueError("checkpointing enabled requires experimental_ack=True")

    def to_dict(self) -> dict:
        return asdict(self)


def validate_activation_checkpoint_config(config: ActivationCheckpointConfig) -> dict:
    return {
        "status": "valid",
        "enabled": config.enabled,
        "granularity": config.granularity,
        "preserve_rng_state": config.preserve_rng_state,
        "experimental_ack": config.experimental_ack,
        "default_enabled": False,
    }


def checkpoint_forward(
    module: nn.Module, x: torch.Tensor, config: ActivationCheckpointConfig
) -> torch.Tensor:
    if not config.enabled:
        return module(x)

    def run(input_tensor: torch.Tensor) -> torch.Tensor:
        return module(input_tensor)

    return checkpoint(
        run,
        x,
        preserve_rng_state=config.preserve_rng_state,
        use_reentrant=False,
    )
