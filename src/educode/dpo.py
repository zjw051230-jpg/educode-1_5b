from __future__ import annotations

import torch
from torch.nn import functional as F


def dpo_loss(
    policy_chosen_logps: torch.Tensor,
    policy_rejected_logps: torch.Tensor,
    reference_chosen_logps: torch.Tensor,
    reference_rejected_logps: torch.Tensor,
    beta: float = 0.1,
) -> torch.Tensor:
    if beta <= 0:
        raise ValueError("beta must be positive")
    shapes = {
        tuple(policy_chosen_logps.shape),
        tuple(policy_rejected_logps.shape),
        tuple(reference_chosen_logps.shape),
        tuple(reference_rejected_logps.shape),
    }
    if len(shapes) != 1:
        raise ValueError("all logprob tensors must have the same shape")
    policy_margin = policy_chosen_logps - policy_rejected_logps
    reference_margin = reference_chosen_logps - reference_rejected_logps
    logits = beta * (policy_margin - reference_margin)
    return -F.logsigmoid(logits).mean()
