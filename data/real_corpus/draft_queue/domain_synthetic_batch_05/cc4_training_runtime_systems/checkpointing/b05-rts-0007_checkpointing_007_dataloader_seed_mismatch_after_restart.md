---
draft_status: candidate
topic_id: B05-RTS-0007
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-4
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---

# Restart Seed Drift

A runtime reviewer usually gets this topic wrong when the title is read without the artifacts that produced it.

**Learning objective:** Explain why validation divergence can come from restart-time dataloader seed drift even when the checkpoint itself is intact.

## Artifact packet
- topic_id: B05-RTS-0007
- subdirectory: `checkpointing`
- concrete anchor: tensor shape
- artifact focus: resume config fragment + validation log delta

## Snapshot
```text
checkpoint_dir: /runs/exp_0007/step_12421
summary.json: latest_step=12421 best_step=12301 val_loss=2.03
trainer.log: resumed_from=step_12416 optimizer_step=12412
metrics.jsonl: last_eval_end step=12419 tokens_seen=121010
```

## Why this packet is interesting
- The artifact set is small enough to inspect by hand.
- Two signals agree, and one signal is suspiciously behind.
- The bounded disagreement is the whole lesson; there is no need to invent a larger story.

## Topic-specific example
A reviewer compares three lines before trusting the run state:

| artifact | observed value | why it matters |
|---|---:|---|
| trainer.log resume step | 12416 | shows where the process thinks it restarted |
| summary.json latest_step | 12421 | shows the summary writer's latest persisted step |
| optimizer_step in checkpoint | 12412 | reveals whether optimizer state kept pace |

If the model weights came from step `12421` but optimizer state is still aligned with `12412`, the next few loss values can jump for a reason that is not weight corruption.

## Pseudo-run log
```text
[12416] INFO resume checkpoint=/runs/exp_0007/step_12421
[12417] INFO loaded model_state shards=4
[12417] INFO loaded optimizer_state shards=4 optimizer_step=12412
[12418] INFO scheduler last_epoch=12411
[12419] INFO validation end val_loss=2.03 tokens_seen=121010
[12420] INFO checkpoint save latest_step=12421
```

## What to trust first
1. Trust the artifact that is hardest to synthesize accidentally.
2. Prefer field-level evidence over a directory name.
3. When counters disagree, compare the counter to the event that updates it.

## Failure mode diagnosis
This pattern most often means one of three things:
- optimizer shards were restored from an older save window
- scheduler state was rolled back with the optimizer
- summary.json advanced on a later write than the optimizer payload

It is less consistent with random checkpoint corruption because the weight load finished cleanly and the run continued to emit plausible metrics.

## What to inspect next
- list optimizer shard filenames and compare counts with model shards
- check whether `last_epoch` and `optimizer_step` move together
- compare the first three post-resume losses with the pre-resume trailing window

## Short decision
Treat the checkpoint as usable for review, but do not treat the first post-resume metric swing as pure model behavior until the optimizer counter gap is explained.
