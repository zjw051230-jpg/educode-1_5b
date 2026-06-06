from __future__ import annotations

from dataclasses import dataclass

import torch

SUPPORTED_POSITION_ENCODINGS = ("learned", "learned_position_embedding", "rope")
DEFAULT_POSITION_ENCODING = "learned_position_embedding"


def normalize_position_encoding(name: str | None) -> str:
    value = DEFAULT_POSITION_ENCODING if name is None else str(name).strip().lower()
    if value not in SUPPORTED_POSITION_ENCODINGS:
        allowed = ", ".join(SUPPORTED_POSITION_ENCODINGS)
        raise ValueError(f"unsupported position_encoding {name!r}; expected one of: {allowed}")
    return value


@dataclass(frozen=True)
class RoPECache:
    cos: torch.Tensor
    sin: torch.Tensor


def build_rope_cache(
    *,
    seq_len: int,
    head_dim: int,
    theta: float = 10000.0,
    device: torch.device | None = None,
    dtype: torch.dtype = torch.float32,
) -> RoPECache:
    if seq_len <= 0:
        raise ValueError("seq_len must be positive")
    if head_dim <= 0 or head_dim % 2 != 0:
        raise ValueError("head_dim must be a positive even integer")
    if theta <= 0:
        raise ValueError("theta must be positive")

    positions = torch.arange(seq_len, device=device, dtype=torch.float32)
    dims = torch.arange(0, head_dim, 2, device=device, dtype=torch.float32)
    inv_freq = 1.0 / (theta ** (dims / head_dim))
    angles = torch.outer(positions, inv_freq)
    return RoPECache(cos=angles.cos().to(dtype=dtype), sin=angles.sin().to(dtype=dtype))


def rotate_half_pairs(x: torch.Tensor) -> torch.Tensor:
    if x.size(-1) % 2 != 0:
        raise ValueError("last dimension must be even for RoPE")
    x_even = x[..., ::2]
    x_odd = x[..., 1::2]
    rotated = torch.stack((-x_odd, x_even), dim=-1)
    return rotated.flatten(start_dim=-2)


def apply_rope(x: torch.Tensor, cache: RoPECache) -> torch.Tensor:
    if x.ndim < 3:
        raise ValueError("RoPE input must have at least [batch, sequence, head_dim] dimensions")
    seq_len = x.size(-2)
    head_dim = x.size(-1)
    if head_dim % 2 != 0:
        raise ValueError("head_dim must be even")
    if cache.cos.size(0) < seq_len or cache.cos.size(1) * 2 != head_dim:
        raise ValueError("RoPE cache shape does not match input")

    cos = cache.cos[:seq_len].repeat_interleave(2, dim=-1)
    sin = cache.sin[:seq_len].repeat_interleave(2, dim=-1)
    while cos.ndim < x.ndim:
        cos = cos.unsqueeze(0)
        sin = sin.unsqueeze(0)
    cos = cos.to(device=x.device, dtype=x.dtype)
    sin = sin.to(device=x.device, dtype=x.dtype)
    return (x * cos) + (rotate_half_pairs(x) * sin)
