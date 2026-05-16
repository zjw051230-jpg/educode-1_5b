---
draft_status: candidate
topic_id: MLF-001
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-1
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
---

# Cross-Entropy for Next-Token Prediction

A tiny decoder predicts one token at each position, but the training target is the next token rather than the current token.
That shift makes the objective match generation: given the prefix, estimate the probability of what comes next.

Consider a synthetic batch with token ids like [4, 8, 2, 9].
The model receives [4, 8, 2] as context positions and is judged against [8, 2, 9] as labels.
Each position contributes one classification decision over the full vocabulary.

Cross entropy is useful because it punishes confident mistakes more than uncertain mistakes.
If the model gives token 9 a probability of 0.80 when 2 is correct, the loss is much worse than if it gave 2 a probability of 0.35 and several alternatives nearby.
This encourages not only correct ranking but calibrated confidence.

In a next-token setting, average loss is often easier to compare across runs than raw summed loss.
A longer sequence naturally creates more prediction events, so summing can make a stable run look worse only because it processed more positions.

A simple synthetic example helps:
- position 1 target = 8, model probability = 0.50
- position 2 target = 2, model probability = 0.25
- position 3 target = 9, model probability = 0.10
The third position dominates the average because the model is assigning too little mass to the truth.

When cross entropy falls over time, the model is usually improving one of two behaviors.
It may place more mass on the correct next token.
It may also become less overconfident on wrong alternatives, which indirectly helps the average objective.

A useful debugging question is whether the loss scale is plausible for the vocabulary size.
If logits are nearly random over many tokens, early loss should look fairly high.
If the initial loss is suspiciously tiny, one possibility is that labels are misaligned, masked incorrectly, or leaking the answer.

Cross entropy also interacts with token distribution.
If a corpus overuses a few easy tokens, the average loss can drop quickly even while rare structural tokens remain poorly modeled.
That is why inspection should combine scalar loss with sample predictions.

For educational tiny runs, the best mental model is simple.
Every token position is a supervised classification event.
Cross entropy summarizes how surprised the model still is by the true next token.
