---
draft_status: candidate
topic_id: B05-RTS-0032
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-4
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---

# Event Typing Drift

A runtime reviewer usually gets this topic wrong when the title is read without the artifacts that produced it.

**Learning objective:** Explain why unlabeled eval rows make throughput summaries misleading even when values look plausible.

## Incident summary
A short run looked acceptable at first glance, but one artifact suggested a narrow runtime failure mode worth isolating.

## Observed packet
```text
phase=train step=12496 tok/s=131760
phase=eval  step=12497 val_loss=1.960
phase=eval  step=12497 reserved_gb=64.5
phase=save  step=12498 save_ms=526
summary.json latest_step=12498 best_step=12477
```

## Competing explanations
| candidate cause | evidence for it | evidence against it |
|---|---|---|
| real model instability | one metric changed abruptly | neighboring artifacts stayed orderly |
| artifact write lag | summary and log disagree by one event | core tensors or counts are still plausible |
| phase-specific runtime bug | anomaly starts exactly at eval/save boundary | train-only window looks normal |

## Concrete anchor
This file uses **mini code trace** rather than a generic note. The failure is described with bounded numbers: allocated `41.9` GB, reserved `64.5` GB, peak `68.1` GB, sequence length `2048`.

## Why the failure is topic-specific
The artifact set is not interchangeable with another runtime topic. The diagnosis depends on the exact combination of:
- a step boundary
- one specific artifact family
- one narrow metric disagreement

## Most likely diagnosis
The packet is more consistent with a localized runtime bookkeeping issue than with a total run collapse. The strongest clue is that one artifact lags while adjacent fields remain internally coherent.

## Recommended follow-up
- capture the three rows before the anomaly and the three rows after it
- compare the artifact with the config field that controls the boundary
- rerun the interpretation using weighted or phase-aware numbers if available

## Review takeaway
The file is useful when the reader learns to choose the smallest sufficient explanation from the available runtime evidence.
