---
draft_status: candidate
topic_id: B05-RTS-0052
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-4
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---

# Checkpoint Selection Under Metric Drift

A runtime reviewer usually gets this topic wrong when the title is read without the artifacts that produced it.

**Learning objective:** Choose a safe checkpoint when validation loss improves but accuracy drifts down across the same window.

## Q1. What is the bounded runtime scene?
A run near step `12557` emitted `metric comparison table` and one neighboring event sequence. The scene is deliberately small so the diagnosis stays specific.

## Q2. Which numbers matter first?
- allocated_gb = 40.8
- reserved_gb = 63.4
- peak_gb = 67.0
- seq_len = 2048
- tokens_per_sec = 140360

## Q3. What does the packet look like?
```text
step=12556 event=train_step
step=12557 event=eval_end val_loss=1.820
step=12557 event=summary_write best_step=12527
step=12558 event=checkpoint_save latest_step=12558
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
