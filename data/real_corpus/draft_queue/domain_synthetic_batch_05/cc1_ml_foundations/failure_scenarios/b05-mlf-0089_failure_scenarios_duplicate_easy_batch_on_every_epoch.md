---
draft_status: candidate
topic_id: B05-MLF-0089
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-1
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---


# Duplicate Easy Batch on Every Epoch

The most memorable teaching examples in this batch are incident-shaped, because they force the reader to reason from symptoms.
The learning objective is specific: Show how one duplicated easy batch can create a fake curve improvement.
This note is written as a incident notebook and uses a small pseudo-run log as the concrete anchor.

## First observation
- topic_id: B05-MLF-0089
- subdirectory: failure_scenarios
- focus: duplicate_easy_batch_on_every_epoch
- reader task: explain the metric shift without falling back to a generic review script

## Timeline notes
| checkpoint | train_loss | val_loss | note |
| --- | ---: | ---: | --- |
| 1 | 2.710 | 2.930 | baseline batch |
| 2 | 2.740 | 2.960 | slightly harder slice |
| 3 | 2.860 | 3.080 | evaluation window drift |
| 4 | 2.980 | 3.200 | post-fix reread |

Pseudo-run log:
```text
step=100 train_loss=2.710 val_loss=2.930 grad_norm=3.120
step=101 train_loss=2.740 val_loss=2.960 grad_norm=3.150
step=102 train_loss=2.860 val_loss=3.080 grad_norm=3.270
step=103 train_loss=2.980 val_loss=3.200 grad_norm=3.390
```

## Small reconstruction
The first trap in duplicate easy batch on every epoch is to turn one scalar into a universal rule.
Here the train values 2.710, 2.740, and 2.860 only become meaningful after the validation path 2.930, 2.960, and 3.080 is inspected alongside the scenario details.
A second trap is to ignore which examples dominate the average. In this topic, the concrete anchor matters because it localizes where the loss story changes shape.

## Working conclusion
Before the correction, the working story was based on this series: 2.710, 2.740, 2.860, 2.980.
After adding the topic-specific check, the team would retell the run using: 2.930, 2.960, 3.080, 3.200.
That difference is small enough to miss in a dashboard and large enough to change a decision about loss/validation/overfitting behavior.

## Next sanity check
- Which piece of evidence is unique to this topic rather than generic to all training runs?
- What would still look suspicious if the metric scalar were removed from the page?
- Which follow-up trace would separate a logging problem from a model-behavior problem?

Closing note: the educational value of this draft comes from tying one exact failure or comparison to one exact reading habit.
