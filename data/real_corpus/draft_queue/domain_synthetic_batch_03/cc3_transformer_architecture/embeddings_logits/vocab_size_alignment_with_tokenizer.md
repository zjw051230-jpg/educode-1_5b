---
draft_status: candidate
topic_id: TRF-016
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC3
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
---

# Vocab Size Alignment with the Tokenizer

## Concept
The model vocabulary size must match the tokenizer vocabulary size.
If they disagree, the data pipeline and the model no longer share the same token-id contract.

## Explanation
The tokenizer defines which integer ids appear in training examples.
The embedding table expects those ids to be inside the valid range.
The final logits layer also assumes the same vocabulary size when scoring possible next tokens.
A mismatch can break the system at either end.

If the embedding table is too small, valid token ids may be out of range.
If the logits layer is misaligned, the model may allocate outputs for nonexistent ids or fail to score legal ones.
This is why vocabulary size alignment is not a minor detail.
It is a core architectural interface.

## Minimal Example
Suppose the tokenizer produces ids from 0 to 8191.
Then both the input embedding table and the final logits projection need vocabulary size 8192.
Any different value should trigger a configuration review.

## Common Pitfalls
One pitfall is to update tokenizer artifacts without updating model config.
Another is to focus only on the embedding side and forget the logits side must agree too.

## Review Notes
Vocabulary alignment is easy to overlook because it feels like setup.
In practice, it is one of the simplest ways to prevent shape and indexing errors across the full training stack.