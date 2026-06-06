from __future__ import annotations

from collections.abc import Iterable

from torch import nn

from src.educode.lora import LoRAConfig, LoRALinear


def select_lora_targets(model: nn.Module, target_suffixes: Iterable[str] | None = None) -> list[str]:
    suffixes = tuple(target_suffixes or ())
    targets = []
    for name, module in model.named_modules():
        if not name or not isinstance(module, nn.Linear):
            continue
        if suffixes and not name.endswith(suffixes):
            continue
        targets.append(name)
    return targets


def wrap_linear_with_lora(base: nn.Linear, config: LoRAConfig) -> LoRALinear:
    return LoRALinear(base, config)
