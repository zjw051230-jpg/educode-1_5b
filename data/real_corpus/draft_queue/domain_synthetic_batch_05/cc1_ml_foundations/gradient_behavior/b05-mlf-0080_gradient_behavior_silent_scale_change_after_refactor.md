---
draft_status: candidate
topic_id: B05-MLF-0080
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-1
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---


# Silent Scale Change After a Refactor

The checklist is evidence-first because the same loss curve can hide very different gradient states.
The learning objective is specific: Show how a refactor can change gradient scale even when the training loop still runs.
This note is written as a evidence-first checklist and uses a debugging transcript as the concrete anchor.

## Evidence before naming the bug
- topic_id: B05-MLF-0080
- subdirectory: gradient_behavior
- focus: silent_scale_change_after_a_refactor
- reader task: explain the metric shift without falling back to a generic review script

## Signals that matter
| checkpoint | train_loss | val_loss | note |
| --- | ---: | ---: | --- |
| 1 | 2.490 | 2.710 | baseline batch |
| 2 | 2.520 | 2.740 | slightly harder slice |
| 3 | 2.640 | 2.860 | evaluation window drift |
| 4 | 2.760 | 2.980 | post-fix reread |

Debugging transcript excerpt:
```text
[reviewer] Why is validation lower after the bugfix?
[engineer] The old logger dropped long examples before averaging.
[reviewer] So the previous comparison favored easier rows?
[engineer] Yes, the denominator was cleaner than the data.
```

## Signals that can mislead
The first trap in silent scale change after a refactor is to turn one scalar into a universal rule.
Here the train values 2.490, 2.520, and 2.640 only become meaningful after the validation path 2.710, 2.740, and 2.860 is inspected alongside the scenario details.
A second trap is to ignore which examples dominate the average. In this topic, the concrete anchor matters because it localizes where the loss story changes shape.

## Minimal intervention
Before the correction, the working story was based on this series: 2.490, 2.520, 2.640, 2.760.
After adding the topic-specific check, the team would retell the run using: 2.710, 2.740, 2.860, 2.980.
That difference is small enough to miss in a dashboard and large enough to change a decision about loss/validation/overfitting behavior.

## Escalation rule
- Which piece of evidence is unique to this topic rather than generic to all training runs?
- What would still look suspicious if the metric scalar were removed from the page?
- Which follow-up trace would separate a logging problem from a model-behavior problem?

Closing note: the educational value of this draft comes from tying one exact failure or comparison to one exact reading habit.
