# Decoder-Only Transformer Notes

A decoder-only transformer predicts the next token from left to right.
It does not look into future positions during training.
That left-to-right restriction is part of the model design.

Common components:
- token embedding
- positional information
- stacked attention and feed-forward blocks
- final projection into vocabulary logits

Why decoder-only works for this repo:
- it matches next-token prediction
- it keeps the training objective simple
- it supports generation after prompt tokens
- it scales from toy smoke runs to larger profiling runs

A decoder-only stack can still be expensive.
Parameter count rises with depth and width.
Memory use also depends on sequence length and activations.
That is why A100 smoke results were useful for scale validation.
