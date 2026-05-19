---
draft_status: candidate
topic_id: B05-RTS-0001
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-4
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---

# Pointer Gap At Resume

The fastest way to misread pointer gap at resume is to quote the neatest number and ignore the artifact trail behind it.

**Learning objective:** Trace a resume event where optimizer_step lags global_step after a checkpoint reload and decide which counter should be trusted first.

## Artifact packet
- topic_id: B05-RTS-0001
- subdirectory: `checkpointing`
- concrete anchor: pseudo-run log
- artifact focus: checkpoint_state.pt keys + trainer resume log

## Snapshot
```text
checkpoint_dir: /runs/exp_0001/step_12403
summary.json: latest_step=12403 best_step=12283 val_loss=2.03
trainer.log: resumed_from=step_12398 optimizer_step=12394
metrics.jsonl: last_eval_end step=12401 tokens_seen=118430
```

## Why this packet is interesting
- The artifact set is small enough to inspect by hand.
- Two signals agree, and one signal is suspiciously behind.
- The bounded disagreement is the whole lesson; there is no need to invent a larger story.

## Topic-specific example
A reviewer compares three lines before trusting the run state:

| artifact | observed value | why it matters |
|---|---:|---|
| trainer.log resume step | 12398 | shows where the process thinks it restarted |
| summary.json latest_step | 12403 | shows the summary writer's latest persisted step |
| optimizer_step in checkpoint | 12394 | reveals whether optimizer state kept pace |

If the model weights came from step `12403` but optimizer state is still aligned with `12394`, the next few loss values can jump for a reason that is not weight corruption.

## Pseudo-run log
```text
[12398] INFO resume checkpoint=/runs/exp_0001/step_12403
[12399] INFO loaded model_state shards=4
[12399] INFO loaded optimizer_state shards=4 optimizer_step=12394
[12400] INFO scheduler last_epoch=12393
[12401] INFO validation end val_loss=2.03 tokens_seen=118430
[12402] INFO checkpoint save latest_step=12403
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
