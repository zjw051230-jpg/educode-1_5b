---
draft_status: candidate
topic_id: B05-RTS-0004
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-4
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---

# Stale Best Step After Resume

The narrow goal here is to decide what stale best step after resume means in one specific runtime scene.

**Learning objective:** Show how best_step can stay stale across resume while latest_step advances correctly in logs.

## 09:12 — what I opened first
The bundle contained `summary.json before/after + resume log` plus a short trainer log. I expected one clean explanation, but the first pass produced two competing stories.

## 09:16 — raw notes
- topic_id: B05-RTS-0004
- anchor: metrics interpretation
- memory_allocated_gb: 41.9
- memory_reserved_gb: 69.1
- peak_reserved_gb: 72.7
- seq_len: 2048
- microbatch: 2

## 09:22 — artifact excerpt
```text
step=12412 train_loss=2.060 lr=1.20e-4 tok/s=119720
step=12413 val_loss=1.820 max_memory_allocated_gb=41.9
step=12413 max_memory_reserved_gb=69.1
step=12414 save_event=complete latest_step=12414
```

## 09:27 — first wrong hypothesis
I initially blamed the cleanest-looking metric row, because it was already normalized and easy to quote. That was too shallow. The row by itself did not explain why the neighboring artifact was lagging.

## 09:35 — the comparison that mattered
| signal | looked healthy? | hidden issue |
|---|---|---|
| throughput row | yes | did not say whether the row came from train or eval |
| memory headline | mostly | hid a larger reserved-memory jump |
| summary field | maybe | updated later than the underlying event |

## 09:42 — diagnosis path
The incident became interpretable only after tying the numbers to a concrete run scene:
1. check which event emitted the line
2. compare that event with adjacent fields in the summary artifact
3. ask whether a delayed write or phase switch could create the mismatch

## 09:49 — failure signature
The suspicious combination is:
- a clean-looking summary field
- a nearby lagging counter or missing event
- one phase transition such as validation or checkpoint save

That bundle usually signals bookkeeping drift, not a mysterious training collapse.

## 09:55 — conclusion entry
For this file, the diagnostic value comes from the bounded disagreement itself. The artifact packet is useful because it teaches the reader to stop after one well-supported explanation instead of inflating the review into a larger narrative.
