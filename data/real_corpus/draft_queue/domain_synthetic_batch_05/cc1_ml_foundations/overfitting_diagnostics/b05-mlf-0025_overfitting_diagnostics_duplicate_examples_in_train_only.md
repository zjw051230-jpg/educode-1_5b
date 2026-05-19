---
draft_status: candidate
topic_id: B05-MLF-0025
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-1
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---


# Duplicate Examples in Train Only

This file reads like a postmortem because the interesting part is the failure path, not the definition.
The learning objective is specific: Diagnose how duplicate training rows create a suspiciously smooth train curve.
This note is written as a failure postmortem and uses a debugging transcript as the concrete anchor.

## Incident setup
- topic_id: B05-MLF-0025
- subdirectory: overfitting_diagnostics
- focus: duplicate_examples_in_train_only
- reader task: explain the metric shift without falling back to a generic review script

## Evidence collected
| checkpoint | train_loss | val_loss | note |
| --- | ---: | ---: | --- |
| 1 | 2.570 | 2.790 | baseline batch |
| 2 | 2.690 | 2.910 | slightly harder slice |
| 3 | 2.720 | 2.940 | evaluation window drift |
| 4 | 2.840 | 3.060 | post-fix reread |

Debugging transcript excerpt:
```text
[reviewer] Why is validation lower after the bugfix?
[engineer] The old logger dropped long examples before averaging.
[reviewer] So the previous comparison favored easier rows?
[engineer] Yes, the denominator was cleaner than the data.
```

## Wrong explanation that looked plausible
The first trap in duplicate examples in train only is to turn one scalar into a universal rule.
Here the train values 2.570, 2.690, and 2.720 only become meaningful after the validation path 2.790, 2.910, and 2.940 is inspected alongside the scenario details.
A second trap is to ignore which examples dominate the average. In this topic, the concrete anchor matters because it localizes where the loss story changes shape.

## Better diagnosis
Before the correction, the working story was based on this series: 2.570, 2.690, 2.720, 2.840.
After adding the topic-specific check, the team would retell the run using: 2.790, 2.910, 2.940, 3.060.
That difference is small enough to miss in a dashboard and large enough to change a decision about loss/validation/overfitting behavior.

## Prevention habit
- Which piece of evidence is unique to this topic rather than generic to all training runs?
- What would still look suspicious if the metric scalar were removed from the page?
- Which follow-up trace would separate a logging problem from a model-behavior problem?

Closing note: the educational value of this draft comes from tying one exact failure or comparison to one exact reading habit.
