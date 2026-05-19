---
draft_status: candidate
topic_id: B05-TRF-0092
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-3
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---

# Why untied output heads reveal width bugs faster (logits projection)

## Mini lab prompt
You are given a logits projection trace and one failing assertion. Repair the interpretation before touching code.

### Observed trace
```
step0 hidden -> (2, 5, 17)
step1 artifact -> (2, 3, 5, 7)
step2 note -> numeric toy example
```

### Questions
- Which axis should be compared first for this logits_projection example?
- Which dimension is structural and which is data-dependent?
- What one-line print would remove the ambiguity?

### Worked answer
This lab treats the logits projection as a small evidence trail rather than a textbook section.
The repair move is to align the printed tuple with the intended invariant named in the title.


## Focused follow-up checks
- Confirm that the logits projection example can be restated as one tuple, one rule, and one failure symptom.
- Re-run the example mentally after swapping the anchor from `numeric toy example` to a second artifact.
- Ask whether the same reasoning would still work if sequence length changed from 5 to 7.

## One concrete failure mode
- A reviewer may accept the outer shape while missing that the inner logits projection width changed too early.
- Another reviewer may describe the issue abstractly instead of showing the exact numeric toy example.
- The repair-aware move is to print or tabulate the state before and after the suspect step.

## Reader exercise
- Write one additional assertion that protects the logits projection invariant.
- Rewrite one sentence so it names the axis or score row directly instead of alluding to it.
- Compare the current toy case against a second case where the numeric toy example exposes a different mistake.

## Closing takeaway
This file is only useful if the learner can explain the logits projection path with concrete evidence rather than topic-shaped prose.
