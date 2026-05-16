---
draft_status: candidate
topic_id: TRF-013
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC3
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
---

# Batch-First Attention Notes

## Concept
Many educational codebases use batch-first tensors with shape `[batch, time, channels]`.
That convention makes attention shape discussions easier to follow.

## Explanation
With batch-first format, the input hidden state usually has shape `[B, T, D]`.
Projection layers keep the batch and time axes while changing feature channels.
After splitting heads, many implementations move to `[B, H, T, d_head]`.
Attention scores then become `[B, H, T, T]`.

This format is intuitive because the first axis always means separate examples.
The second axis always means token positions.
Any transpose that appears later is usually about computation order, not about changing the meaning of batch or time.

## Minimal Example
Suppose two sequences of length four are processed together.
The hidden tensor shape is `[2, 4, D]`.
Attention never mixes token positions across the batch axis.
It mixes positions inside each example only.

## Common Pitfalls
A common mistake is to treat `T` like a feature axis.
Another is to see a transpose in code and assume the model semantics changed.
Usually the transpose only prepares the tensor for matrix multiplication.

## Review Notes
Batch-first notation is not the only convention, but it is often the clearest for beginners.
It keeps time visible in later discussions about masks, logits, and shifted targets.