---
draft_status: candidate
topic_id: MLF-016
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-1
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
---

# Lower Train Loss but Worse Validation Loss

## Concept
This pattern is one of the clearest warning signs in small language-model experiments.
The training objective is improving on seen data while held-out performance moves in the wrong direction.

## Explanation
The first interpretation is overfitting.
The model is adapting to details specific to the training split rather than learning patterns that transfer.

But overfitting is not the only possibility.
A mismatch in tokenization, loss masking, or label shift between train and validation pipelines can also create this divergence.

That is why the pattern should trigger both conceptual and mechanical checks.
- are train and val computing the same next-token objective?
- do they use the same vocabulary and padding rules?
- is the validation split representative enough to trust?

If the mechanics are aligned, then optimizer behavior becomes the main story.
A learning rate that is slightly too aggressive can drive rapid specialization to the training set before validation can benefit.

## Minimal Example
If training batches overuse common endings, the model can harvest cheap train-loss wins.
Validation with a different ending mix then receives little benefit and may worsen.

## Common Pitfalls
- Assuming the divergence must be a code bug
- Ignoring token-distribution mismatch across splits
- Overreacting to one small noisy validation increase

## Review Notes
Train loss alone is incomplete evidence about what the model has actually learned.
