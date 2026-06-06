from __future__ import annotations

import torch
from torch.nn import functional as F


def validate_sampling_args(temperature: float = 1.0, top_k: int | None = None, top_p: float | None = None) -> None:
    if temperature <= 0:
        raise ValueError("temperature must be greater than 0")
    if top_k is not None and top_k <= 0:
        raise ValueError("top_k must be positive when provided")
    if top_p is not None and not 0 < top_p <= 1:
        raise ValueError("top_p must be in (0, 1]")


def greedy_token(logits: torch.Tensor) -> torch.Tensor:
    if logits.ndim != 1:
        raise ValueError("logits must have shape [vocab_size]")
    return torch.argmax(logits, dim=-1)


def filter_top_k(logits: torch.Tensor, top_k: int | None) -> torch.Tensor:
    if top_k is None:
        return logits
    if top_k <= 0:
        raise ValueError("top_k must be positive")
    k = min(top_k, logits.shape[-1])
    values, _ = torch.topk(logits, k=k)
    threshold = values[..., -1, None]
    return torch.where(logits < threshold, torch.full_like(logits, float("-inf")), logits)


def filter_top_p(logits: torch.Tensor, top_p: float | None) -> torch.Tensor:
    if top_p is None or top_p >= 1:
        return logits
    if top_p <= 0:
        raise ValueError("top_p must be in (0, 1]")
    sorted_logits, sorted_indices = torch.sort(logits, descending=True)
    sorted_probs = F.softmax(sorted_logits, dim=-1)
    cumulative = torch.cumsum(sorted_probs, dim=-1)
    remove = cumulative > top_p
    remove[..., 1:] = remove[..., :-1].clone()
    remove[..., 0] = False
    filtered_sorted = sorted_logits.masked_fill(remove, float("-inf"))
    filtered = torch.full_like(logits, float("-inf"))
    return filtered.scatter(dim=-1, index=sorted_indices, src=filtered_sorted)


def sample_token(
    logits: torch.Tensor,
    *,
    temperature: float = 1.0,
    top_k: int | None = None,
    top_p: float | None = None,
    generator: torch.Generator | None = None,
) -> torch.Tensor:
    if logits.ndim != 1:
        raise ValueError("logits must have shape [vocab_size]")
    validate_sampling_args(temperature=temperature, top_k=top_k, top_p=top_p)
    filtered = filter_top_p(filter_top_k(logits / temperature, top_k), top_p)
    probs = F.softmax(filtered, dim=-1)
    if not torch.isfinite(probs).all() or float(probs.sum().item()) <= 0:
        raise ValueError("sampling probabilities are invalid")
    return torch.multinomial(probs, num_samples=1, generator=generator).squeeze(0)
