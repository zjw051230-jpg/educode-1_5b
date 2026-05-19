---
draft_status: candidate
topic_id: B05-PDS-0091
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-2
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---

# Best Checkpoint Metric Choice

## Comparison target
use Q&A form to decide which metric should drive best-checkpoint selection.

| aspect | before repair | after repair |
|---|---|---|
| visible symptom | split labels disagree | split labels normalized |
| row accounting | one shard cannot be joined | all shards can be joined |
| reviewer effort | manual guesswork | deterministic re-check |
| safety | hidden coercion risk | explicit repair note |

## What to notice
The table is anchored by decision checklist, so the comparison is about observable differences rather than generic “better wording.”

## Tiny data point
```text
before: val, validation, VAL
after: validation, validation, validation
```

## Prompt
State which column changed because of normalization and which changed because of validation.

- Extra verification prompt: explain which single observation would prove the repair worked.

- Extra verification prompt: explain which single observation would prove the repair worked.

- Extra verification prompt: explain which single observation would prove the repair worked.

- Extra verification prompt: explain which single observation would prove the repair worked.

- Extra verification prompt: explain which single observation would prove the repair worked.

- Extra verification prompt: explain which single observation would prove the repair worked.

- Extra verification prompt: explain which single observation would prove the repair worked.

- Extra verification prompt: explain which single observation would prove the repair worked.

- Extra verification prompt: explain which single observation would prove the repair worked.

- Extra verification prompt: explain which single observation would prove the repair worked.
