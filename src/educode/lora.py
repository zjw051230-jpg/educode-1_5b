from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Mapping

import torch
from torch import nn
from torch.nn import functional as F


@dataclass(frozen=True)
class LoRAConfig:
    rank: int = 8
    alpha: float = 16.0
    enabled: bool = False
    freeze_base: bool = True

    def __post_init__(self) -> None:
        if self.rank <= 0:
            raise ValueError("rank must be positive")
        if self.alpha <= 0:
            raise ValueError("alpha must be positive")


class LoRALinear(nn.Module):
    """Small LoRA wrapper for torch.nn.Linear, disabled by default."""

    def __init__(self, base: nn.Linear, config: LoRAConfig) -> None:
        super().__init__()
        if not isinstance(base, nn.Linear):
            raise TypeError("base must be torch.nn.Linear")
        self.base = base
        self.config = config
        self.scaling = config.alpha / config.rank
        self.merged = False
        self.lora_a = nn.Parameter(torch.empty(config.rank, base.in_features))
        self.lora_b = nn.Parameter(torch.zeros(base.out_features, config.rank))
        nn.init.kaiming_uniform_(self.lora_a, a=math.sqrt(5))

        if config.freeze_base:
            for parameter in self.base.parameters():
                parameter.requires_grad = False
        self.lora_a.requires_grad = config.enabled
        self.lora_b.requires_grad = config.enabled

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        result = self.base(x)
        if not self.config.enabled or self.merged:
            return result
        adapter = F.linear(F.linear(x, self.lora_a), self.lora_b) * self.scaling
        return result + adapter

    def merge(self) -> None:
        if not self.config.enabled:
            raise RuntimeError("cannot merge a disabled LoRA adapter")
        if self.merged:
            raise RuntimeError("LoRA adapter is already merged")
        delta = torch.matmul(self.lora_b, self.lora_a) * self.scaling
        with torch.no_grad():
            self.base.weight.add_(delta.to(self.base.weight.dtype))
        self.merged = True

    def unmerge(self) -> None:
        if not self.merged:
            raise RuntimeError("LoRA adapter is not merged")
        delta = torch.matmul(self.lora_b, self.lora_a) * self.scaling
        with torch.no_grad():
            self.base.weight.sub_(delta.to(self.base.weight.dtype))
        self.merged = False


def adapter_state_dict(modules: nn.Module | Mapping[str, nn.Module]) -> dict[str, torch.Tensor]:
    if isinstance(modules, Mapping):
        named_modules = modules.items()
    else:
        named_modules = modules.named_modules()

    state = {}
    for prefix, module in named_modules:
        if isinstance(module, LoRALinear):
            stem = f"{prefix}." if prefix else ""
            state[f"{stem}lora_a"] = module.lora_a.detach().clone()
            state[f"{stem}lora_b"] = module.lora_b.detach().clone()
    return state
