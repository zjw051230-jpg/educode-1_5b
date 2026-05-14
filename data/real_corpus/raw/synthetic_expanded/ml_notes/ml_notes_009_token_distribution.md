# Vocabulary Item Distribution Notes

Project-authored synthetic educational example for controlled corpus expansion.

## What distribution means here
A tokenizer maps text into ids, and some ids appear far more often than others.
That frequency pattern shapes what the model sees during training.

## Frequent items
Frequent ids often correspond to common punctuation, whitespace fragments, keywords, or short subword pieces.
They dominate early gradient signal.

## Rare items
Rare ids may represent uncommon code fragments, Chinese phrases, or unusual spelling patterns.
They matter, but a tiny corpus may not revisit them often enough.

## Why this matters
- train loss can look healthy while rare patterns remain underexposed
- a small corpus may give a narrow frequency profile
- adding steps does not create new variety by itself

## Practical observation
When corpus breadth is low, the model keeps seeing the same common fragments.
That can encourage memorization-like behavior on the training path.

## Summary
The distribution of vocabulary items is part of the data bottleneck.
More optimization steps cannot replace a wider range of educational examples.
