---
draft_status: candidate
topic_id: B05-RTS-0071
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-4
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---

# Smoke Pass But Checkpoint Incomplete

The fastest way to misread smoke pass but checkpoint incomplete is to quote the neatest number and ignore the artifact trail behind it.

**Learning objective:** Explain how a smoke test can look green while still writing an incomplete checkpoint bundle.

## Runtime scene
This walkthrough uses `smoke summary + checkpoint tree` plus a small pseudo trace to show how a topic-specific check should reason about the packet.

## Pseudo trace
```python
step = 12614
val_batches = [128, 128, 64, 32]
losses = [1.830, 1.780, 1.750, 1.970]
weighted = sum(b * l for b, l in zip(val_batches, losses)) / sum(val_batches)
naive = sum(losses) / len(losses)
```

## Walkthrough notes
1. The trace is short on purpose.
2. The last batch is smaller, which matters if the topic touches weighted aggregation.
3. The interesting question is whether the runtime summary used `weighted` or `naive`.

## Artifact excerpt
```text
summary.json val_loss=1.750
metrics.jsonl eval_end weighted_loss=1.760
metrics.jsonl debug naive_mean=1.830
```

## What the trace proves
The packet is only interpretable because the code trace names the arithmetic that the artifact fields imply. Without that, the file would collapse back into generic review framing.

## Failure mode diagnosis
If the summary copied `naive_mean` instead of `weighted_loss`, the checkpoint chosen from that summary could be wrong even though each individual batch loss looks plausible.

## Review takeaway
A short trace is enough when it directly explains the exact artifact disagreement.
