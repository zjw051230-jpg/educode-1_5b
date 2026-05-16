---
draft_status: candidate
topic_id: TRF-006
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC3
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
---

# Learned Position Embeddings vs RoPE

## Concept
A decoder-only model needs position information because token embeddings alone do not encode order.
Learned position embeddings and RoPE supply that information in different ways.

## Explanation
Learned position embeddings assign a trainable vector to each position index.
A model usually adds the token embedding and the position embedding before the first decoder block.
This is direct and easy to visualize.
It also makes the position mechanism easy to separate conceptually from attention.

RoPE, or rotary position embedding, changes how queries and keys interact inside attention.
Instead of adding a separate position vector to the residual stream, it rotates feature pairs according to position.
That means positional information affects attention geometry directly.
The ordering signal appears in how dot products are formed, not only in the input representation.

## Minimal Example
With learned embeddings, position 0 and position 1 contribute different trainable vectors before any block runs.
With RoPE, position 0 and position 1 rotate query and key features differently before attention scores are computed.
Both methods communicate order.
They simply place order information in different parts of the pipeline.

## Common Pitfalls
A common mistake is to say RoPE removes positional encoding.
It does not remove it; it changes the mechanism.
Another mistake is to compare the two methods only by convenience and ignore their architectural meaning.

## Review Notes
For a very small teaching model, learned position embeddings are easier to introduce first.
For modern architecture discussions, RoPE is important because it changes how many people think about positional structure in attention.