# draft_status: candidate
# topic_id: BIL-014
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC5
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only

from typing import Dict, Iterable, List


def summarize_bilingual_losses(step_rows: Iterable[Dict[str, float]]) -> Dict[str, float]:
    rows = list(step_rows)
    if not rows:
        return {"steps": 0, "train_loss_mean": 0.0, "val_loss_mean": 0.0}

    train_losses: List[float] = [row["train_loss"] for row in rows]
    val_losses: List[float] = [row["val_loss"] for row in rows]
    zh_share: List[float] = [row.get("zh_share", 0.0) for row in rows]

    return {
        "steps": float(len(rows)),
        "train_loss_mean": sum(train_losses) / len(train_losses),
        "val_loss_mean": sum(val_losses) / len(val_losses),
        "avg_zh_share": sum(zh_share) / len(zh_share),
    }


if __name__ == "__main__":
    demo_rows = [
        {"step": 1, "train_loss": 3.2, "val_loss": 3.4, "zh_share": 0.50},
        {"step": 2, "train_loss": 3.0, "val_loss": 3.3, "zh_share": 0.75},
        {"step": 3, "train_loss": 2.9, "val_loss": 3.1, "zh_share": 0.25},
    ]
    print(summarize_bilingual_losses(demo_rows))

# Educational notes:
# - Logging language-share next to losses can help explain why two nearby steps behave differently.
# - The helper avoids external dependencies and stays suitable for draft review snippets.
# - The values are synthetic and are not tied to a real training run.
