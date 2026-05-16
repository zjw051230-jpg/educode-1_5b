---
draft_status: candidate
topic_id: TRF-001
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC3
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
---

# Decoder-Only Language Modeling Overview

## Concept
A decoder-only transformer predicts the next token from the tokens that already appeared.
It is designed for left-to-right generation rather than full-sentence encoding.
The core rule is that each position can use the past but not the future.

## Explanation
Inputs usually begin as token ids with shape `[batch, time]`.
An embedding table maps those ids into vectors with shape `[batch, time, d_model]`.
Position information is added so the model can tell early and late tokens apart.
The hidden states then flow through a stack of decoder blocks.

Each decoder block contains masked self-attention.
That attention lets one position gather evidence from earlier positions.
Each block also contains a feedforward layer.
That layer transforms features inside the current position.
Residual connections keep earlier information available.
Layer norm helps stabilize feature scales.

After the final block, the model applies a projection into vocabulary logits.
The output shape becomes `[batch, time, vocab_size]`.
Training compares each position against the next token in the sequence.
This makes decoder-only transformers natural next-token predictors.

## Minimal Example
In the sequence `the cat sleeps`, the position for `sleeps` may use `the cat` as context.
The position for `cat` may use `the` as context.
No position should use a token that appears later in the sequence.
That rule keeps training consistent with generation.

## Common Pitfalls
A common mistake is to describe the model as if it could inspect the whole sentence while predicting.
Another is to forget that labels are shifted relative to inputs.
It is also easy to lose track of shape flow once attention splits into heads.

## Review Notes
A useful summary is: embeddings create token vectors, decoder blocks refine them, and logits score possible next tokens.
The whole architecture is organized around causal prediction.