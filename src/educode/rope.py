from __future__ import annotations

from dataclasses import dataclass

import torch


@dataclass(frozen=True)
class RoPECache:
    cos: torch.Tensor
    sin: torch.Tensor


def rotate_half(x: torch.Tensor) -> torch.Tensor:
    if x.shape[-1] % 2 != 0:
        raise ValueError("head_dim must be even for RoPE")
    even = x[..., ::2]
    odd = x[..., 1::2]
    return torch.stack((-odd, even), dim=-1).flatten(start_dim=-2)


def build_rope_cache(
    seq_len: int,
    head_dim: int,
    *,
    theta: float = 10000.0,
    scaling_factor: float = 1.0,
    device: torch.device | None = None,
    dtype: torch.dtype = torch.float32,
) -> RoPECache:
    if seq_len <= 0:
        raise ValueError("seq_len must be positive")
    if head_dim <= 0 or head_dim % 2 != 0:
        raise ValueError("head_dim must be a positive even integer")
    if theta <= 0:
        raise ValueError("theta must be positive")
    if scaling_factor <= 0:
        raise ValueError("scaling_factor must be positive")
    positions = torch.arange(seq_len, device=device, dtype=torch.float32) / float(scaling_factor)
    dims = torch.arange(0, head_dim, 2, device=device, dtype=torch.float32)
    inv_freq = 1.0 / (theta ** (dims / head_dim))
    angles = torch.outer(positions, inv_freq)
    return RoPECache(cos=angles.cos().to(dtype=dtype), sin=angles.sin().to(dtype=dtype))


def apply_rotary_emb(q: torch.Tensor, k: torch.Tensor, cache: RoPECache) -> tuple[torch.Tensor, torch.Tensor]:
    if q.shape != k.shape:
        raise ValueError("q and k must have matching shapes")
    if q.ndim != 4:
        raise ValueError("q and k must have shape [batch, heads, sequence, head_dim]")
    seq_len = q.shape[-2]
    head_dim = q.shape[-1]
    if cache.cos.shape[0] < seq_len or cache.cos.shape[1] * 2 != head_dim:
        raise ValueError("RoPE cache shape does not match q/k")
    cos = cache.cos[:seq_len].repeat_interleave(2, dim=-1)
    sin = cache.sin[:seq_len].repeat_interleave(2, dim=-1)
    while cos.ndim < q.ndim:
        cos = cos.unsqueeze(0)
        sin = sin.unsqueeze(0)
    cos = cos.to(device=q.device, dtype=q.dtype)
    sin = sin.to(device=q.device, dtype=q.dtype)
    return (q * cos) + (rotate_half(q) * sin), (k * cos) + (rotate_half(k) * sin)
