---
draft_status: candidate
topic_id: TRF-009
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC3
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
---

# Attention Mask Shapes Explained

## Concept
Attention masks can be confusing because they interact with batch size, number of heads, and sequence length.
The safest approach is to track the shape of the attention score tensor first.

## Explanation
In multi-head self-attention, attention scores often have shape `[B, H, T, T]`.
The last two axes compare query positions against key positions.
A causal mask may begin as `[T, T]`.
Broadcasting can then expand it across batch and head dimensions.

Some implementations explicitly materialize shapes such as `[1, 1, T, T]`.
Others combine causal masking with batch-specific padding masks.
The exact shape can differ, but the semantic goal is the same.
Future positions must be blocked for every query position.

## Minimal Example
If `B=2`, `H=4`, and `T=5`, then the score tensor has shape `[2, 4, 5, 5]`.
A causal mask with shape `[5, 5]` can still work if broadcasting is set up correctly.
That mask does not need a separate copy for every head unless the implementation chooses to make one.

## Common Pitfalls
A common mistake is to match the mask to `[B, T, D]` instead of the attention scores.
Another is to forget that broadcasting rules are part of the implementation contract.

## Review Notes
When a learner asks which mask shape is correct, a good answer is: any shape that broadcasts correctly to the attention score tensor and blocks future positions.