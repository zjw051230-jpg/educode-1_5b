# draft_status: candidate
# topic_id: MLF-005
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC-1
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only

"""Minimal train/validation loss logging fields for tiny educational runs."""


def build_loss_row(step, split, loss, learning_rate, batch_size, token_count, seq_len):
    return {
        "step": int(step),
        "split": split,
        "loss": float(loss),
        "learning_rate": float(learning_rate),
        "batch_size": int(batch_size),
        "token_count": int(token_count),
        "sequence_length": int(seq_len),
    }


def preview_rows():
    train_row = build_loss_row(
        step=12,
        split="train",
        loss=3.42,
        learning_rate=3e-4,
        batch_size=8,
        token_count=1024,
        seq_len=128,
    )
    val_row = build_loss_row(
        step=12,
        split="val",
        loss=3.67,
        learning_rate=3e-4,
        batch_size=8,
        token_count=768,
        seq_len=128,
    )
    return [train_row, val_row]


if __name__ == "__main__":
    for row in preview_rows():
        print(row)
