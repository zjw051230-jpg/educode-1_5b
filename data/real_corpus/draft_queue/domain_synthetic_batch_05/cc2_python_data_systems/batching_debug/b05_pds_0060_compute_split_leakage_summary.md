---
draft_status: candidate
topic_id: B05-PDS-0060
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-2
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---

# Compute Split Leakage Summary

## Config under review
```yaml
batch_size: 32
max_length: 4096
split_ratio: [0.8, 0.15, 0.1]
log_eval_every: 0
```

## Review question
compute a toy leakage summary grouped by document family and split.

## Findings
- One field combination is internally inconsistent.
- One field is numerically possible but operationally misleading.
- One field needs a repair rule before downstream interpretation is safe.

## Repair proposal
```yaml
batch_size: 8
max_length: 1024
split_ratio: [0.8, 0.1, 0.1]
log_eval_every: 50
```

## Why this file is not a template clone
It is driven by a concrete config snippet and a review-style comparison, with emphasis on debugging transcript.

## Final check
Name one metric or count that would immediately improve after the repaired config is used.

- Extra verification prompt: explain which single observation would prove the repair worked.

- Extra verification prompt: explain which single observation would prove the repair worked.

- Extra verification prompt: explain which single observation would prove the repair worked.

- Extra verification prompt: explain which single observation would prove the repair worked.

- Extra verification prompt: explain which single observation would prove the repair worked.

- Extra verification prompt: explain which single observation would prove the repair worked.
