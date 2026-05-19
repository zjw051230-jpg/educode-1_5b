---
draft_status: candidate
topic_id: B05-RTS-0009
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-4
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---

# Directory Name Hides Gap

The narrow goal here is to decide what directory name hides gap means in one specific runtime scene.

**Learning objective:** Spot a checkpoint directory name that looks monotonic even though step_12400 was never written.

## Artifact packet
- topic_id: B05-RTS-0009
- subdirectory: `checkpointing`
- concrete anchor: numeric toy example
- artifact focus: directory names + summary counter table

## Snapshot
```text
checkpoint_dir: /runs/exp_0009/step_12427
summary.json: latest_step=12427 best_step=12307 val_loss=1.89
trainer.log: resumed_from=step_12422 optimizer_step=12418
metrics.jsonl: last_eval_end step=12425 tokens_seen=121870
```

## Why this packet is interesting
- The artifact set is small enough to inspect by hand.
- Two signals agree, and one signal is suspiciously behind.
- The bounded disagreement is the whole lesson; there is no need to invent a larger story.

## Topic-specific example
A reviewer compares three lines before trusting the run state:

| artifact | observed value | why it matters |
|---|---:|---|
| trainer.log resume step | 12422 | shows where the process thinks it restarted |
| summary.json latest_step | 12427 | shows the summary writer's latest persisted step |
| optimizer_step in checkpoint | 12418 | reveals whether optimizer state kept pace |

If the model weights came from step `12427` but optimizer state is still aligned with `12418`, the next few loss values can jump for a reason that is not weight corruption.

## Pseudo-run log
```text
[12422] INFO resume checkpoint=/runs/exp_0009/step_12427
[12423] INFO loaded model_state shards=4
[12423] INFO loaded optimizer_state shards=4 optimizer_step=12418
[12424] INFO scheduler last_epoch=12417
[12425] INFO validation end val_loss=1.89 tokens_seen=121870
[12426] INFO checkpoint save latest_step=12427
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
