# draft_status: candidate
# topic_id: B05-PDS-0022
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

"""Check Required Columns Against Schema.
Learning objective: check toy records against a required-column schema and return actionable errors.
Concrete anchor: schema mismatch.
"""

@dataclass
class ReviewIssue:
    code: str
    message: str
    row_ref: str

def validate_record(record: dict[str, object], required: dict[str, type]) -> list[ReviewIssue]:
    issues: list[ReviewIssue] = []
    for key, expected_type in required.items():
        if key not in record:
            issues.append(ReviewIssue("missing_key", f"missing {key}", str(record.get("doc_id", "unknown"))))
            continue
        value = record[key]
        if not isinstance(value, expected_type):
            issues.append(ReviewIssue("type_mismatch", f"{key} expected {expected_type.__name__} got {type(value).__name__}", str(record.get("doc_id", "unknown"))))
    return issues

def demo_records() -> list[dict[str, object]]:
    return [
        {"doc_id": "r1", "split": "train", "token_count": 14},
        {"doc_id": "r2", "split": "val", "token_count": "14"},
        {"doc_id": "r3", "token_count": 9},
    ]

def main() -> None:
    schema = {"doc_id": str, "split": str, "token_count": int}
    all_issues: list[ReviewIssue] = []
    for record in demo_records():
        all_issues.extend(validate_record(record, schema))
    print({
        "topic_id": "B05-PDS-0022",
        "issue_count": len(all_issues),
        "issue_codes": [issue.code for issue in all_issues],
        "rows": [issue.row_ref for issue in all_issues],
    })

if __name__ == "__main__":
    main()

def _review_prompt() -> str:
    return "check toy records against a required-column schema and return actionable errors"

