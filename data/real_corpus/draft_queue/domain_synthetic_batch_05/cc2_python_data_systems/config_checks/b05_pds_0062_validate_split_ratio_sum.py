# draft_status: candidate
# topic_id: B05-PDS-0062
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

"""Validate Split Ratio Sum.
Learning objective: validate that train/val/test ratios sum to one within a strict tolerance.
Concrete anchor: numeric toy example.
"""

@dataclass
class ReviewIssue:
    code: str
    message: str
    row_ref: str

def validate_config(cfg: dict[str, object]) -> list[ReviewIssue]:
    issues: list[ReviewIssue] = []
    batch_size = int(cfg.get("batch_size", 0))
    max_length = int(cfg.get("max_length", 0))
    ratios = cfg.get("split_ratio", [])
    if batch_size > 0 and max_length > 0 and batch_size * max_length > 8192:
        issues.append(ReviewIssue("memory_budget", "batch_size * max_length exceeds toy review budget", "config"))
    if isinstance(ratios, list) and ratios and abs(sum(ratios) - 1.0) > 1e-6:
        issues.append(ReviewIssue("ratio_sum", "split ratios must sum to 1.0", "config"))
    if cfg.get("log_eval_every") == 0:
        issues.append(ReviewIssue("missing_eval_interval", "log_eval_every must be positive", "config"))
    return issues

def main() -> None:
    config = {
        "batch_size": 32,
        "max_length": 4096,
        "split_ratio": [0.8, 0.15, 0.1],
        "log_eval_every": 0,
    }
    issues = validate_config(config)
    print({
        "topic_id": "B05-PDS-0062",
        "issue_codes": [issue.code for issue in issues],
        "messages": [issue.message for issue in issues],
    })

if __name__ == "__main__":
    main()

def _review_prompt() -> str:
    return "validate that train/val/test ratios sum to one within a strict tolerance"

