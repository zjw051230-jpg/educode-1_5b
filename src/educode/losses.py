from __future__ import annotations

import torch
from torch.nn import functional as F


def next_token_cross_entropy(logits: torch.Tensor, target_ids: torch.Tensor) -> torch.Tensor:
    if not isinstance(logits, torch.Tensor):
        raise TypeError("logits must be a torch.Tensor")
    if not isinstance(target_ids, torch.Tensor):
        raise TypeError("target_ids must be a torch.Tensor")
    if logits.ndim != 3:
        raise ValueError("logits must have shape [B, T, V]")
    if target_ids.ndim != 2:
        raise ValueError("target_ids must have shape [B, T]")
    if target_ids.dtype != torch.long:
        raise TypeError("target_ids must have dtype torch.long")
    if logits.shape[0] != target_ids.shape[0] or logits.shape[1] != target_ids.shape[1]:
        raise ValueError("logits and target_ids must have matching batch and sequence dimensions")

    batch_size, sequence_length, vocab_size = logits.shape
    flat_logits = logits.reshape(batch_size * sequence_length, vocab_size)
    flat_targets = target_ids.reshape(batch_size * sequence_length)
    return F.cross_entropy(flat_logits, flat_targets)
