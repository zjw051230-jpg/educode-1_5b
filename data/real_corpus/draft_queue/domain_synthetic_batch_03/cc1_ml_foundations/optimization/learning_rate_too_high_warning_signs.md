---
draft_status: candidate
topic_id: MLF-010
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-1
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
---

# Warning Signs of an Excessive Learning Rate

## Concept
A learning rate that is too high does not just make training fast.
It can make updates so large that the model repeatedly overshoots better regions of parameter space.

## Explanation
One warning sign is loss that refuses to settle.
Train loss may jump down and then sharply up across adjacent steps rather than showing noisy but directional progress.

Another sign is non-finite values appearing only after optimizer steps.
If the forward pass is finite before training but NaNs emerge after several updates, the step size is a plausible cause.

Validation loss often becomes erratic as well.
When the optimizer keeps leaping, small improvements on one batch may be erased on the next, and held-out behavior can look unstable or random.

Gradient norms can offer a clue, but they are not the whole story.
Large gradients with a sensible learning rate may still be manageable.
Moderate gradients multiplied by an excessive rate can still produce harmful parameter jumps.

## Minimal Example
If one batch mostly contains easy repeated tokens, a large step may tune the model too hard toward that pattern.
The next batch, containing rarer structures, then suffers dramatically.
That can produce a misleading early drop followed by oscillation.

## Common Pitfalls
- Mistaking an early fast drop for healthy optimization
- Relying on clipping to hide a bad step size
- Judging stability only from one or two batches

## Review Notes
In small training loops, the best rate is usually the one that moves decisively without making the optimization story chaotic.
