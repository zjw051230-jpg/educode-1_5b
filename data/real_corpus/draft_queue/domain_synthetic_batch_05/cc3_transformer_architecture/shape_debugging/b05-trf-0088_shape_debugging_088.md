---
draft_status: candidate
topic_id: B05-TRF-0088
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-3
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---

# How one wrong reshape poisons later blocks (shape mismatch)

## Failure scenario
A teammate reports that the shape mismatch branch is “probably fine” because the outer tensor shape still matches.

### Why that report is incomplete
- Outer shape agreement can hide a wrong inner split.
- A mask row can be the wrong pattern while still matching the expected matrix size.
- A logits tensor can have the right rank while using the wrong last dimension.

### Better response
Ask for one decision checklist, one explicit tuple, and one statement of the intended invariant.


## Focused follow-up checks
- Confirm that the shape mismatch example can be restated as one tuple, one rule, and one failure symptom.
- Re-run the example mentally after swapping the anchor from `decision checklist` to a second artifact.
- Ask whether the same reasoning would still work if sequence length changed from 4 to 7.

## One concrete failure mode
- A reviewer may accept the outer shape while missing that the inner shape mismatch width changed too early.
- Another reviewer may describe the issue abstractly instead of showing the exact decision checklist.
- The repair-aware move is to print or tabulate the state before and after the suspect step.

## Reader exercise
- Write one additional assertion that protects the shape mismatch invariant.
- Rewrite one sentence so it names the axis or score row directly instead of alluding to it.
- Compare the current toy case against a second case where the decision checklist exposes a different mistake.

## Closing takeaway
This file is only useful if the learner can explain the shape mismatch path with concrete evidence rather than topic-shaped prose.
