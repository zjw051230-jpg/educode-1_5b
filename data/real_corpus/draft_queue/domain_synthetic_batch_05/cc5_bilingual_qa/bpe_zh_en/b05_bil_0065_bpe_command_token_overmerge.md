---
draft_status: candidate
topic_id: B05-BIL-0065
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-5
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---

# BPE Merge Rules and Vocabulary Growth 65: Command Token Overmerge

## Numeric toy example
Suppose a shard gives the following pair scores:
- `(A,100)`: 4 + 2 bonus = 6
- `(吞,吐)`: 5 + 0 bonus = 5
- `(lr,=)`: 3 - 1 penalty = 2

A raw-frequency system would choose `(吞,吐)` first. The literal-aware system chooses `(A,100)` first.

## Why the ranking shift matters
One ranking preserves a visible hardware anchor in both languages; the other only optimizes general compression.

## Concrete anchor: before/after comparison
The file teaches through scored comparisons.

## Learning objective
Map merge ranking changes to real teaching consequences in bilingual technical text.
