# draft_status: candidate
# topic_id: PDS-002
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC2
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only

from typing import Any

REQUIRED_FIELDS = {"id", "text", "source_category", "language"}


def validate_processed_record(record: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    missing = sorted(REQUIRED_FIELDS - record.keys())
    if missing:
        issues.append(f"missing fields: {', '.join(missing)}")
    if not isinstance(record.get("id"), str) or not record.get("id"):
        issues.append("id must be a non-empty string")
    if not isinstance(record.get("text"), str) or not record.get("text", "").strip():
        issues.append("text must be a non-empty string")
    if record.get("language") not in {"en", "zh", "mixed"}:
        issues.append("language must be en, zh, or mixed")
    source = record.get("source_category")
    if source not in {"synthetic_examples", "synthetic_notes"}:
        issues.append("source_category is outside the draft schema")
    return issues


def main() -> None:
    sample = {
        "id": "draft-001",
        "text": "Token batching keeps shapes predictable.",
        "source_category": "synthetic_examples",
        "language": "en",
    }
    print(validate_processed_record(sample))


if __name__ == "__main__":
    main()
