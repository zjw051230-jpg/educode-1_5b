# draft_status: candidate
# topic_id: COD-001
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC-6
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only

"""Minimal tensor shape print example for educational review."""

import torch


def describe_batch_shapes(batch_size: int = 2, seq_len: int = 4, hidden_size: int = 8) -> dict[str, tuple[int, ...]]:
    token_ids = torch.arange(batch_size * seq_len).view(batch_size, seq_len)
    hidden_states = torch.randn(batch_size, seq_len, hidden_size)

    shape_map = {
        "token_ids": tuple(token_ids.shape),
        "hidden_states": tuple(hidden_states.shape),
    }

    for name, shape in shape_map.items():
        print(f"{name}: {shape}")

    return shape_map


def main() -> None:
    shapes = describe_batch_shapes()
    assert shapes["token_ids"] == (2, 4)
    assert shapes["hidden_states"] == (2, 4, 8)
    print("shape check passed")


if __name__ == "__main__":
    main()
