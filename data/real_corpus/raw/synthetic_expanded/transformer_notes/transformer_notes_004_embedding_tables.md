# Embedding Table Notes

Project-authored synthetic educational example for controlled corpus expansion.

## What an embedding table does
An embedding table maps integer ids to dense vectors.
Those vectors become the model's starting representation of discrete input items.

## Why it exists
A neural network cannot directly operate on symbolic ids in a meaningful way.
The embedding table turns each id into a learned continuous representation.

## Common shape
```text
[vocab_size, d_model]
```

## Practical consequence
Larger vocabulary size increases the embedding table size.
That affects memory even before attention or feedforward blocks are considered.

## Small synthetic corpus reminder
A small corpus may not train every row equally well.
Many ids can remain underexposed if the text distribution is narrow.

## Summary
Embedding tables are simple conceptually, but their training quality depends heavily on vocabulary coverage and corpus diversity.
