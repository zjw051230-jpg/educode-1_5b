---
draft_status: candidate
topic_id: B05-TRF-0023
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-3
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---

# Checking packed QKV against split heads (QKV head split)

## Bug diary excerpt
Symptom: a tiny QKV head split demo passed shape checks at the input boundary but failed after one later transformation.

### Day 1 observation
- The first healthy line was `(batch=2, seq=6, width=16)`.
- The suspicious line appeared after a small pseudo-run log.

### Day 2 narrowing step
- Freeze the toy input.
- Write down the intended shape after each transition.
- Refuse to trust any reshape that is not justified by a printed tuple.

### Resolution
The real fix was not “understand transformers better”; it was naming the exact QKV head split invariant and checking it earlier.


## Focused follow-up checks
- Confirm that the QKV head split example can be restated as one tuple, one rule, and one failure symptom.
- Re-run the example mentally after swapping the anchor from `small pseudo-run log` to a second artifact.
- Ask whether the same reasoning would still work if sequence length changed from 5 to 6.

## One concrete failure mode
- A reviewer may accept the outer shape while missing that the inner QKV head split width changed too early.
- Another reviewer may describe the issue abstractly instead of showing the exact small pseudo-run log.
- The repair-aware move is to print or tabulate the state before and after the suspect step.

## Reader exercise
- Write one additional assertion that protects the QKV head split invariant.
- Rewrite one sentence so it names the axis or score row directly instead of alluding to it.
- Compare the current toy case against a second case where the small pseudo-run log exposes a different mistake.

## Closing takeaway
This file is only useful if the learner can explain the QKV head split path with concrete evidence rather than topic-shaped prose.
