---
draft_status: candidate
topic_id: B05-RTS-0043
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-4
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---

# Weighted Versus Unweighted Validation Loss

This draft treats weighted versus unweighted validation loss as a bounded incident reconstruction problem rather than a generic lesson.

**Learning objective:** Demonstrate how averaging per-batch losses naively can understate validation loss when batch sizes differ.

## Lab setup
You are given one compact artifact packet and one question: is the runtime signal trustworthy enough to support a narrow conclusion?

## Input artifact
```json
{
  "topic_id": "B05-RTS-0043",
  "step": 12530,
  "val_loss": 2.030,
  "tokens_seen": 136490,
  "max_memory_allocated_gb": 38.6,
  "max_memory_reserved_gb": 63.5
}
```

## Extra rows
```text
step=12529 event=train_step loss=2.210
step=12530 event=eval_end samples=512 weighted_loss=2.030
step=12531 event=checkpoint_save duration_ms=496
```

## Exercise A
List which field you would trust first and why.

## Exercise B
Use the packet to answer one specific question:
- does the event order support the summary field?
- does the memory number change at a boundary?
- does the denominator make the loss comparable?

## Worked answer
A good answer names the exact field and its neighboring artifact. For example, if `weighted_loss` is present with `samples=512`, it carries more diagnostic weight than an unlabeled average copied into a summary blob.

## Failure mode diagnosis
The main trap is to restate the prettiest number without checking what emitted it. That turns a useful artifact packet into shallow generic explanation.

## Mini conclusion
This lab is complete when the learner can point to one field, one neighboring line, and one reason they belong together.
