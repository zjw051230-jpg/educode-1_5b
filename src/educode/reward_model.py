from __future__ import annotations

from dataclasses import asdict, dataclass

import torch
from torch import nn
from torch.nn import functional as F


@dataclass(frozen=True)
class RewardPair:
    prompt: str
    chosen: str
    rejected: str
    source: str = "synthetic"

    def __post_init__(self) -> None:
        for field_name in ("prompt", "chosen", "rejected"):
            if not getattr(self, field_name).strip():
                raise ValueError(f"{field_name} must be non-empty")
        if self.chosen == self.rejected:
            raise ValueError("chosen and rejected responses must differ")

    def to_dict(self) -> dict:
        return asdict(self)


class RewardHead(nn.Module):
    def __init__(self, hidden_size: int) -> None:
        super().__init__()
        if hidden_size <= 0:
            raise ValueError("hidden_size must be positive")
        self.proj = nn.Linear(hidden_size, 1)

    def forward(self, hidden_states: torch.Tensor) -> torch.Tensor:
        return self.proj(hidden_states).squeeze(-1)


def pairwise_ranking_loss(
    chosen_rewards: torch.Tensor, rejected_rewards: torch.Tensor
) -> torch.Tensor:
    if chosen_rewards.shape != rejected_rewards.shape:
        raise ValueError("chosen and rejected reward tensors must have the same shape")
    return -F.logsigmoid(chosen_rewards - rejected_rewards).mean()


def validate_reward_pair(pair: RewardPair) -> dict:
    return {
        "status": "valid",
        "prompt_chars": len(pair.prompt),
        "chosen_chars": len(pair.chosen),
        "rejected_chars": len(pair.rejected),
        "source": pair.source,
    }
