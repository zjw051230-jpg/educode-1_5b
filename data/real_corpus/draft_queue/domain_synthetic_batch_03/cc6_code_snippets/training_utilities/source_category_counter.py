# draft_status: candidate
# topic_id: COD-015
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC-6
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only

"""Source category counter for tiny synthetic record lists."""

from collections import Counter


def count_source_categories(records: list[dict[str, str]]) -> dict[str, int]:
    counts = Counter(record["source_category"] for record in records)
    print(dict(counts))
    return dict(counts)


if __name__ == "__main__":
    rows = [
        {"source_category": "synthetic_examples"},
        {"source_category": "synthetic_examples"},
        {"source_category": "draft_notes"},
    ]
    summary = count_source_categories(rows)
    assert summary["synthetic_examples"] == 2
