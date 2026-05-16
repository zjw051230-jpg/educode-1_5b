# draft_status: candidate
# topic_id: COD-016
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC-6
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only

"""Summary data dict pattern for a small synthetic run report."""


def build_run_summary(step: int, train_loss: float, val_loss: float) -> dict[str, object]:
    summary = {
        "step": step,
        "train_loss": round(train_loss, 4),
        "val_loss": round(val_loss, 4),
        "loss_gap": round(val_loss - train_loss, 4),
        "checkpoint_reload_success": True,
    }
    print(summary)
    return summary


if __name__ == "__main__":
    result = build_run_summary(step=50, train_loss=1.2345, val_loss=1.4567)
    assert result["loss_gap"] == 0.2222
