---
draft_status: candidate
topic_id: PDS-004
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC2
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
---

# Consistency Checks Between Manifests and Splits

## Concept
A split manifest describes which files or records belong to train and validation partitions. A consistency check confirms that the manifest and the actual split outputs still agree.

## Explanation
In tiny educational pipelines, split logic often changes faster than the surrounding documentation. A manifest might still say that `train.jsonl` contains 900 rows while the regenerated file now contains 880 rows. Without a consistency pass, downstream readers may assume the mismatch is acceptable and continue.

A good check answers simple questions: do all listed files exist, do listed counts match observed counts, and does any record ID appear in more than one split. This is especially useful when review is manual, because the checker can surface a short report instead of forcing a reviewer to inspect every file by hand.

## Minimal Example
A draft checker can compare:
1. manifest row count for each split
2. observed row count from the current files
3. overlap of stable IDs between train and validation

If any one of these checks fails, the split should be treated as review-needed rather than silently accepted.

## Common Pitfalls
- Using filenames as the only identity when multiple files can contain the same record IDs.
- Verifying counts but never checking for overlap.
- Updating split files without updating the manifest.
- Treating a stale manifest as harmless metadata.

## Review Notes
The point of manifest consistency is not bureaucracy. It is a cheap way to preserve trust in later metrics, because train and validation comparisons stop being meaningful once the partition boundary becomes uncertain.
