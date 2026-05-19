---
draft_status: candidate
topic_id: B05-TRF-0066
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-3
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---

# Why a valid causal mask still fails with padding (mask matrix)

## Short pseudo-run log
```
[info] topic=B05-TRF-0066
[info] subdir=attention_masking
[info] opening-artifact=before/after comparison
[trace] hidden=(2, 5, 14)
[trace] focused-path=mask matrix
[warn] mismatch discovered after line-of-interest
```

## Reading the log
This file is intentionally written like a bug triage note so that the opening texture changes from neighboring markdown files.
The learner reads the log, names the invariant, and only then explains the shape decision.


## Focused follow-up checks
- Confirm that the mask matrix example can be restated as one tuple, one rule, and one failure symptom.
- Re-run the example mentally after swapping the anchor from `before/after comparison` to a second artifact.
- Ask whether the same reasoning would still work if sequence length changed from 6 to 7.

## One concrete failure mode
- A reviewer may accept the outer shape while missing that the inner mask matrix width changed too early.
- Another reviewer may describe the issue abstractly instead of showing the exact before/after comparison.
- The repair-aware move is to print or tabulate the state before and after the suspect step.

## Reader exercise
- Write one additional assertion that protects the mask matrix invariant.
- Rewrite one sentence so it names the axis or score row directly instead of alluding to it.
- Compare the current toy case against a second case where the before/after comparison exposes a different mistake.

## Closing takeaway
This file is only useful if the learner can explain the mask matrix path with concrete evidence rather than topic-shaped prose.
