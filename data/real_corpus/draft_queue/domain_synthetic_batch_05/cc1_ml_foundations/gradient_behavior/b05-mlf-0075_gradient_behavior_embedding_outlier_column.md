---
draft_status: candidate
topic_id: B05-MLF-0075
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-1
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---


# Embedding Outlier Column

Instead of summarizing gradients in abstract terms, this file assembles the exact clues a reviewer would inspect.
The learning objective is specific: Show how one outlier embedding column can dominate a layer-level diagnostic.
This note is written as a evidence-first checklist and uses a tensor shape as the concrete anchor.

## Evidence before naming the bug
- topic_id: B05-MLF-0075
- subdirectory: gradient_behavior
- focus: embedding_outlier_column
- reader task: explain the metric shift without falling back to a generic review script

## Signals that matter
| checkpoint | train_loss | val_loss | note |
| --- | ---: | ---: | --- |
| 1 | 2.650 | 2.870 | baseline batch |
| 2 | 2.770 | 2.990 | slightly harder slice |
| 3 | 2.890 | 3.110 | evaluation window drift |
| 4 | 2.920 | 3.140 | post-fix reread |

Shape trace:
- logits: [batch=2, time=4, vocab=16]
- targets: [batch=2, time=4]
- active mask: [batch=2, time=4] with one dropped suffix position

## Signals that can mislead
The first trap in embedding outlier column is to turn one scalar into a universal rule.
Here the train values 2.650, 2.770, and 2.890 only become meaningful after the validation path 2.870, 2.990, and 3.110 is inspected alongside the scenario details.
A second trap is to ignore which examples dominate the average. In this topic, the concrete anchor matters because it localizes where the loss story changes shape.

## Minimal intervention
Before the correction, the working story was based on this series: 2.650, 2.770, 2.890, 2.920.
After adding the topic-specific check, the team would retell the run using: 2.870, 2.990, 3.110, 3.140.
That difference is small enough to miss in a dashboard and large enough to change a decision about loss/validation/overfitting behavior.

## Escalation rule
- Which piece of evidence is unique to this topic rather than generic to all training runs?
- What would still look suspicious if the metric scalar were removed from the page?
- Which follow-up trace would separate a logging problem from a model-behavior problem?

Closing note: the educational value of this draft comes from tying one exact failure or comparison to one exact reading habit.
