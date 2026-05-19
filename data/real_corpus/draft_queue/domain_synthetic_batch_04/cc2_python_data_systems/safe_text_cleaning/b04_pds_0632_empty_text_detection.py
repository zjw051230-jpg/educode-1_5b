# draft_status: candidate
# topic_id: B04-PDS-0632
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
    "empty text detection",
    "edge case guardrail",
    "Safe Text Cleaning",
]


def build_demo_rows() -> list[dict[str, object]]:
    return [
        {"topic_id": "B04-PDS-0632", "label": EXAMPLE_LABELS[0], "position": 0},
        {"topic_id": "B04-PDS-0632", "label": EXAMPLE_LABELS[1], "position": 1},
        {"topic_id": "B04-PDS-0632", "label": EXAMPLE_LABELS[2], "position": 2},
    ]


def summarize_empty_text_detection(rows: Iterable[dict[str, object]]) -> dict[str, object]:
    materialized = list(rows)
    labels = [str(row.get("label", "")) for row in materialized]
    return {
        "topic_id": "B04-PDS-0632",
        "objective": "explaining empty text detection through a edge case guardrail for safe text cleaning",
        "row_count": len(materialized),
        "labels": labels,
        "directory": "Safe Text Cleaning",
    }


def validate_empty_text_detection(summary: dict[str, object]) -> list[str]:
    issues: list[str] = []
    if summary.get("row_count", 0) == 0:
        issues.append("demo rows should not be empty")
    if summary.get("directory") != "Safe Text Cleaning":
        issues.append("directory label drifted from the intended block")
    if not str(summary.get("objective", "")).strip():
        issues.append("objective text should be present for review")
    return issues


def render_demo_path(base: str | Path) -> Path:
    return Path(base) / "b04_pds_0632.jsonl"


def main() -> None:
    rows = build_demo_rows()
    summary = summarize_empty_text_detection(rows)
    issues = validate_empty_text_detection(summary)
    print(summary)
    print({"issues": issues, "demo_path": str(render_demo_path("draft_examples"))})


if __name__ == "__main__":
    main()
