---
draft_status: candidate
topic_id: RTS-015
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC4
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
---

# Metrics Logging per Step vs per Eval

## Concept
Per-step logging and per-eval logging serve different purposes.
One captures runtime evolution at fine granularity.
The other records less frequent but often more interpretable checkpoints.

## Explanation
Per-step logs are useful for:
- train loss trend inspection
- step time tracking
- memory tracking
- failure localization around a bad step

Per-eval logs are useful for:
- validation loss snapshots
- aggregate quality checks
- milestone summaries
- early overfit review

A practical system often uses both.
Per-step rows show how the run behaves.
Per-eval rows show what periodic evaluation concluded.

## Minimal Example
A run logs every training step:
- step
- train_loss
- lr
- step_time_ms
- cuda_reserved_gb

Every 100 steps it also logs an evaluation row:
- step
- val_loss
- tokens_seen
- checkpoint_written

The schemas overlap, but their intent differs.

## Common Pitfalls
One pitfall is forcing validation fields into every step row, producing mostly empty columns.
Another is logging every possible metric every step and slowing down the run.
A third is naming fields differently across train and eval summaries for the same concept.
A fourth is failing to distinguish missing metrics from not-yet-computed metrics.

## Review Notes
The right logging frequency depends on the question being asked.
If you are debugging a transient runtime issue, per-step detail matters.
If you are reviewing experiment progression, per-eval summaries may carry more signal.
Educational examples should teach that logging design is about review utility, not metric hoarding.
