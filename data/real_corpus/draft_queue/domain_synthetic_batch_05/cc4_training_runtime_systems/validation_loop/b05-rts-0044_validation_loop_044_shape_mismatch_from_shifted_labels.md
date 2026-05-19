---
draft_status: candidate
topic_id: B05-RTS-0044
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-4
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---

# Shape Mismatch From Shifted Labels

The narrow goal here is to decide what shape mismatch from shifted labels means in one specific runtime scene.

**Learning objective:** Trace a validation crash caused by logits of [8,4096,32000] against labels of [8,4095].

## Q1. What is the bounded runtime scene?
A run near step `12533` emitted `tensor shapes + stack trace` and one neighboring event sequence. The scene is deliberately small so the diagnosis stays specific.

## Q2. Which numbers matter first?
- allocated_gb = 39.7
- reserved_gb = 66.9
- peak_gb = 70.5
- seq_len = 2048
- tokens_per_sec = 136920

## Q3. What does the packet look like?
```text
step=12532 event=train_step
step=12533 event=eval_end val_loss=1.960
step=12533 event=summary_write best_step=12503
step=12534 event=checkpoint_save latest_step=12534
```

## Q4. What is the subtle mistake people make?
They answer with a general rule about runtime reviews instead of explaining what these exact artifacts say.

## Q5. What is the better answer?
The better answer says which artifact is closest to the underlying state update and why a neighboring artifact either confirms it or lags behind it.

## Q6. What failure mode does this packet suggest?
A narrow bookkeeping or boundary-handling issue is more plausible than a fully broken training loop when only one artifact family drifts.

## Q7. What would strengthen confidence?
- one more adjacent event row
- one matching config field
- one field-level comparison rather than a title-level comparison

## Final answer
Treat the packet as a targeted diagnostic exercise, not a general lesson about all training runs.
