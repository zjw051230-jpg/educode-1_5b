from __future__ import annotations

from dataclasses import dataclass, field

import torch


@dataclass
class LayerKV:
    key: torch.Tensor | None = None
    value: torch.Tensor | None = None


@dataclass
class KVCache:
    num_layers: int
    layers: list[LayerKV] = field(init=False)

    def __post_init__(self) -> None:
        if self.num_layers <= 0:
            raise ValueError("num_layers must be positive")
        self.layers = [LayerKV() for _ in range(self.num_layers)]

    def append(self, layer_idx: int, key: torch.Tensor, value: torch.Tensor) -> None:
        layer = self.layers[layer_idx]
        if key.shape != value.shape:
            raise ValueError("key and value must have matching shapes")
        if key.ndim != 4:
            raise ValueError("key/value must have shape [batch, heads, sequence, head_dim]")
        if layer.key is None:
            layer.key = key.clone()
            layer.value = value.clone()
            return
        layer.key = torch.cat([layer.key, key], dim=2)
        layer.value = torch.cat([layer.value, value], dim=2)

    def read(self, layer_idx: int) -> tuple[torch.Tensor | None, torch.Tensor | None]:
        layer = self.layers[layer_idx]
        return layer.key, layer.value

    def reset(self) -> None:
        for layer in self.layers:
            layer.key = None
            layer.value = None

    def sequence_length(self, layer_idx: int = 0) -> int:
        key = self.layers[layer_idx].key
        return 0 if key is None else int(key.shape[2])
