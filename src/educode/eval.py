from __future__ import annotations

import math

import torch

from educode.losses import next_token_cross_entropy


def evaluate_next_token_loss(model, input_ids: torch.Tensor, target_ids: torch.Tensor) -> dict[str, float]:
    model.eval()
    with torch.no_grad():
        logits = model(input_ids)
        loss = next_token_cross_entropy(logits, target_ids)
    loss_value = float(loss.item())
    return {
        "loss": loss_value,
        "perplexity": float(math.exp(loss_value)) if loss_value < 80 else float("inf"),
    }
