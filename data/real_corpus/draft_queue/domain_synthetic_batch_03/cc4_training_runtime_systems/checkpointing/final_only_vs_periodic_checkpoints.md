---
draft_status: candidate
topic_id: RTS-004
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC4
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
---

# Final-Only vs Periodic Checkpoints

## Concept
Checkpoint cadence is a runtime tradeoff between storage cost and recovery confidence.
A final-only policy is simple.
A periodic policy gives more recovery options.

## Explanation
Final-only checkpoints reduce disk usage and simplify cleanup.
They work best when runs are short, stable, and cheap to rerun.
Periodic checkpoints are better when runs are long or when interruptions are plausible.
They provide restart anchors and make progress review easier.

The hidden difference is what happens after a failure.
With final-only saves, one crash near the end can erase all progress.
With periodic saves, the loss is bounded by the interval.

## Minimal Example
Consider two 6-hour smokes.
Run A saves only at the end.
Run B saves every 30 minutes and at the end.
If both runs fail at hour 5:40, Run A restarts from zero.
Run B restarts from the most recent interval.

## Common Pitfalls
A common mistake is choosing a very short interval that harms throughput with excessive I/O.
Another is choosing such a long interval that the periodic policy is periodic in name only.
A third is keeping every checkpoint forever and making the experiment directory hard to inspect.
A fourth is assuming periodic saves remove the need for reload testing.

## Review Notes
There is no universal best interval.
For bounded educational runs, the right question is:
"How much progress can we afford to lose if this job stops now?"
That question usually leads to a better checkpoint schedule than copying a default from another project.
