# draft_status: candidate
# topic_id: B04-PDS-0393
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC-2
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only
# batch_id: domain_synthetic_batch_04
from __future__ import annotations

from pathlib import Path
from typing import Iterable

EXAMPLE_LABELS = [
    "seed field parsing",
    "failure diagnosis pattern",
    "Config Validation",
]


def build_demo_rows() -> list[dict[str, object]]:
    return [
        {"topic_id": "B04-PDS-0393", "label": EXAMPLE_LABELS[0], "position": 0},
        {"topic_id": "B04-PDS-0393", "label": EXAMPLE_LABELS[1], "position": 1},
        {"topic_id": "B04-PDS-0393", "label": EXAMPLE_LABELS[2], "position": 2},
    ]


def summarize_seed_field_parsing(rows: Iterable[dict[str, object]]) -> dict[str, object]:
    materialized = list(rows)
    labels = [str(row.get("label", "")) for row in materialized]
    return {
        "topic_id": "B04-PDS-0393",
        "objective": "explaining seed field parsing through a failure diagnosis pattern for config validation",
        "row_count": len(materialized),
        "labels": labels,
        "directory": "Config Validation",
    }


def validate_seed_field_parsing(summary: dict[str, object]) -> list[str]:
    issues: list[str] = []
    if summary.get("row_count", 0) == 0:
        issues.append("demo rows should not be empty")
    if summary.get("directory") != "Config Validation":
        issues.append("directory label drifted from the intended block")
    if not str(summary.get("objective", "")).strip():
        issues.append("objective text should be present for review")
    return issues


def render_demo_path(base: str | Path) -> Path:
    return Path(base) / "b04_pds_0393.jsonl"


def main() -> None:
    rows = build_demo_rows()
    summary = summarize_seed_field_parsing(rows)
    issues = validate_seed_field_parsing(summary)
    print(summary)
    print({"issues": issues, "demo_path": str(render_demo_path("draft_examples"))})


if __name__ == "__main__":
    main()
