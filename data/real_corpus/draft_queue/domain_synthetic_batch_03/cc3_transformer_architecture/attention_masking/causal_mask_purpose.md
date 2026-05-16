---
draft_status: candidate
topic_id: TRF-008
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC3
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
---

# Purpose of the Causal Mask

## Concept
The causal mask prevents a token position from attending to future positions.
Without it, a decoder-only model could see answers it is supposed to predict.

## Explanation
During next-token training, position `t` should use only positions `0` through `t`.
If it could inspect `t + 1`, the learning problem would become artificially easy.
The model would learn from information that will not exist during generation.
The causal mask enforces the same information boundary used at inference time.

A common implementation uses a lower-triangular pattern.
Entries on or below the diagonal are allowed.
Entries above the diagonal are blocked.
The mask is usually applied to attention scores before softmax.
Blocked entries receive a very large negative value so their probability becomes effectively zero.

## Minimal Example
For sequence length 4, position 2 may attend to positions 0, 1, and 2.
It may not attend to position 3.
That allowed region forms a triangle in the attention matrix.

## Common Pitfalls
One pitfall is to say the current token must also be hidden.
In standard decoder self-attention, the current position is allowed.
Another pitfall is applying the mask after softmax instead of before it.

## Review Notes
The causal mask is not an optional training trick.
It is part of the architecture that makes autoregressive prediction well defined.