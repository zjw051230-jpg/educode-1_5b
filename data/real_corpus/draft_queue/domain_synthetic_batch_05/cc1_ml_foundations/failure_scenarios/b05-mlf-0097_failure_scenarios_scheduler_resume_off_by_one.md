---
draft_status: candidate
topic_id: B05-MLF-0097
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-1
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---


# Scheduler Resume Off by One

The most memorable teaching examples in this batch are incident-shaped, because they force the reader to reason from symptoms.
The learning objective is specific: Use an off-by-one scheduler resume bug to teach how curves drift after checkpoint recovery.
This note is written as a incident notebook and uses a debugging transcript as the concrete anchor.

## First observation
- topic_id: B05-MLF-0097
- subdirectory: failure_scenarios
- focus: scheduler_resume_off_by_one
- reader task: explain the metric shift without falling back to a generic review script

## Timeline notes
| checkpoint | train_loss | val_loss | note |
| --- | ---: | ---: | --- |
| 1 | 2.790 | 3.010 | baseline batch |
| 2 | 2.910 | 3.130 | slightly harder slice |
| 3 | 2.940 | 3.160 | evaluation window drift |
| 4 | 3.060 | 3.280 | post-fix reread |

Debugging transcript excerpt:
```text
[reviewer] Why is validation lower after the bugfix?
[engineer] The old logger dropped long examples before averaging.
[reviewer] So the previous comparison favored easier rows?
[engineer] Yes, the denominator was cleaner than the data.
```

## Small reconstruction
The first trap in scheduler resume off by one is to turn one scalar into a universal rule.
Here the train values 2.790, 2.910, and 2.940 only become meaningful after the validation path 3.010, 3.130, and 3.160 is inspected alongside the scenario details.
A second trap is to ignore which examples dominate the average. In this topic, the concrete anchor matters because it localizes where the loss story changes shape.

## Working conclusion
Before the correction, the working story was based on this series: 2.790, 2.910, 2.940, 3.060.
After adding the topic-specific check, the team would retell the run using: 3.010, 3.130, 3.160, 3.280.
That difference is small enough to miss in a dashboard and large enough to change a decision about loss/validation/overfitting behavior.

## Next sanity check
- Which piece of evidence is unique to this topic rather than generic to all training runs?
- What would still look suspicious if the metric scalar were removed from the page?
- Which follow-up trace would separate a logging problem from a model-behavior problem?

Closing note: the educational value of this draft comes from tying one exact failure or comparison to one exact reading habit.
