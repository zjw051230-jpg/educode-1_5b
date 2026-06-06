from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import Mapping

import torch
from torch import nn
from torch.nn import functional as F


@dataclass(frozen=True)
class LoRAConfig:
    rank: int = 8
    alpha: float = 16.0
    dropout: float = 0.0
    enabled: bool = False
    freeze_base: bool = True

    def __post_init__(self) -> None:
        if self.rank <= 0:
            raise ValueError("rank must be positive")
        if self.alpha <= 0:
            raise ValueError("alpha must be positive")
        if not 0.0 <= self.dropout < 1.0:
            raise ValueError("dropout must be in [0, 1)")

    def to_dict(self) -> dict:
        return asdict(self)


class LoRALinear(nn.Module):
    def __init__(self, base: nn.Linear, config: LoRAConfig) -> None:
        super().__init__()
        if not isinstance(base, nn.Linear):
            raise TypeError("base must be torch.nn.Linear")
        self.base = base
        self.config = config
        self.scaling = config.alpha / config.rank
        self.dropout = nn.Dropout(config.dropout)
        self.merged = False
        self.lora_a = nn.Parameter(torch.empty(config.rank, base.in_features))
        self.lora_b = nn.Parameter(torch.zeros(base.out_features, config.rank))
        nn.init.kaiming_uniform_(self.lora_a, a=math.sqrt(5))

        if config.freeze_base:
            for parameter in self.base.parameters():
                parameter.requires_grad = False
        self.lora_a.requires_grad = config.enabled
        self.lora_b.requires_grad = config.enabled

    def _delta_weight(self) -> torch.Tensor:
        return torch.matmul(self.lora_b, self.lora_a) * self.scaling

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        result = self.base(x)
        if not self.config.enabled or self.merged:
            return result
        adapter = F.linear(F.linear(self.dropout(x), self.lora_a), self.lora_b)
        return result + adapter * self.scaling

    def merge(self) -> None:
        if not self.config.enabled:
            raise RuntimeError("cannot merge disabled LoRA adapter")
        if self.merged:
            raise RuntimeError("LoRA adapter already merged")
        with torch.no_grad():
            self.base.weight.add_(self._delta_weight().to(self.base.weight.dtype))
        self.merged = True

    def unmerge(self) -> None:
        if not self.merged:
            raise RuntimeError("LoRA adapter is not merged")
        with torch.no_grad():
            self.base.weight.sub_(self._delta_weight().to(self.base.weight.dtype))
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


def count_trainable_parameters(module: nn.Module) -> dict:
    trainable = [(name, parameter.numel()) for name, parameter in module.named_parameters() if parameter.requires_grad]
    return {
        "trainable_parameter_count": sum(count for _, count in trainable),
        "trainable_names": [name for name, _ in trainable],
    }
