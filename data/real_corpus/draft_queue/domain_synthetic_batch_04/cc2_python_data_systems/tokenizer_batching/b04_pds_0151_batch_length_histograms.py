# draft_status: candidate
# topic_id: B04-PDS-0151
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
    "batch length histograms",
    "review checklist framing",
    "Tokenizer Batching",
]


def build_demo_rows() -> list[dict[str, object]]:
    return [
        {"topic_id": "B04-PDS-0151", "label": EXAMPLE_LABELS[0], "position": 0},
        {"topic_id": "B04-PDS-0151", "label": EXAMPLE_LABELS[1], "position": 1},
        {"topic_id": "B04-PDS-0151", "label": EXAMPLE_LABELS[2], "position": 2},
    ]


def summarize_batch_length_histograms(rows: Iterable[dict[str, object]]) -> dict[str, object]:
    materialized = list(rows)
    labels = [str(row.get("label", "")) for row in materialized]
    return {
        "topic_id": "B04-PDS-0151",
        "objective": "explaining batch length histograms through a review checklist framing for tokenizer batching",
        "row_count": len(materialized),
        "labels": labels,
        "directory": "Tokenizer Batching",
    }


def validate_batch_length_histograms(summary: dict[str, object]) -> list[str]:
    issues: list[str] = []
    if summary.get("row_count", 0) == 0:
        issues.append("demo rows should not be empty")
    if summary.get("directory") != "Tokenizer Batching":
        issues.append("directory label drifted from the intended block")
    if not str(summary.get("objective", "")).strip():
        issues.append("objective text should be present for review")
    return issues


def render_demo_path(base: str | Path) -> Path:
    return Path(base) / "b04_pds_0151.jsonl"


def main() -> None:
    rows = build_demo_rows()
    summary = summarize_batch_length_histograms(rows)
    issues = validate_batch_length_histograms(summary)
    print(summary)
    print({"issues": issues, "demo_path": str(render_demo_path("draft_examples"))})


if __name__ == "__main__":
    main()
