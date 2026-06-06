from __future__ import annotations

import torch


def repeat_kv_for_gqa(x: torch.Tensor, *, num_query_heads: int) -> torch.Tensor:
    if x.ndim != 4:
        raise ValueError("GQA tensor must have shape [batch, kv_heads, sequence, head_dim]")
    kv_heads = x.shape[1]
    if num_query_heads <= 0:
        raise ValueError("num_query_heads must be positive")
    if num_query_heads % kv_heads != 0:
        raise ValueError("num_query_heads must be divisible by kv_heads")
    repeat_factor = num_query_heads // kv_heads
    if repeat_factor == 1:
        return x
    return x.repeat_interleave(repeat_factor, dim=1)


def validate_qkv_shapes(q: torch.Tensor, k: torch.Tensor, v: torch.Tensor) -> None:
    if q.ndim != 4 or k.ndim != 4 or v.ndim != 4:
        raise ValueError("q, k, and v must have shape [batch, heads, sequence, head_dim]")
    if k.shape != v.shape:
        raise ValueError("k and v must have matching shapes")
    if q.shape[0] != k.shape[0] or q.shape[2] != k.shape[2] or q.shape[3] != k.shape[3]:
        raise ValueError("q and k/v must match batch, sequence, and head_dim")
