# draft_status: candidate
# topic_id: COD-006
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC-6
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only

"""Tiny optimizer step example with before and after parameter snapshots."""

import torch
from torch import nn


def run_optimizer_step() -> tuple[float, float]:
    model = nn.Linear(2, 1)
    optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
    inputs = torch.tensor([[1.0, 2.0], [0.0, 1.0]])
    targets = torch.tensor([[1.0], [0.0]])

    before = model.weight.detach().clone()
    predictions = model(inputs)
    loss = nn.MSELoss()(predictions, targets)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    after = model.weight.detach().clone()
    weight_change = torch.abs(after - before).sum().item()
    print(f"loss: {loss.item():.4f}")
    print(f"weight change: {weight_change:.4f}")
    return loss.item(), weight_change


if __name__ == "__main__":
    loss_value, delta = run_optimizer_step()
    assert loss_value >= 0.0
    assert delta > 0.0
