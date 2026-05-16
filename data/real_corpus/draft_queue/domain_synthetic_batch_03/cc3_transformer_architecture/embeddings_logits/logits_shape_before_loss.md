---
draft_status: candidate
topic_id: TRF-018
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC3
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
---

# Expected Logits Shape Before Loss

## Concept
Before cross-entropy is computed, a decoder-only model usually produces one vocabulary-sized score vector per token position.
That leads to the standard outer shape `[batch, time, vocab_size]`.

## Explanation
After the final decoder block, hidden states still have shape `[B, T, D]`.
A linear projection maps each `D`-dimensional vector into `V` scores, where `V` is vocabulary size.
The logits therefore have shape `[B, T, V]`.
Each time step gets its own candidate distribution over next tokens.

Targets usually begin with shape `[B, T]` after shifting.
Loss code often flattens logits to `[B * T, V]` and targets to `[B * T]` for convenience.
That flattening is part of the loss interface.
It does not change the fact that the model predicts at every token position.

## Minimal Example
If `B=2`, `T=5`, and `V=1000`, the logits shape is `[2, 5, 1000]`.
That means there are ten position-level prediction vectors in the batch.
Each one scores all 1000 possible next-token classes.

## Common Pitfalls
A common mistake is to confuse hidden width `D` with vocabulary size `V`.
Another is to think the model predicts one vocabulary vector for the whole sequence during training.
Teacher forcing produces one prediction per position.

## Review Notes
A good way to remember the shape is to ask what question the model answers at each step.
It answers: what token should come next here?
That question requires one full vocabulary score vector per position.