# Cross Entropy for Language Modeling

Cross entropy compares the model distribution with the correct next-token label.
For each position, the model emits logits over the vocabulary.
Those logits are converted into a probability distribution.
The loss is lower when the correct token gets higher probability.

A small example:
- target token id: `42`
- predicted probability for token `42`: `0.70`
- predicted probability for many wrong tokens: small values

In that case the contribution to loss is lower than a flat distribution.
If the model is uncertain and spreads probability across many tokens, loss rises.

In this repo, cross entropy is useful because it gives one scalar that can be tracked:
- after one forward pass
- across several smoke steps
- across training and validation batches

Cross entropy is informative, but context matters.
A low loss on a tiny synthetic corpus may only show memorization pressure.
A stable finite loss during smoke tests is still valuable.
It proves the forward path, label alignment, and optimization loop are connected.
