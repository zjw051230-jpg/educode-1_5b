---
draft_status: candidate
topic_id: TRF-002
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC3
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
---

# Transformer Block Data Flow

## Concept
A transformer block updates hidden states while keeping the outer shape unchanged.
The important question is not whether the shape changes, but how the information changes.

## Explanation
Suppose the incoming tensor has shape `[B, T, D]`.
Layer norm first rescales features within each token position.
Masked self-attention then reads from earlier positions and produces an update of shape `[B, T, D]`.
That update is added back to the residual stream.

A second layer norm prepares the tensor for the feedforward sublayer.
The feedforward network usually expands channels from `D` to a wider internal size.
A nonlinearity transforms those wider features.
A final projection returns the width back to `D`.
That result is also added to the residual stream.

## Minimal Example
One token may begin with a rough feature such as `is a noun`.
Attention may add context such as `comes after an article`.
Feedforward may sharpen the combination into a more useful local feature.
The token leaves the block with the same width but richer meaning.

## Common Pitfalls
A common confusion is to treat attention and feedforward as doing the same job.
Attention moves information across positions.
Feedforward transforms information inside one position.
Another confusion is to describe the sublayer output as a replacement rather than an addition.

## Review Notes
A decoder stack is mostly repetition of this block pattern.
Once the learner can trace one block, the whole stack becomes easier to reason about.