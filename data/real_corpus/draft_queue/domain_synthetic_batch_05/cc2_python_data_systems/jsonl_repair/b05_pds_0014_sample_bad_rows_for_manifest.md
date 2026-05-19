---
draft_status: candidate
topic_id: B05-PDS-0014
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-2
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---

# Sample Bad Rows For Manifest

## Lab setup
Goal: sample the first three broken rows for a review manifest sidecar.
Anchor: mini code trace.

## Inputs
| item | value |
|---|---|
| expected objects | 3 |
| valid rows before repair | 2 |
| malformed rows | 1 |

## Procedure
```text
step 1: preview three rows
step 2: mark the malformed token boundary
step 3: apply a narrow repair rule
step 4: parse again and compare counts
```

## Observation sheet
- Before repair, one row fails for a visible local reason.
- After repair, the row count changes only if the malformed row becomes valid.
- The learner should state whether the repair was deterministic or guessy.

## Expected output
```text
usable_rows_before: 2
usable_rows_after: 3
rows_requiring_manual_review: 0
```

## Why this lab is narrow
The point is not to simulate a whole trainer. The point is to practice one repair-aware decision with observable consequences.

- Extra verification prompt: explain which single observation would prove the repair worked.

- Extra verification prompt: explain which single observation would prove the repair worked.

- Extra verification prompt: explain which single observation would prove the repair worked.

- Extra verification prompt: explain which single observation would prove the repair worked.
