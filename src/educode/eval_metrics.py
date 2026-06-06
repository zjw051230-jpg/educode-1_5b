from __future__ import annotations

import math

import torch
from torch.nn import functional as F


def exact_match_score(prediction: str, target: str, normalize: bool = True) -> float:
    if normalize:
        prediction = prediction.strip().lower()
        target = target.strip().lower()
    return 1.0 if prediction == target else 0.0


def multiple_choice_accuracy(scores: list[float], target_index: int) -> float:
    if not scores:
        raise ValueError("scores must be non-empty")
    if not 0 <= target_index < len(scores):
        raise ValueError("target_index out of range")
    predicted = max(range(len(scores)), key=lambda index: scores[index])
    return 1.0 if predicted == target_index else 0.0


def perplexity_from_logits(logits: torch.Tensor, targets: torch.Tensor) -> float:
    if logits.ndim != 3:
        raise ValueError("logits must have shape [batch, seq, vocab]")
    if targets.shape != logits.shape[:2]:
        raise ValueError("targets must match logits batch and sequence dimensions")
    loss = F.cross_entropy(logits.reshape(-1, logits.shape[-1]), targets.reshape(-1))
    return float(math.exp(float(loss.item())))
