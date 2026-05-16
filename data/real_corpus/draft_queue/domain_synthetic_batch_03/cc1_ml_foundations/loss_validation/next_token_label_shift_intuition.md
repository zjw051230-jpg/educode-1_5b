---
draft_status: candidate
topic_id: MLF-002
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-1
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
---

# Why Next-Token Labels Are Shifted by One Position

A next-token model should not be trained to repeat the token it already sees at the same position.
Instead, each hidden state is asked to predict the token immediately to its right.

Take a synthetic sequence: [BOS, blue, birds, sing].
Input positions can be [BOS, blue, birds].
Targets become [blue, birds, sing].
The shift creates a clean supervised signal from prefix to continuation.

Without the shift, the model could learn a trivial identity-like mapping in some architectures or tooling setups.
That would produce misleadingly low training loss without teaching generation behavior.

The label shift also explains why the final token often has no direct next-token label inside a fixed sequence window.
There is nothing after it unless an EOS token or a following packed token is included.

In tiny experiments, many apparent loss bugs come from shape agreement hiding semantic disagreement.
The logits tensor and target tensor may have compatible lengths, but each target may be attached to the wrong timestep.

A quick synthetic audit is to write the input and target text side by side.
- input:  the cat sat
- target: cat sat still
If the rows do not look like a one-token slide, the training objective is probably wrong.

Shifted labels matter for validation too.
If train uses shifted targets but validation forgets to shift, train loss and val loss no longer measure the same task.
That can create fake generalization gaps.

This convention also influences padding and masking.
When sequences have different lengths, the shifted target at padded positions must be ignored so the model is not punished for synthetic filler tokens.

From an optimization view, the shift tells each hidden state what information it was supposed to preserve from the prefix.
A hidden state after token blue is useful only if it helps predict birds, not blue again.

The simplest rule is this: model state at index t should be judged by token t+1.
That rule keeps training, evaluation, and generation aligned.
