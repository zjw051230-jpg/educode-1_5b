---
draft_status: candidate
topic_id: B05-BIL-0036
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-5
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---

# BPE Merge Rules and Vocabulary Growth 36: Rare Term Budget

## Failure analysis
A merge list that looks statistically sensible can still fail a bilingual technical task.

## Symptom
- `throughput` survives as one piece
- `A100` splits in half
- punctuation neighbors keep getting merged ahead of the hardware literal

## Why the failure matters
The model then sees a stable English descriptor but an unstable identifier for the same lesson. That weakens retrieval of the concrete technical anchor.

## Before / after
| setting | merge kept | result |
|---|---|---|
| raw frequency only | `(, ,keep)` | `A` + `100` |
| literal-aware bonus | `(A,100)` | `A100` |

## Concrete anchor: debugging transcript
The analysis depends on one merge table comparison.

## Learning objective
See why literal-aware merge ranking can outperform naive frequency sorting in bilingual technical data.
