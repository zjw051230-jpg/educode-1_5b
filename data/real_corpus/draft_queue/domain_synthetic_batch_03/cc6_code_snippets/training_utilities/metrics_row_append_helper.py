# draft_status: candidate
# topic_id: COD-017
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC-6
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only

"""Metrics row append helper that prepares JSONL-style line strings."""

import json


def build_metrics_row(step: int, loss: float, tokens_per_sec: float) -> str:
    row = {
        "step": step,
        "loss": round(loss, 4),
        "tokens_per_sec": round(tokens_per_sec, 2),
    }
    encoded = json.dumps(row, ensure_ascii=False)
    print(encoded)
    return encoded


if __name__ == "__main__":
    row = build_metrics_row(step=10, loss=2.3456, tokens_per_sec=1280.55)
    assert '"step": 10' in row
