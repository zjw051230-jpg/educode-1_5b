---
draft_status: candidate
topic_id: B05-RTS-0030
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-4
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---

# Smoke Checkpoint Expectation Matrix

Instead of explaining smoke checkpoint expectation matrix in the abstract, this file starts from a concrete artifact packet.

**Learning objective:** Use a decision matrix to decide which artifacts must exist after a 50-step smoke test with save interval 20.

## Incident summary
A short run looked acceptable at first glance, but one artifact suggested a narrow runtime failure mode worth isolating.

## Observed packet
```text
phase=train step=12490 tok/s=130900
phase=eval  step=12491 val_loss=2.100
phase=eval  step=12491 reserved_gb=57.7
phase=save  step=12492 save_ms=520
summary.json latest_step=12492 best_step=12471
```

## Competing explanations
| candidate cause | evidence for it | evidence against it |
|---|---|---|
| real model instability | one metric changed abruptly | neighboring artifacts stayed orderly |
| artifact write lag | summary and log disagree by one event | core tensors or counts are still plausible |
| phase-specific runtime bug | anomaly starts exactly at eval/save boundary | train-only window looks normal |

## Concrete anchor
This file uses **decision checklist** rather than a generic note. The failure is described with bounded numbers: allocated `39.7` GB, reserved `57.7` GB, peak `61.3` GB, sequence length `4096`.

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
