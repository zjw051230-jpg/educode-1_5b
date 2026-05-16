---
draft_status: candidate
topic_id: MLF-013
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-1
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
---

# How Random Seeds Affect Tiny Experiments

## Concept
Random seeds influence initialization, data order, and sometimes dropout masks.
In tiny experiments, those choices can noticeably change the observed loss curve.

## Explanation
This is not a flaw in the idea of training.
It is a reminder that small datasets provide less averaging over randomness.

Consider two short runs with the same model and learning rate.
One seed may start with output weights that accidentally favor common tokens in the training split.
Another seed may start farther away, making early loss look worse.

The train/validation split can amplify this effect.
If the validation slice is tiny, a different shuffle or sampled order can make generalization look better or worse than it really is.

Seeds also interact with overfitting judgments.
A single seed producing a small val improvement is evidence, but weak evidence.
A pattern that survives several seeds is more convincing.

## Minimal Example
Two seeds may produce:
- seed A: train loss drops fast, val loss improves slightly
- seed B: train loss drops slower, val loss stays flat
The recipe is the same, but the visible path differs.

## Common Pitfalls
- Drawing strong conclusions from one seed on a tiny split
- Forgetting that token distribution can align differently with initialization
- Treating stochastic variation as proof of a code bug

## Review Notes
Reproducible seeds are still valuable.
They let a reviewer distinguish real code changes from ordinary stochastic variation.
