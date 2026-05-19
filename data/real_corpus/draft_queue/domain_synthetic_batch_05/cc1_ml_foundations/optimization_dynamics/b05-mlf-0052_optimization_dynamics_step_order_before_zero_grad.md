---
draft_status: candidate
topic_id: B05-MLF-0052
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-1
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---


# Step Order Before Zero-Grad

The explanation starts from a changed knob and follows its downstream effects on the curve.
The learning objective is specific: Use a trace to show how incorrect step order creates optimization artifacts.
This note is written as a what-changed analysis and uses a mini code trace as the concrete anchor.

## Baseline and modified run
- topic_id: B05-MLF-0052
- subdirectory: optimization_dynamics
- focus: step_order_before_zero_grad
- reader task: explain the metric shift without falling back to a generic review script

## What changed first
| checkpoint | train_loss | val_loss | note |
| --- | ---: | ---: | --- |
| 1 | 2.460 | 2.680 | baseline batch |
| 2 | 2.580 | 2.800 | slightly harder slice |
| 3 | 2.610 | 2.830 | evaluation window drift |
| 4 | 2.730 | 2.950 | post-fix reread |

Mini code trace:
```text
shifted_targets = targets[:, 1:]
trimmed_logits   = logits[:, :-1, :]
loss = cross_entropy(trimmed_logits.reshape(-1, vocab), shifted_targets.reshape(-1))
```

## Downstream metric shift
The first trap in step order before zero-grad is to turn one scalar into a universal rule.
Here the train values 2.460, 2.580, and 2.610 only become meaningful after the validation path 2.680, 2.800, and 2.830 is inspected alongside the scenario details.
A second trap is to ignore which examples dominate the average. In this topic, the concrete anchor matters because it localizes where the loss story changes shape.

## Why the new setting behaved this way
Before the correction, the working story was based on this series: 2.460, 2.580, 2.610, 2.730.
After adding the topic-specific check, the team would retell the run using: 2.680, 2.800, 2.830, 2.950.
That difference is small enough to miss in a dashboard and large enough to change a decision about loss/validation/overfitting behavior.

## Re-test checklist
- Which piece of evidence is unique to this topic rather than generic to all training runs?
- What would still look suspicious if the metric scalar were removed from the page?
- Which follow-up trace would separate a logging problem from a model-behavior problem?

Closing note: the educational value of this draft comes from tying one exact failure or comparison to one exact reading habit.
