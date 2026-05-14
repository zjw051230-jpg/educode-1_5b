# Causal Mask

A causal mask prevents position `t` from attending to positions after `t`.
Without this rule, the model could peek at future tokens.
That would break the next-token objective.

A simple shape idea:
- sequence length: `4`
- allowed attention:
  - token 0 sees 0
  - token 1 sees 0, 1
  - token 2 sees 0, 1, 2
  - token 3 sees 0, 1, 2, 3

The mask is a training-time correctness rule.
It is not only a math detail.
If the mask is wrong, loss can look artificially better.
That would make the systems result misleading.

In smoke tests, causal masking helps validate that:
- logits align with labels
- sequence order is respected
- attention logic matches the decoder-only design
