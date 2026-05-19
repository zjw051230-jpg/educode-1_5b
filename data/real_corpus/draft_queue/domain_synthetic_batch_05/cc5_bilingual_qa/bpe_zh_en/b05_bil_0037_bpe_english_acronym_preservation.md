---
draft_status: candidate
topic_id: B05-BIL-0037
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-5
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---

# BPE Merge Rules and Vocabulary Growth 37: English Acronym Preservation

## Debugging diary
11:02 — The generated vocab looked fine overall, but `A100` kept splitting in one shard.

11:09 — Pair counts were healthy. The issue was merge priority after punctuation-heavy English examples crowded the shortlist.

11:15 — The shard had enough evidence for `(A,100)` but not enough rank to beat comma-adjacent pairs.

## Failure slice
- expected: `[A100]`
- observed: `[A][100]`

## Concrete anchor: numeric toy example
The anchor is a shard-level failure scenario, not a generic statement about vocab growth.

## Learning objective
Trace literal fragmentation back to merge-priority competition.
