# draft_status: candidate
# topic_id: B05-PDS-0058
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

"""Verify Sorted Length Order.
Learning objective: verify that a length-sorted batch stays stable after a filtering pass.
Concrete anchor: mini code trace.
"""

@dataclass
class ReviewIssue:
    code: str
    message: str
    row_ref: str

def pad_batch(sequences: list[list[int]], pad_id: int) -> tuple[list[list[int]], list[list[int]]]:
    max_len = max(len(seq) for seq in sequences)
    padded: list[list[int]] = []
    masks: list[list[int]] = []
    for seq in sequences:
        pad_count = max_len - len(seq)
        padded.append(seq + [pad_id] * pad_count)
        masks.append([1] * len(seq) + [0] * pad_count)
    return padded, masks

def validate_shapes(padded: list[list[int]], masks: list[list[int]]) -> list[ReviewIssue]:
    issues: list[ReviewIssue] = []
    if len(padded) != len(masks):
        issues.append(ReviewIssue("batch_count_mismatch", "padded rows and mask rows differ", "batch"))
    for idx, (row, mask) in enumerate(zip(padded, masks), start=1):
        if len(row) != len(mask):
            issues.append(ReviewIssue("shape_mismatch", "row and mask lengths differ", f"batch_row:{idx}"))
    return issues

def main() -> None:
    sequences = [[11, 12, 13, 14], [21, 22], [31, 32, 33]]
    padded, masks = pad_batch(sequences, pad_id=0)
    issues = validate_shapes(padded, masks)
    print({
        "topic_id": "B05-PDS-0058",
        "input_lengths": [len(seq) for seq in sequences],
        "padded_shape": [len(padded), len(padded[0])],
        "mask_shape": [len(masks), len(masks[0])],
        "issues": [issue.code for issue in issues],
    })

if __name__ == "__main__":
    main()
