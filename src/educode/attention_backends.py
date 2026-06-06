from __future__ import annotations

import importlib.util
import math
from dataclasses import dataclass

import torch
from torch.nn import functional as F

from educode.attention_utils import repeat_kv_for_gqa, validate_qkv_shapes

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
    backend = name.strip().lower()
    if backend not in SUPPORTED_ATTENTION_BACKENDS:
        allowed = ", ".join(SUPPORTED_ATTENTION_BACKENDS)
        raise ValueError(f"unsupported attention backend {name!r}; expected one of: {allowed}")
    return backend


def flash_attention_2_availability() -> BackendAvailability:
    if importlib.util.find_spec("flash_attn") is None:
        return BackendAvailability("flash_attention_2", False, "flash_attn package is not installed")
    return BackendAvailability("flash_attention_2", True, "flash_attn import spec is available")


def backend_availability(name: str) -> BackendAvailability:
    backend = normalize_attention_backend(name)
    if backend == "flash_attention_2":
        return flash_attention_2_availability()
    return BackendAvailability(backend, True, "available in PyTorch/local implementation")


def naive_causal_attention(
    q: torch.Tensor,
    k: torch.Tensor,
    v: torch.Tensor,
    *,
    dropout_p: float = 0.0,
    training: bool = False,
) -> torch.Tensor:
    validate_qkv_shapes(q, k, v)
    if q.shape[1] != k.shape[1]:
        k = repeat_kv_for_gqa(k, num_query_heads=q.shape[1])
        v = repeat_kv_for_gqa(v, num_query_heads=q.shape[1])
    scale = 1.0 / math.sqrt(q.shape[-1])
    scores = torch.matmul(q, k.transpose(-2, -1)) * scale
    seq_len = q.shape[-2]
    mask = torch.ones(seq_len, seq_len, dtype=torch.bool, device=q.device).tril()
    scores = scores.masked_fill(~mask, float("-inf"))
    weights = torch.softmax(scores, dim=-1)
    if dropout_p > 0 and training:
        weights = F.dropout(weights, p=dropout_p, training=True)
    return torch.matmul(weights, v)


def sdpa_causal_attention(
    q: torch.Tensor,
    k: torch.Tensor,
    v: torch.Tensor,
    *,
    dropout_p: float = 0.0,
    training: bool = False,
) -> torch.Tensor:
    validate_qkv_shapes(q, k, v)
    if q.shape[1] != k.shape[1]:
        k = repeat_kv_for_gqa(k, num_query_heads=q.shape[1])
        v = repeat_kv_for_gqa(v, num_query_heads=q.shape[1])
    return F.scaled_dot_product_attention(q, k, v, dropout_p=dropout_p if training else 0.0, is_causal=True)


def flash_attention_2_causal_attention(
    q: torch.Tensor,
    k: torch.Tensor,
    v: torch.Tensor,
    *,
    dropout_p: float = 0.0,
    training: bool = False,
) -> torch.Tensor:
    availability = flash_attention_2_availability()
    if not availability.available:
        raise RuntimeError(f"flash_attention_2 unavailable: {availability.reason}")
    try:
        from flash_attn import flash_attn_func
    except Exception as exc:  # pragma: no cover - optional dependency
        raise RuntimeError(f"flash_attention_2 import failed: {exc}") from exc
    validate_qkv_shapes(q, k, v)
    if q.shape[1] != k.shape[1]:
        k = repeat_kv_for_gqa(k, num_query_heads=q.shape[1])
        v = repeat_kv_for_gqa(v, num_query_heads=q.shape[1])
    output = flash_attn_func(
        q.transpose(1, 2).contiguous(),
        k.transpose(1, 2).contiguous(),
        v.transpose(1, 2).contiguous(),
        dropout_p=dropout_p if training else 0.0,
        causal=True,
    )
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
    backend = normalize_attention_backend(backend)
    if backend == "sdpa":
        return sdpa_causal_attention(q, k, v, dropout_p=dropout_p, training=training)
    if backend == "naive":
        return naive_causal_attention(q, k, v, dropout_p=dropout_p, training=training)
    return flash_attention_2_causal_attention(q, k, v, dropout_p=dropout_p, training=training)
