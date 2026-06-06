from __future__ import annotations

from collections.abc import Iterable

from torch import nn

from src.educode.lora import LoRAConfig, LoRALinear


def find_target_linear_modules(
    model: nn.Module, target_names: Iterable[str] | None = None
) -> list[str]:
    suffixes = tuple(target_names or ())
    targets = []
    for name, module in model.named_modules():
        if not name or not isinstance(module, nn.Linear):
            continue
        if suffixes and not name.endswith(suffixes):
            continue
        targets.append(name)
    return targets


def apply_lora_to_linear_module(base: nn.Linear, config: LoRAConfig) -> LoRALinear:
    return LoRALinear(base, config)
