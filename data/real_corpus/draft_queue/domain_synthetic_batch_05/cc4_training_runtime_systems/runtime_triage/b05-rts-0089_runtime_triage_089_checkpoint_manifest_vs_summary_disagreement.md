---
draft_status: candidate
topic_id: B05-RTS-0089
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-4
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---

# Checkpoint Manifest Versus Summary

The narrow goal here is to decide what checkpoint manifest versus summary means in one specific runtime scene.

**Learning objective:** Resolve a disagreement between checkpoint manifest contents and summary.json claims about the latest complete save.

## Config fragment under review
```yaml
seq_len: 3072
microbatch_size: 4
grad_accum: 2
eval_every_steps: 40
save_every_steps: 50
eval_batch_size: 2
smoke_reserved_gb_limit: 72.2
```

## Why this config matters
A config review is only useful when it predicts a visible runtime artifact. Here the interesting question is whether these settings create the exact boundary behavior seen in `manifest excerpt + summary.json snippet`.

## Predicted artifact schedule
- training steps emit dense metrics rows
- evaluation starts near step 12668
- checkpoint save is likely near step 12669
- the memory guardrail may fire if reserved exceeds 72.2 GB

## Concrete packet
```text
step=12668 event=eval_start seq_len=3072
step=12668 reserved_gb=70.2
step=12669 event=checkpoint_save duration_ms=608
```

## Review notes
- If `eval_every_steps` and `save_every_steps` land on the same window, latency spikes can stack.
- If `eval_batch_size` differs from training microbatch, validation-specific memory surprises become more likely.
- If the smoke limit sits only 1-2 GB above the observed reserved peak, a tiny data shift can flip the gate.

## Failure mode diagnosis
This config is risky when it creates exactly the boundary pattern that later appears in the logs. The config itself is not the bug, but it explains why the artifact sequence looks the way it does.

## Decision
Treat the runtime packet as expected-under-config only if the predicted schedule matches the observed events.
