# Train and Validation Split Notes

Project-authored synthetic educational example for controlled corpus expansion.

## Purpose of a split
A train and validation split separates optimization data from review data.

## Why document-level split helps
- it reduces leakage across highly similar examples
- it makes later interpretation easier
- it prevents the same short note from appearing in both paths

## Good habits
- choose a deterministic split rule
- keep the seed fixed for reproducibility
- record the number of train and validation documents
- keep split artifacts under versioned project logic

## What a split should avoid
- mixing nearly identical duplicates across both sets
- changing the split every time a script runs
- treating validation text as if it were hidden test data

## Small-corpus reality
A tiny split is better than no split, but it remains weak evidence.
On a very small project-authored corpus, the split mainly helps inspect stability.

## Example workflow
```text
raw files -> cleaned records -> deterministic split -> train.jsonl + val.jsonl
```

## Summary
A train/validation split is one of the simplest controls in training work, and one of the easiest to weaken by accident if the procedure is not explicit.
