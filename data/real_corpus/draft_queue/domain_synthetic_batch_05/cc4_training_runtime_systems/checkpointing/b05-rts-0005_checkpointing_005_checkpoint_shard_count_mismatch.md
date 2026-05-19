---
draft_status: candidate
topic_id: B05-RTS-0005
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-4
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---

# Shard Count Mismatch Review

Instead of explaining shard count mismatch review in the abstract, this file starts from a concrete artifact packet.

**Learning objective:** Review a multi-shard checkpoint whose metadata claims four shards while the directory only contains three.

## Artifact packet
- topic_id: B05-RTS-0005
- subdirectory: `checkpointing`
- concrete anchor: before/after comparison
- artifact focus: manifest snippet + shard filenames

## Snapshot
```text
checkpoint_dir: /runs/exp_0005/step_12415
summary.json: latest_step=12415 best_step=12295 val_loss=1.75
trainer.log: resumed_from=step_12410 optimizer_step=12406
metrics.jsonl: last_eval_end step=12413 tokens_seen=120150
```

## Why this packet is interesting
- The artifact set is small enough to inspect by hand.
- Two signals agree, and one signal is suspiciously behind.
- The bounded disagreement is the whole lesson; there is no need to invent a larger story.

## Topic-specific example
A reviewer compares three lines before trusting the run state:

| artifact | observed value | why it matters |
|---|---:|---|
| trainer.log resume step | 12410 | shows where the process thinks it restarted |
| summary.json latest_step | 12415 | shows the summary writer's latest persisted step |
| optimizer_step in checkpoint | 12406 | reveals whether optimizer state kept pace |

If the model weights came from step `12415` but optimizer state is still aligned with `12406`, the next few loss values can jump for a reason that is not weight corruption.

## Pseudo-run log
```text
[12410] INFO resume checkpoint=/runs/exp_0005/step_12415
[12411] INFO loaded model_state shards=4
[12411] INFO loaded optimizer_state shards=4 optimizer_step=12406
[12412] INFO scheduler last_epoch=12405
[12413] INFO validation end val_loss=1.75 tokens_seen=120150
[12414] INFO checkpoint save latest_step=12415
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
