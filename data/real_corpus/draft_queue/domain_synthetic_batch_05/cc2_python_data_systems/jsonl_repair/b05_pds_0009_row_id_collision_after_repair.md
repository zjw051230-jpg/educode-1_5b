---
draft_status: candidate
topic_id: B05-PDS-0009
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-2
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---

# Row Id Collision After Repair

## What the learner should leave with
spot row id collisions introduced by a careless repair merge.

## Broken case on the table
This note focuses on a debugging transcript inside `jsonl_repair`.
The example is intentionally small so the repair rule stays visible instead of hiding inside pipeline boilerplate.

## Concrete sample
```text
topic_id: B05-PDS-0009
broken_focus: row_id_collision_after_repair
row_01: {"doc_id": "a1", "text": "alpha"}
row_02: {"doc_id": "a2", "text": "beta"
row_03: {"doc_id": "a3", "text": "gamma"}
```

## Why it breaks
A downstream loader cannot distinguish a truncated object from a clean end-of-file condition unless the repair pass preserves row identity and surfaces the failure site.
That is the teaching point here: repair must be specific, not magical.

## Repair steps
1. Isolate the first row that violates the local rule.
2. Decide whether the row can be repaired deterministically.
3. Keep a note of the original row number.
4. Re-validate the repaired stream before counting the file as usable.

## Tiny verification questions
- Which row should be rejected before any batching logic runs?
- What evidence proves the repair pass did not silently reorder rows?
- Which field would you preserve in a sidecar report?

## Distinctive detail
The learning objective is not “understand jsonl_repair broadly”; it is to spot row id collisions introduced by a careless repair merge.

- Extra verification prompt: explain which single observation would prove the repair worked.

- Extra verification prompt: explain which single observation would prove the repair worked.

- Extra verification prompt: explain which single observation would prove the repair worked.

- Extra verification prompt: explain which single observation would prove the repair worked.
