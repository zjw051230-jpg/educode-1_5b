---
draft_status: candidate
topic_id: B05-PDS-0073
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-2
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---

# Seed Propagation Across Stages

**Learning objective:** explain a config repair where preprocessing and batching used different seeds.

## Question 1
What is the first observation that tells you the artifact is broken?

## Answer 1
The answer comes from a before/after comparison that exposes a mismatch before any large pipeline reasoning is needed.

## Question 2
Why is the obvious quick fix not always safe?

## Answer 2
Because quick coercion can erase the evidence that would let a reviewer explain the bug source. Draft review prefers visible, reversible fixes.

## Question 3
What should be re-checked after the repair?

## Answer 3
Re-check the narrow invariant that the file is teaching: row shape, split boundaries, metric units, or batch alignment.

## Counterexample
A repair that makes counts look clean while changing row identity is not acceptable here.

## Final prompt
Write one sentence saying which invariant changed from failing to passing.

- Extra verification prompt: explain which single observation would prove the repair worked.

- Extra verification prompt: explain which single observation would prove the repair worked.

- Extra verification prompt: explain which single observation would prove the repair worked.

- Extra verification prompt: explain which single observation would prove the repair worked.

- Extra verification prompt: explain which single observation would prove the repair worked.

- Extra verification prompt: explain which single observation would prove the repair worked.

- Extra verification prompt: explain which single observation would prove the repair worked.

- Extra verification prompt: explain which single observation would prove the repair worked.
