---
draft_status: candidate
topic_id: TRF-012
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC3
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
---

# Sequence Length and Mask Memory Cost

## Concept
The causal mask looks simple, but its size grows quickly with sequence length.
That growth matters because attention also scales with pairwise token interactions.

## Explanation
For sequence length `T`, a full causal pattern conceptually occupies a `[T, T]` grid.
If `T` doubles, the number of position pairs grows by roughly four times.
Even when the mask is shared across batches and heads, the attention scores it supports still grow quadratically.
That is one reason long context windows are expensive.

The mask itself is not always the largest tensor.
Attention scores often dominate because they may have shape `[B, H, T, T]`.
Still, understanding the mask's quadratic structure helps learners see why sequence length is such an influential hyperparameter.

## Minimal Example
At `T=128`, the mask pattern spans 16,384 position pairs.
At `T=512`, it spans 262,144 pairs.
The growth is much faster than the token count alone.

## Common Pitfalls
A common mistake is to talk about long-sequence cost only in terms of embeddings or feedforward layers.
Another is to assume mask storage and attention-score storage are identical tensors in every implementation.

## Review Notes
The educational goal here is not exact profiling.
It is to build the right intuition: longer sequences create many more token-to-token interactions.