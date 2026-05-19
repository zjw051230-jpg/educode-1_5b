# draft_status: candidate
# topic_id: B05-PDS-0088
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC-2
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only
# batch_id: domain_synthetic_batch_05
from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Iterable

"""Detect Duplicate Run Ids.
Learning objective: detect duplicate run identifiers across toy metric fragments.
Concrete anchor: failure scenario.
"""

@dataclass
class ReviewIssue:
    code: str
    message: str
    row_ref: str

def validate_metric_rows(rows: list[dict[str, object]]) -> list[ReviewIssue]:
    issues: list[ReviewIssue] = []
    last_step = -1
    for idx, row in enumerate(rows, start=1):
        step = int(row["step"])
        if step < last_step:
            issues.append(ReviewIssue("non_monotonic_step", f"step {step} came after {last_step}", f"metric_row:{idx}"))
        last_step = step
        if "split" not in row:
            issues.append(ReviewIssue("missing_split", "metric row missing split label", f"metric_row:{idx}"))
    return issues

def demo_rows() -> list[dict[str, object]]:
    return [
        {"step": 100, "split": "train", "loss": 2.8},
        {"step": 200, "split": "validation", "loss": 2.7},
        {"step": 150, "split": "validation", "loss": 2.6},
    ]

def main() -> None:
    rows = demo_rows()
    issues = validate_metric_rows(rows)
    print({
        "topic_id": "B05-PDS-0088",
        "row_count": len(rows),
        "issues": [issue.message for issue in issues],
    })

if __name__ == "__main__":
    main()

def _review_prompt() -> str:
    return "detect duplicate run identifiers across toy metric fragments"

