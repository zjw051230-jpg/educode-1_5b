# draft_status: candidate
# topic_id: COD-007
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC-6
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only

"""Gradient norm print helper for a tiny educational model."""

import math

import torch
from torch import nn


def compute_grad_norm(model: nn.Module) -> float:
    squared_total = 0.0
    for parameter in model.parameters():
        if parameter.grad is None:
            continue
        squared_total += parameter.grad.norm().item() ** 2
    return math.sqrt(squared_total)


def main() -> None:
    model = nn.Linear(3, 2)
    inputs = torch.randn(2, 3)
    targets = torch.tensor([0, 1])

    loss = nn.CrossEntropyLoss()(model(inputs), targets)
    loss.backward()

    grad_norm = compute_grad_norm(model)
    print(f"grad_norm: {grad_norm:.4f}")
    assert grad_norm > 0.0


if __name__ == "__main__":
    main()
