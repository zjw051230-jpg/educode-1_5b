---
draft_status: candidate
topic_id: B05-MLF-0063
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-1
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---


# Clip Before Optimizer Step

Instead of summarizing gradients in abstract terms, this file assembles the exact clues a reviewer would inspect.
The learning objective is specific: Use a step trace to explain why clipping must be read in relation to the optimizer step.
This note is written as a evidence-first checklist and uses a mini code trace as the concrete anchor.

## Evidence before naming the bug
- topic_id: B05-MLF-0063
- subdirectory: gradient_behavior
- focus: clip_before_optimizer_step
- reader task: explain the metric shift without falling back to a generic review script

## Signals that matter
| checkpoint | train_loss | val_loss | note |
| --- | ---: | ---: | --- |
| 1 | 2.100 | 2.320 | baseline batch |
| 2 | 2.220 | 2.440 | slightly harder slice |
| 3 | 2.340 | 2.560 | evaluation window drift |
| 4 | 2.370 | 2.590 | post-fix reread |

Mini code trace:
```text
shifted_targets = targets[:, 1:]
trimmed_logits   = logits[:, :-1, :]
loss = cross_entropy(trimmed_logits.reshape(-1, vocab), shifted_targets.reshape(-1))
```

## Signals that can mislead
The first trap in clip before optimizer step is to turn one scalar into a universal rule.
Here the train values 2.100, 2.220, and 2.340 only become meaningful after the validation path 2.320, 2.440, and 2.560 is inspected alongside the scenario details.
A second trap is to ignore which examples dominate the average. In this topic, the concrete anchor matters because it localizes where the loss story changes shape.

## Minimal intervention
Before the correction, the working story was based on this series: 2.100, 2.220, 2.340, 2.370.
After adding the topic-specific check, the team would retell the run using: 2.320, 2.440, 2.560, 2.590.
That difference is small enough to miss in a dashboard and large enough to change a decision about loss/validation/overfitting behavior.

## Escalation rule
- Which piece of evidence is unique to this topic rather than generic to all training runs?
- What would still look suspicious if the metric scalar were removed from the page?
- Which follow-up trace would separate a logging problem from a model-behavior problem?

Closing note: the educational value of this draft comes from tying one exact failure or comparison to one exact reading habit.
