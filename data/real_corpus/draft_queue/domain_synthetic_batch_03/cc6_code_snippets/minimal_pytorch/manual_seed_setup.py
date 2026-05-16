# draft_status: candidate
# topic_id: COD-003
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC-6
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only

"""Manual seed setup example for deterministic toy tensors."""

import random

import torch


def build_seeded_preview(seed: int = 7) -> dict[str, list[float]]:
    random.seed(seed)
    torch.manual_seed(seed)

    weights = torch.randn(3)
    python_values = [round(random.random(), 4) for _ in range(3)]
    torch_values = [round(value, 4) for value in weights.tolist()]

    preview = {
        "python_random": python_values,
        "torch_random": torch_values,
    }

    print(preview)
    return preview


if __name__ == "__main__":
    first = build_seeded_preview()
    second = build_seeded_preview()
    assert first == second
