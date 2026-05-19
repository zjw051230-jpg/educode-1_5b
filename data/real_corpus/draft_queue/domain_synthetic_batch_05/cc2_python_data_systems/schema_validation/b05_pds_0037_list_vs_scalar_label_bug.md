---
draft_status: candidate
topic_id: B05-PDS-0037
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-2
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---

# List Vs Scalar Label Bug

## Diary entry
I started with a symptom tied to failure scenario.
The concrete target was to show how a list-vs-scalar label bug propagates into batching assumptions.

## First clue
```text
09:10 loader preview: 4 rows scanned
09:10 warning: expected key `split`, saw key `spilt` on row 3
09:11 validator halted before batching
```

## Wrong guess I rejected
At first glance the problem looked like a parser issue, but the parser only exposed a field-name drift that had already entered the draft asset.

## Actual cause
The failure came from a local mismatch between the schema assumption and the stored row shape.

## Repair I kept
I kept the repair only if it could be expressed as a reversible field-level action with a visible validation check immediately after it.

## Regression question
If the same shard appears tomorrow with a different mismatch, which signal would tell us the old repair rule is too narrow?

## One detail that keeps this file distinct
Its center of gravity is a diary-style failure narrative, not a generic explanation block about schema_validation.

- Extra verification prompt: explain which single observation would prove the repair worked.

- Extra verification prompt: explain which single observation would prove the repair worked.

- Extra verification prompt: explain which single observation would prove the repair worked.

- Extra verification prompt: explain which single observation would prove the repair worked.

- Extra verification prompt: explain which single observation would prove the repair worked.

- Extra verification prompt: explain which single observation would prove the repair worked.

- Extra verification prompt: explain which single observation would prove the repair worked.

- Extra verification prompt: explain which single observation would prove the repair worked.
