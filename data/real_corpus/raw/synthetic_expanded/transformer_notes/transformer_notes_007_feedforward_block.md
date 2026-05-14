# Feedforward Block Notes

Project-authored synthetic educational example for controlled corpus expansion.

## Role in the stack
After attention mixes information across positions, the feedforward block transforms each position independently.

## Conceptual form
```text
x -> linear up -> activation -> linear down
```

## Why it matters
The feedforward block provides much of the per-position capacity.
Attention handles routing, but the feedforward sublayer helps build richer representations.

## Common choices
- ReLU
- GELU
- SwiGLU-style gated variants

## Capacity tradeoff
A wider feedforward dimension increases model size and computation.
That must be balanced against available hardware and the project stage.

## Tiny synthetic setting
In a bounded local run, the feedforward block mostly serves as part of end-to-end pipeline validation.
Train loss going down does not imply that its learned features are broadly useful.

## Summary
The feedforward block is a major source of model capacity, but its value is only as meaningful as the data and evaluation behind it.
