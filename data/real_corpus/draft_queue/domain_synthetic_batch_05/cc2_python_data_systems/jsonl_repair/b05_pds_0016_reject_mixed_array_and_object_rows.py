# draft_status: candidate
# topic_id: B05-PDS-0016
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

"""Reject Mixed Array And Object Rows.
Learning objective: reject streams that mix top-level arrays and objects line by line.
Concrete anchor: schema mismatch.
"""

@dataclass
class ReviewIssue:
    code: str
    message: str
    row_ref: str

def iter_candidate_lines(text: str) -> list[str]:
    return [line for line in text.splitlines() if line.strip()]

def parse_jsonl_lines(lines_in: Iterable[str]) -> tuple[list[dict], list[ReviewIssue]]:
    parsed: list[dict] = []
    issues: list[ReviewIssue] = []
    for idx, raw in enumerate(lines_in, start=1):
        try:
            parsed.append(json.loads(raw))
        except json.JSONDecodeError as exc:
            issues.append(ReviewIssue("json_decode", f"{exc.msg} at col {exc.colno}", f"line:{idx}"))
    return parsed, issues

def repair_line(raw: str) -> str:
    repaired = raw.rstrip()
    if repaired.endswith(",") and repaired.count("{") == repaired.count("}"):
        repaired = repaired[:-1]
    if repaired.startswith("	{"):
        repaired = repaired.lstrip()
    return repaired

def demo_text() -> str:
    return "
".join([
        "{"doc_id": "a1", "text": "ok"}",
        "{"doc_id": "a2", "text": "needs comma repair"},",
        "	{"doc_id": "a3", "text": "tab prefixed"}",
    ])

def main() -> None:
    original = iter_candidate_lines(demo_text())
    parsed_before, issues_before = parse_jsonl_lines(original)
    repaired_lines = [repair_line(line) for line in original]
    parsed_after, issues_after = parse_jsonl_lines(repaired_lines)
    print({
        "topic_id": "B05-PDS-0016",
        "subdirectory": "jsonl_repair",
        "anchor": "schema mismatch",
        "rows_before": len(parsed_before),
        "rows_after": len(parsed_after),
        "issues_before": [issue.message for issue in issues_before],
        "issues_after": [issue.message for issue in issues_after],
    })

if __name__ == "__main__":
    main()
