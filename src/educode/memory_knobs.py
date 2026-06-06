from __future__ import annotations

from dataclasses import dataclass

from src.educode.activation_checkpointing import ActivationCheckpointConfig


@dataclass(frozen=True)
class MemoryKnobSummary:
    activation_checkpointing: ActivationCheckpointConfig

    def to_dict(self) -> dict:
        return {
            "activation_checkpointing": self.activation_checkpointing.to_dict(),
            "modal_gpu_training_run": False,
        }
