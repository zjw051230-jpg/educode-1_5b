from __future__ import annotations

from dataclasses import dataclass

import torch
from torch import nn
from torch.nn import functional as F


@dataclass(frozen=True)
class MoEConfig:
    d_model: int
    d_ff: int
    num_experts: int
    top_k: int = 2

    def __post_init__(self) -> None:
        if self.d_model <= 0:
            raise ValueError("moe.d_model must be positive")
        if self.d_ff <= self.d_model:
            raise ValueError("moe.d_ff must be greater than d_model")
        if self.num_experts <= 0:
            raise ValueError("moe.num_experts must be positive")
        if self.top_k <= 0 or self.top_k > self.num_experts:
            raise ValueError("moe.top_k must be in [1, num_experts]")


class TopKRouter(nn.Module):
    def __init__(self, d_model: int, num_experts: int, top_k: int = 2) -> None:
        super().__init__()
        if d_model <= 0:
            raise ValueError("d_model must be positive")
        if num_experts <= 0:
            raise ValueError("num_experts must be positive")
        if top_k <= 0 or top_k > num_experts:
            raise ValueError("top_k must be in [1, num_experts]")
        self.num_experts = num_experts
        self.top_k = top_k
        self.router = nn.Linear(d_model, num_experts, bias=False)

    def forward(self, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        if x.ndim != 3:
            raise ValueError("router input must have shape [batch, sequence, d_model]")
        logits = self.router(x)
        top_values, top_indices = torch.topk(logits, k=self.top_k, dim=-1)
        top_weights = torch.softmax(top_values, dim=-1)
        return top_indices, top_weights


class ExpertMLP(nn.Module):
    def __init__(self, d_model: int, d_ff: int) -> None:
        super().__init__()
        self.gate_proj = nn.Linear(d_model, d_ff, bias=False)
        self.up_proj = nn.Linear(d_model, d_ff, bias=False)
        self.down_proj = nn.Linear(d_ff, d_model, bias=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.down_proj(F.silu(self.gate_proj(x)) * self.up_proj(x))


class SparseMoESkeleton(nn.Module):
    """Prepared MoE skeleton for local shape tests; not wired into dense training."""

    def __init__(self, config: MoEConfig) -> None:
        super().__init__()
        self.config = config
        self.router = TopKRouter(config.d_model, config.num_experts, config.top_k)
        self.experts = nn.ModuleList(ExpertMLP(config.d_model, config.d_ff) for _ in range(config.num_experts))

    def forward(self, x: torch.Tensor) -> dict[str, torch.Tensor]:
        top_indices, top_weights = self.router(x)
        return {
            "top_indices": top_indices,
            "top_weights": top_weights,
        }
