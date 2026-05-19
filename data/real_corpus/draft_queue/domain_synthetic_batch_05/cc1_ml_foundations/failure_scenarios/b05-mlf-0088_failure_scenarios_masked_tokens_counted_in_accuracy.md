---
draft_status: candidate
topic_id: B05-MLF-0088
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-1
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---


# Masked Tokens Counted in Accuracy

The entry starts with a confusing run artifact and reconstructs the debugging path that untangled it.
The learning objective is specific: Teach how counting masked tokens in accuracy hides quality regressions.
This note is written as a incident notebook and uses a numeric toy example as the concrete anchor.

## First observation
- topic_id: B05-MLF-0088
- subdirectory: failure_scenarios
- focus: masked_tokens_counted_in_accuracy
- reader task: explain the metric shift without falling back to a generic review script

## Timeline notes
| checkpoint | train_loss | val_loss | note |
| --- | ---: | ---: | --- |
| 1 | 2.570 | 2.790 | baseline batch |
| 2 | 2.690 | 2.910 | slightly harder slice |
| 3 | 2.720 | 2.940 | evaluation window drift |
| 4 | 2.840 | 3.060 | post-fix reread |

Concrete anchor in use: numeric toy example.
- baseline reading: 2.570
- changed reading: 3.060
- comparison delta: 0.490

## Small reconstruction
The first trap in masked tokens counted in accuracy is to turn one scalar into a universal rule.
Here the train values 2.570, 2.690, and 2.720 only become meaningful after the validation path 2.790, 2.910, and 2.940 is inspected alongside the scenario details.
A second trap is to ignore which examples dominate the average. In this topic, the concrete anchor matters because it localizes where the loss story changes shape.

## Working conclusion
Before the correction, the working story was based on this series: 2.570, 2.690, 2.720, 2.840.
After adding the topic-specific check, the team would retell the run using: 2.790, 2.910, 2.940, 3.060.
That difference is small enough to miss in a dashboard and large enough to change a decision about loss/validation/overfitting behavior.

## Next sanity check
- Which piece of evidence is unique to this topic rather than generic to all training runs?
- What would still look suspicious if the metric scalar were removed from the page?
- Which follow-up trace would separate a logging problem from a model-behavior problem?

Closing note: the educational value of this draft comes from tying one exact failure or comparison to one exact reading habit.
