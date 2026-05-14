# Overfitting on a Small Corpus

A model can overfit quickly when the corpus is tiny and repetitive.
This happens even faster when the model is large relative to the dataset.
The training loss may fall sharply while the data diversity stays narrow.

Typical signs in a small educational corpus:
- the same phrases appear across many notes
- the same code patterns repeat often
- validation content is too similar to training content
- generation starts echoing familiar fragments

For engineering milestones, fast overfitting is not always bad.
It can help confirm that:
- gradients are flowing
- optimizer steps update weights
- checkpoint reload works
- the model can memorize a bounded pattern

But overfitting is a poor proxy for meaningful pretraining.
A good systems milestone is not the same as a good data milestone.
That is why this project now treats corpus scale as a bottleneck.
A larger approved corpus is needed before longer training becomes informative.
