---
draft_status: candidate
topic_id: B05-TRF-0051
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-3
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---

# Tracing head width after projection (QKV head split)

## Opening question
What should a reviewer inspect first when a QKV head split example looks plausible but one dimension is silently wrong?

## Learning objective
verify head split arithmetic from d_model to head_dim; file 0051 uses a config snippet to keep the lesson specific.

## Toy artifact
- batch = 2
- seq = 6
- d_model = 20
- heads = 4
- anchor = config snippet

## Shape trace
1. start hidden: `(2, 6, 20)`
2. project or inspect the QKV head split path before any silent broadcast
3. compare the expected inner width against the observed trace
4. mark the first line where the invariant breaks

## Why this case matters
The file avoids generic transformer narration by staying inside one concrete QKV head split example.
The reader should leave with a repeatable debugging move instead of a vague review note.

## Quick decision checklist
- Is the outer batch/sequence shape preserved?
- Does the inner width match the intended head or vocab rule?
- Can the mismatch be proven with one printed tuple?
- Would a smaller toy case expose the same bug?


## Focused follow-up checks
- Confirm that the QKV head split example can be restated as one tuple, one rule, and one failure symptom.
- Re-run the example mentally after swapping the anchor from `config snippet` to a second artifact.
- Ask whether the same reasoning would still work if sequence length changed from 6 to 6.

## One concrete failure mode
- A reviewer may accept the outer shape while missing that the inner QKV head split width changed too early.
- Another reviewer may describe the issue abstractly instead of showing the exact config snippet.
- The repair-aware move is to print or tabulate the state before and after the suspect step.

## Reader exercise
- Write one additional assertion that protects the QKV head split invariant.
- Rewrite one sentence so it names the axis or score row directly instead of alluding to it.
- Compare the current toy case against a second case where the config snippet exposes a different mistake.

## Closing takeaway
This file is only useful if the learner can explain the QKV head split path with concrete evidence rather than topic-shaped prose.
