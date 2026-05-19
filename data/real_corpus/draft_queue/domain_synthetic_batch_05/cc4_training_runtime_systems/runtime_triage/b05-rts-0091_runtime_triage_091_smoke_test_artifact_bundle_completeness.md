---
draft_status: candidate
topic_id: B05-RTS-0091
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-4
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---

# Smoke Artifact Bundle Completeness

The fastest way to misread smoke artifact bundle completeness is to quote the neatest number and ignore the artifact trail behind it.

**Learning objective:** Check whether a supposedly successful smoke test wrote every artifact promised by its config and progress log.

## Config fragment under review
```yaml
seq_len: 4608
microbatch_size: 8
grad_accum: 4
eval_every_steps: 25
save_every_steps: 70
eval_batch_size: 4
smoke_reserved_gb_limit: 59.8
```

## Why this config matters
A config review is only useful when it predicts a visible runtime artifact. Here the interesting question is whether these settings create the exact boundary behavior seen in `artifact checklist + run log`.

## Predicted artifact schedule
- training steps emit dense metrics rows
- evaluation starts near step 12674
- checkpoint save is likely near step 12675
- the memory guardrail may fire if reserved exceeds 59.8 GB

## Concrete packet
```text
step=12674 event=eval_start seq_len=4608
step=12674 reserved_gb=57.8
step=12675 event=checkpoint_save duration_ms=612
```

## Review notes
- If `eval_every_steps` and `save_every_steps` land on the same window, latency spikes can stack.
- If `eval_batch_size` differs from training microbatch, validation-specific memory surprises become more likely.
- If the smoke limit sits only 1-2 GB above the observed reserved peak, a tiny data shift can flip the gate.

## Failure mode diagnosis
This config is risky when it creates exactly the boundary pattern that later appears in the logs. The config itself is not the bug, but it explains why the artifact sequence looks the way it does.

## Decision
Treat the runtime packet as expected-under-config only if the predicted schedule matches the observed events.
