---
draft_status: candidate
topic_id: TRF-004
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC3
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
---

# Role of the Feedforward Layer

## Concept
The feedforward sublayer transforms each token position independently.
Its job is local feature computation, not communication across positions.

## Explanation
Given hidden states of shape `[B, T, D]`, the feedforward network applies the same small neural network at every position.
A common pattern is `D -> 4D -> D`.
The wider internal dimension gives the model room to form richer intermediate features.
The nonlinearity lets the model represent behavior that a single linear map cannot express.
The final projection returns the outer shape to `[B, T, D]`.

Attention answers which earlier tokens matter.
Feedforward answers how to transform the information now present at the current token.
These are different roles.
A transformer block depends on both of them.

## Minimal Example
Attention may reveal that the current token is inside a numbered list.
The feedforward layer can turn that hint into a stronger local feature such as `expect punctuation` or `expect another item`.
No new positions are read during this step.

## Common Pitfalls
A common mistake is to treat the feedforward layer as an unimportant extra depth.
Another is to forget that the same feedforward weights are reused at all time steps.
It is also easy to miss the importance of the internal width expansion.

## Review Notes
A practical teaching phrase is: attention communicates, feedforward computes.
That summary is simplified, but it separates the two roles clearly.