---
draft_status: candidate
topic_id: RTS-008
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC4
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
---

# CUDA Allocated vs Reserved Memory

## Concept
Allocated and reserved memory answer different questions.
Allocated memory is what live tensors currently use.
Reserved memory includes what the allocator is holding onto for reuse.

## Explanation
A training run may report modest allocated memory while reserved memory stays much higher.
That does not automatically mean there is a leak.
Caching allocators often keep blocks available to reduce future allocation overhead.

For runtime review, the important question is not "Why are these numbers different?"
The better question is "Are these numbers stable for this workload, or are they climbing step after step without a good reason?"

## Minimal Example
Suppose a tiny A100 smoke logs:
- step 1: allocated 8 GB, reserved 10 GB
- step 10: allocated 8.1 GB, reserved 10 GB
- step 100: allocated 8.1 GB, reserved 10.1 GB

This pattern may be normal.
Now imagine instead:
- step 1: allocated 8 GB, reserved 10 GB
- step 10: allocated 10 GB, reserved 14 GB
- step 100: allocated 18 GB, reserved 24 GB

That second pattern deserves investigation.

## Common Pitfalls
A common mistake is alarming on reserved memory alone.
Another is ignoring monotonic growth in both numbers.
A third is comparing metrics from different sequence lengths as if they were the same workload.
A fourth is reporting a single peak number without the surrounding context.

## Review Notes
Memory reviews are more useful when paired with batch size, sequence length, and precision mode.
Without that context, the same number can look healthy or unhealthy depending on the run.
For synthetic educational material, trend interpretation is more valuable than exact hardware-specific thresholds.
