# draft_status: candidate
# topic_id: COD-018
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC-6
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only

"""Validation loss helper using averaged synthetic batch losses."""


def average_validation_loss(loss_values: list[float]) -> float:
    if not loss_values:
        raise ValueError("loss_values must not be empty")
    return sum(loss_values) / len(loss_values)


def main() -> None:
    losses = [1.8, 1.6, 1.7]
    average = average_validation_loss(losses)
    print(f"average validation loss: {average:.4f}")
    assert round(average, 4) == 1.7


if __name__ == "__main__":
    main()
