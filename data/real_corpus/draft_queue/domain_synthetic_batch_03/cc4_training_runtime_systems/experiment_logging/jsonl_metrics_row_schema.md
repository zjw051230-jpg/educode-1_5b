---
draft_status: candidate
topic_id: RTS-018
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC4
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
---

# JSONL Metrics Row Schema

## Concept
A JSONL metrics schema works best when every row has a clear event meaning.
That keeps downstream review tools simple.

## Explanation
A metrics row often represents one of a few event types:
- training step
- evaluation summary
- checkpoint write
- run end summary

Instead of inventing separate files for every event, a team can keep one JSONL stream and include an `event_type` field.
That makes append-only logging straightforward while preserving row meaning.

Useful fields may include:
- `event_type`
- `step`
- `wall_time_s`
- `train_loss`
- `val_loss`
- `lr`
- `tokens_per_s`
- `cuda_reserved_gb`

## Minimal Example
A training row might contain `event_type: train_step` and omit `val_loss`.
An evaluation row might contain `event_type: eval` and include `val_loss`.
A checkpoint row might contain `event_type: checkpoint_saved` and include the artifact name.

The schema is consistent because the row type explains which fields are expected.

## Common Pitfalls
One pitfall is logging rows with no event marker and expecting consumers to infer meaning.
Another is changing field names between row types for the same metric.
A third is stuffing long prose notes into every row.
A fourth is forgetting that sparse fields should be documented rather than assumed.

## Review Notes
A good JSONL schema supports two reading styles.
Humans can inspect a handful of rows directly.
Small scripts can aggregate them without complex parsing rules.
That balance is ideal for educational runtime drafts where clarity matters more than maximal schema flexibility.
