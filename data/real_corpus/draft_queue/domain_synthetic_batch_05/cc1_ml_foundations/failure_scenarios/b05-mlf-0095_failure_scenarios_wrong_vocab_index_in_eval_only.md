---
draft_status: candidate
topic_id: B05-MLF-0095
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-1
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---


# Wrong Vocab Index in Eval Only

A failure scenario teaches more than a slogan when each symptom points toward a different wrong explanation first.
The learning objective is specific: Show how an eval-only index bug creates selective degradation that training logs cannot reveal.
This note is written as a incident notebook and uses a mini code trace as the concrete anchor.

## First observation
- topic_id: B05-MLF-0095
- subdirectory: failure_scenarios
- focus: wrong_vocab_index_in_eval_only
- reader task: explain the metric shift without falling back to a generic review script

## Timeline notes
| checkpoint | train_loss | val_loss | note |
| --- | ---: | ---: | --- |
| 1 | 2.600 | 2.820 | baseline batch |
| 2 | 2.630 | 2.850 | slightly harder slice |
| 3 | 2.750 | 2.970 | evaluation window drift |
| 4 | 2.870 | 3.090 | post-fix reread |

Mini code trace:
```text
shifted_targets = targets[:, 1:]
trimmed_logits   = logits[:, :-1, :]
loss = cross_entropy(trimmed_logits.reshape(-1, vocab), shifted_targets.reshape(-1))
```

## Small reconstruction
The first trap in wrong vocab index in eval only is to turn one scalar into a universal rule.
Here the train values 2.600, 2.630, and 2.750 only become meaningful after the validation path 2.820, 2.850, and 2.970 is inspected alongside the scenario details.
A second trap is to ignore which examples dominate the average. In this topic, the concrete anchor matters because it localizes where the loss story changes shape.

## Working conclusion
Before the correction, the working story was based on this series: 2.600, 2.630, 2.750, 2.870.
After adding the topic-specific check, the team would retell the run using: 2.820, 2.850, 2.970, 3.090.
That difference is small enough to miss in a dashboard and large enough to change a decision about loss/validation/overfitting behavior.

## Next sanity check
- Which piece of evidence is unique to this topic rather than generic to all training runs?
- What would still look suspicious if the metric scalar were removed from the page?
- Which follow-up trace would separate a logging problem from a model-behavior problem?

Closing note: the educational value of this draft comes from tying one exact failure or comparison to one exact reading habit.
