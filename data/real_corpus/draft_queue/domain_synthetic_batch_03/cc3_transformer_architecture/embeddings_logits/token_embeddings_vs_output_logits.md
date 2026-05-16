---
draft_status: candidate
topic_id: TRF-015
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC3
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
---

# Token Embeddings vs Output Logits

## Concept
Token embeddings and output logits both involve the vocabulary dimension, but they point in opposite directions.
Embeddings map token ids into vectors.
Logits map vectors into scores over the vocabulary.

## Explanation
At the input side, an embedding table with shape `[vocab_size, d_model]` converts each token id into a dense feature vector.
Those vectors enter the decoder stack and become context-aware hidden states.
At the output side, a projection maps each hidden state into `vocab_size` scores.
That produces logits with shape `[B, T, vocab_size]`.

The similarity in shapes can hide the difference in roles.
Embeddings answer, `How should this token be represented?`
Logits answer, `How plausible is each next token?`
One is a lookup-like input interface.
The other is a classification-style output interface.

## Minimal Example
If token id 17 corresponds to `cat`, the embedding table returns one vector for that id.
After contextual processing, the output projection returns one score for every vocabulary item.
A high score for another id may indicate the model expects `sleeps` next.

## Common Pitfalls
A common mistake is to call logits probabilities.
They are raw scores before softmax.
Another is to blur the distinction between an embedding table and an output classifier just because both mention vocabulary size.

## Review Notes
This input-output contrast is a useful teaching anchor.
The model enters through embeddings, reasons through hidden states, and exits through logits.