---
draft_status: candidate
topic_id: B05-TRF-0038
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-3
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---

# Separating visibility bugs from shape bugs (mask matrix)

## Failure scenario
A teammate reports that the mask matrix branch is “probably fine” because the outer tensor shape still matches.

### Why that report is incomplete
- Outer shape agreement can hide a wrong inner split.
- A mask row can be the wrong pattern while still matching the expected matrix size.
- A logits tensor can have the right rank while using the wrong last dimension.

### Better response
Ask for one numeric toy example, one explicit tuple, and one statement of the intended invariant.


## Focused follow-up checks
- Confirm that the mask matrix example can be restated as one tuple, one rule, and one failure symptom.
- Re-run the example mentally after swapping the anchor from `numeric toy example` to a second artifact.
- Ask whether the same reasoning would still work if sequence length changed from 5 to 7.

## One concrete failure mode
- A reviewer may accept the outer shape while missing that the inner mask matrix width changed too early.
- Another reviewer may describe the issue abstractly instead of showing the exact numeric toy example.
- The repair-aware move is to print or tabulate the state before and after the suspect step.

## Reader exercise
- Write one additional assertion that protects the mask matrix invariant.
- Rewrite one sentence so it names the axis or score row directly instead of alluding to it.
- Compare the current toy case against a second case where the numeric toy example exposes a different mistake.

## Closing takeaway
This file is only useful if the learner can explain the mask matrix path with concrete evidence rather than topic-shaped prose.
