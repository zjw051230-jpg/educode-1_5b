---
draft_status: candidate
topic_id: MLF-003
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-1
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
---

# Finite Loss Checks in Smoke Training Runs

A smoke run is not meant to prove quality.
Its first job is to prove the training loop produces finite numbers under realistic tensor shapes.

The most basic loss check is whether the scalar is finite on step 0.
If the first forward pass returns NaN or inf, optimization discussions are premature.

A synthetic checklist can be tiny:
- logits contain finite values
- loss is finite before backward
- gradients are finite after backward
- parameters remain finite after optimizer step

Each item narrows the failure region.
Non-finite logits often point to exploding activations or invalid masking.
Finite logits with non-finite loss may point to target indexing or loss-mask bugs.
Finite loss but non-finite gradients can indicate unstable scaling under backpropagation.

It is useful to think in terms of propagation.
A single NaN introduced in one tensor can spread through the training step and make later diagnostics noisy.
Checking early catches the first bad boundary rather than the last visible symptom.

Validation loss belongs in smoke checks too.
A loop that trains with finite loss but evaluates with NaN may still have a mismatch in masking, mixed precision settings, or sequence packing paths.

Finite does not mean good.
A model can produce a stable but useless loss curve if labels are shifted incorrectly or data is overly repetitive.
Still, non-finite values mean the run is not trustworthy enough for higher-level interpretation.

For very small educational corpora, a good smoke run often shows noisy but bounded movement.
Loss might rise and fall over a few steps while staying finite and roughly plausible.
Perfect smoothness is not required.

If instability appears only after several optimizer steps, learning rate is an immediate suspect.
If instability appears before any step, inspect data flow, masking, and initialization first.

The goal is modest but essential.
Finite train and validation losses tell us the system is numerically alive enough to begin real debugging.
