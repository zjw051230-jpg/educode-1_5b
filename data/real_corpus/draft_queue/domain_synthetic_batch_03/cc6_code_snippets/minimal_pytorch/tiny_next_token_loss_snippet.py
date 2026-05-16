# draft_status: candidate
# topic_id: COD-002
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC-6
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only

"""Tiny next-token loss snippet using small synthetic tensors."""

import torch
import torch.nn.functional as F


def compute_tiny_next_token_loss() -> torch.Tensor:
    logits = torch.tensor(
        [
            [[2.0, 0.5, -1.0], [0.1, 1.5, 0.0]],
            [[-0.2, 0.3, 1.8], [1.2, -0.7, 0.4]],
        ],
        dtype=torch.float32,
    )
    targets = torch.tensor([[0, 1], [2, 0]], dtype=torch.long)

    flat_logits = logits.view(-1, logits.size(-1))
    flat_targets = targets.view(-1)
    loss = F.cross_entropy(flat_logits, flat_targets)

    print(f"logits shape: {tuple(logits.shape)}")
    print(f"targets shape: {tuple(targets.shape)}")
    print(f"loss: {loss.item():.4f}")
    return loss


if __name__ == "__main__":
    result = compute_tiny_next_token_loss()
    assert torch.isfinite(result)
