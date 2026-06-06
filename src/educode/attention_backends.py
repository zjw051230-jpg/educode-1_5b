from __future__ import annotations

import importlib.util
import math
from dataclasses import dataclass

import torch
from torch.nn import functional as F

SUPPORTED_ATTENTION_BACKENDS = ("sdpa", "naive", "flash_attention_2")
DEFAULT_ATTENTION_BACKEND = "sdpa"


@dataclass(frozen=True)
class BackendAvailability:
    backend: str
    available: bool
    reason: str


def normalize_attention_backend(name: str) -> str:
    if not isinstance(name, str) or not name.strip():
        raise ValueError("attention backend must be a non-empty string")
    normalized = name.strip().lower()
    if normalized not in SUPPORTED_ATTENTION_BACKENDS:
        allowed = ", ".join(SUPPORTED_ATTENTION_BACKENDS)
        raise ValueError(f"unsupported attention backend {name!r}; expected one of: {allowed}")
    return normalized


def flash_attention_2_availability() -> BackendAvailability:
    if importlib.util.find_spec("flash_attn") is None:
        return BackendAvailability(
            backend="flash_attention_2",
            available=False,
            reason="flash_attn package is not installed",
        )
    return BackendAvailability(
        backend="flash_attention_2",
        available=True,
        reason="flash_attn package import spec is available",
    )


def backend_availability(name: str) -> BackendAvailability:
    backend = normalize_attention_backend(name)
    if backend == "flash_attention_2":
        return flash_attention_2_availability()
    return BackendAvailability(backend=backend, available=True, reason="available in PyTorch")


def _naive_causal_attention(
    q: torch.Tensor,
    k: torch.Tensor,
    v: torch.Tensor,
    *,
    dropout_p: float = 0.0,
    training: bool = False,
) -> torch.Tensor:
    scale = 1.0 / math.sqrt(q.size(-1))
    scores = torch.matmul(q, k.transpose(-2, -1)) * scale
    seq_len = q.size(-2)
    causal_mask = torch.ones(seq_len, seq_len, dtype=torch.bool, device=q.device).tril()
    scores = scores.masked_fill(~causal_mask, float("-inf"))
    weights = torch.softmax(scores, dim=-1)
    if dropout_p > 0.0 and training:
        weights = F.dropout(weights, p=dropout_p, training=True)
    return torch.matmul(weights, v)


def _flash_attention_2_causal_attention(
    q: torch.Tensor,
    k: torch.Tensor,
    v: torch.Tensor,
    *,
    dropout_p: float = 0.0,
) -> torch.Tensor:
    availability = flash_attention_2_availability()
    if not availability.available:
        raise RuntimeError(f"flash_attention_2 unavailable: {availability.reason}")

    try:
        from flash_attn import flash_attn_func
    except Exception as exc:  # pragma: no cover - depends on optional external package
        raise RuntimeError(f"flash_attention_2 import failed: {exc}") from exc

    q_t = q.transpose(1, 2).contiguous()
    k_t = k.transpose(1, 2).contiguous()
    v_t = v.transpose(1, 2).contiguous()
    output = flash_attn_func(q_t, k_t, v_t, dropout_p=dropout_p, causal=True)
    return output.transpose(1, 2).contiguous()


def causal_attention(
    q: torch.Tensor,
    k: torch.Tensor,
    v: torch.Tensor,
    *,
    backend: str = DEFAULT_ATTENTION_BACKEND,
    dropout_p: float = 0.0,
    training: bool = False,
) -> torch.Tensor:
    normalized_backend = normalize_attention_backend(backend)
    if normalized_backend == "sdpa":
        return F.scaled_dot_product_attention(
            q,
            k,
            v,
            dropout_p=dropout_p if training else 0.0,
            is_causal=True,
        )
    if normalized_backend == "naive":
        return _naive_causal_attention(q, k, v, dropout_p=dropout_p, training=training)
    return _flash_attention_2_causal_attention(
        q,
        k,
        v,
        dropout_p=dropout_p if training else 0.0,
    )
