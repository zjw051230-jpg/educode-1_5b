# Overfit Detection Notes

Project-authored synthetic educational example for controlled corpus expansion.

## Basic signal
Overfitting often appears when training loss keeps improving while validation loss stalls or worsens.
That pattern suggests the model is fitting the training set more specifically than the held-out split.

## Why tiny datasets are tricky
With a very small validation split, the signal can be noisy.
A single bad validation point is not enough to make a sweeping conclusion.

## Still useful
Even noisy validation trends are worth watching in bounded experiments.
They help decide whether adding more steps is likely to improve learning or just memorize the available examples.

## Practical takeaway
If longer runs keep lowering train loss but do not improve validation, expanding the corpus may be more valuable than increasing step count.

## Summary
Overfit detection is less about a single number and more about how train and validation behavior diverge over time.