---
draft_status: candidate
topic_id: B05-RTS-0067
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-4
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---

# Wrong Best Checkpoint From Unweighted Mean

A runtime reviewer usually gets this topic wrong when the title is read without the artifacts that produced it.

**Learning objective:** Show how a selection script promotes the wrong checkpoint because it ranks an unweighted validation mean.

## Runtime scene
This walkthrough uses `metric table + selection output` plus a small pseudo trace to show how a topic-specific check should reason about the packet.

## Pseudo trace
```python
step = 12602
val_batches = [128, 128, 64, 32]
losses = [2.110, 2.060, 2.030, 2.250]
weighted = sum(b * l for b, l in zip(val_batches, losses)) / sum(val_batches)
naive = sum(losses) / len(losses)
```

## Walkthrough notes
1. The trace is short on purpose.
2. The last batch is smaller, which matters if the topic touches weighted aggregation.
3. The interesting question is whether the runtime summary used `weighted` or `naive`.

## Artifact excerpt
```text
summary.json val_loss=2.030
metrics.jsonl eval_end weighted_loss=2.040
metrics.jsonl debug naive_mean=2.110
```

## What the trace proves
The packet is only interpretable because the code trace names the arithmetic that the artifact fields imply. Without that, the file would collapse back into generic review framing.

## Failure mode diagnosis
If the summary copied `naive_mean` instead of `weighted_loss`, the checkpoint chosen from that summary could be wrong even though each individual batch loss looks plausible.

## Review takeaway
A short trace is enough when it directly explains the exact artifact disagreement.
