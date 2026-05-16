# draft_status: candidate
# topic_id: COD-005
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC-6
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only

"""Device move sanity check using CPU-safe fallback logic."""

import torch


def move_batch_to_device(batch: dict[str, torch.Tensor], device: torch.device) -> dict[str, torch.Tensor]:
    return {name: tensor.to(device) for name, tensor in batch.items()}


def main() -> None:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    batch = {
        "input_ids": torch.tensor([[1, 2, 3], [4, 5, 6]]),
        "targets": torch.tensor([[2, 3, 4], [5, 6, 7]]),
    }

    moved = move_batch_to_device(batch, device)
    for name, tensor in moved.items():
        print(f"{name}: {tensor.device} {tuple(tensor.shape)}")
        assert tensor.device.type == device.type


if __name__ == "__main__":
    main()
