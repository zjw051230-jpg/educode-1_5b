# draft_status: candidate
# topic_id: COD-004
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC-6
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only

"""Single-batch forward and backward example with a tiny module."""

import torch
from torch import nn


class TinyProjector(nn.Module):
    def __init__(self, in_features: int = 4, out_features: int = 3) -> None:
        super().__init__()
        self.linear = nn.Linear(in_features, out_features)

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        return self.linear(inputs)


def run_single_batch_step() -> float:
    model = TinyProjector()
    inputs = torch.randn(2, 4)
    targets = torch.tensor([1, 0])

    logits = model(inputs)
    loss = nn.CrossEntropyLoss()(logits, targets)
    loss.backward()

    grad_found = any(parameter.grad is not None for parameter in model.parameters())
    print(f"logits shape: {tuple(logits.shape)}")
    print(f"loss: {loss.item():.4f}")
    assert grad_found
    return float(loss.item())


if __name__ == "__main__":
    run_single_batch_step()
