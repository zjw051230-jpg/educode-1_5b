from __future__ import annotations

from dataclasses import dataclass
from importlib.util import find_spec

import torch
from torch.nn import functional as F


SUPPORTED_ATTENTION_BACKENDS = ("sdpa", "naive", "flash_attention_2")


@dataclass(frozen=True)
class AttentionBackendAvailability:
    name: str
    supported_by_config: bool
    available: bool
    reason: str


def normalize_attention_backend(name: str) -> str:
    if not isinstance(name, str):
        raise TypeError("attention backend name must be a string")
    normalized = name.strip().lower()
    if normalized not in SUPPORTED_ATTENTION_BACKENDS:
        raise ValueError(f"attention_backend must be one of: {', '.join(SUPPORTED_ATTENTION_BACKENDS)}")
    return normalized


def attention_backend_availability(name: str) -> AttentionBackendAvailability:
    backend = normalize_attention_backend(name)
    if backend in {"sdpa", "naive"}:
        return AttentionBackendAvailability(
            name=backend,
            supported_by_config=True,
            available=True,
            reason="available in the local PyTorch CPU/GPU runtime",
        )
    flash_installed = find_spec("flash_attn") is not None
    return AttentionBackendAvailability(
        name=backend,
        supported_by_config=True,
        available=flash_installed,
        reason="flash_attn import is available" if flash_installed else "flash_attn package is not installed",
    )


def _naive_causal_attention(
    q: torch.Tensor,
    k: torch.Tensor,
    v: torch.Tensor,
    *,
    dropout_p: float,
    training: bool,
) -> torch.Tensor:
    if q.ndim != 4 or k.ndim != 4 or v.ndim != 4:
        raise ValueError("q, k, and v must have shape [batch, heads, seq, head_dim]")
    if q.shape != k.shape or q.shape != v.shape:
        raise ValueError("q, k, and v must have matching shapes")
    seq_len = q.shape[-2]
    scale = q.shape[-1] ** -0.5
    scores = torch.matmul(q, k.transpose(-2, -1)) * scale
    mask = torch.ones(seq_len, seq_len, dtype=torch.bool, device=q.device).tril()
    scores = scores.masked_fill(~mask, float("-inf"))
    weights = torch.softmax(scores.float(), dim=-1).to(dtype=v.dtype)
    if dropout_p and training:
        weights = F.dropout(weights, p=dropout_p, training=True)
    return torch.matmul(weights, v)


def causal_attention(
    q: torch.Tensor,
    k: torch.Tensor,
    v: torch.Tensor,
    *,
    backend: str,
    dropout_p: float,
    training: bool,
) -> torch.Tensor:
    selected = normalize_attention_backend(backend)
    if selected == "sdpa":
        return F.scaled_dot_product_attention(
            q,
            k,
            v,
            dropout_p=dropout_p if training else 0.0,
            is_causal=True,
        )
    if selected == "naive":
        return _naive_causal_attention(q, k, v, dropout_p=dropout_p, training=training)

    availability = attention_backend_availability(selected)
    if not availability.available:
        raise RuntimeError(
            "flash_attention_2 backend is unavailable because flash_attn is not installed; "
            "this branch only adds the feasibility guard and does not install FlashAttention"
        )
    raise RuntimeError(
        "flash_attention_2 backend is detected but not wired into TinyDecoderOnlyTransformer yet; "
        "run a dedicated feasibility implementation before enabling it"
    )
