---
draft_status: candidate
topic_id: TRF-011
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC3
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
---

# Why Future Tokens Must Be Hidden

## Concept
A decoder-only model generates text one step at a time.
Future tokens must stay hidden during training so the model practices the same task it will face later.

## Explanation
If training allowed position `t` to inspect the true token at `t + 1`, the model would learn from information that will not exist at generation time.
That would produce a mismatch between the objective and deployment behavior.
The model might achieve low training loss while learning poor causal reasoning.

The hidden-future rule aligns training with inference.
At training time, the model is asked what should come next given a prefix.
At generation time, it answers the same question repeatedly.
The causal mask keeps both settings consistent.

## Minimal Example
Suppose the prefix is `the glass fell and`.
The model should infer a likely continuation from that prefix alone.
If it secretly sees `shattered`, the task is no longer true prediction.
It becomes leakage.

## Common Pitfalls
A common mistake is to confuse data availability with architectural permission.
Even if the full sequence exists in memory, future tokens are still forbidden inputs for a causal decoder.

## Review Notes
Hiding future tokens is not about making the problem difficult on purpose.
It is about preserving the integrity of next-token learning.