---
draft_status: candidate
topic_id: B05-MLF-0081
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-1
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---


# Shifted Labels After Concatenation

The most memorable teaching examples in this batch are incident-shaped, because they force the reader to reason from symptoms.
The learning objective is specific: Teach how a concatenation bug shifts labels and poisons both loss and validation interpretation.
This note is written as a incident notebook and uses a mini code trace as the concrete anchor.

## First observation
- topic_id: B05-MLF-0081
- subdirectory: failure_scenarios
- focus: shifted_labels_after_concatenation
- reader task: explain the metric shift without falling back to a generic review script

## Timeline notes
| checkpoint | train_loss | val_loss | note |
| --- | ---: | ---: | --- |
| 1 | 2.540 | 2.760 | baseline batch |
| 2 | 2.660 | 2.880 | slightly harder slice |
| 3 | 2.780 | 3.000 | evaluation window drift |
| 4 | 2.810 | 3.030 | post-fix reread |

Mini code trace:
```text
shifted_targets = targets[:, 1:]
trimmed_logits   = logits[:, :-1, :]
loss = cross_entropy(trimmed_logits.reshape(-1, vocab), shifted_targets.reshape(-1))
```

## Small reconstruction
The first trap in shifted labels after concatenation is to turn one scalar into a universal rule.
Here the train values 2.540, 2.660, and 2.780 only become meaningful after the validation path 2.760, 2.880, and 3.000 is inspected alongside the scenario details.
A second trap is to ignore which examples dominate the average. In this topic, the concrete anchor matters because it localizes where the loss story changes shape.

## Working conclusion
Before the correction, the working story was based on this series: 2.540, 2.660, 2.780, 2.810.
After adding the topic-specific check, the team would retell the run using: 2.760, 2.880, 3.000, 3.030.
That difference is small enough to miss in a dashboard and large enough to change a decision about loss/validation/overfitting behavior.

## Next sanity check
- Which piece of evidence is unique to this topic rather than generic to all training runs?
- What would still look suspicious if the metric scalar were removed from the page?
- Which follow-up trace would separate a logging problem from a model-behavior problem?

Closing note: the educational value of this draft comes from tying one exact failure or comparison to one exact reading habit.
