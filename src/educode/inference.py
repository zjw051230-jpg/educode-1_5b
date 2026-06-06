from __future__ import annotations

import torch

from educode.kv_cache import KVCache


def prefill(model, input_ids: torch.Tensor, cache: KVCache | None = None) -> tuple[torch.Tensor, KVCache | None]:
    if input_ids.ndim != 2:
        raise ValueError("input_ids must have shape [batch, sequence]")
    model.eval()
    with torch.no_grad():
        logits = model(input_ids)
    return logits, cache


def decode_one(model, input_ids: torch.Tensor, cache: KVCache | None = None) -> tuple[torch.Tensor, KVCache | None]:
    if input_ids.ndim != 2 or input_ids.shape[1] != 1:
        raise ValueError("decode input_ids must have shape [batch, 1]")
    model.eval()
    with torch.no_grad():
        logits = model(input_ids)
    return logits[:, -1:, :], cache
