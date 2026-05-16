---
draft_status: candidate
topic_id: RTS-016
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC4
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
---

# Run Metadata Field Guidelines

## Concept
Run metadata gives the experiment summary its identity.
It explains what was executed without forcing reviewers to infer context from filenames alone.

## Explanation
Strong metadata fields answer simple questions quickly:
- what run is this?
- what config family produced it?
- what hardware profile was used?
- what precision mode was active?
- what sequence length and batch shape were chosen?
- what checkpoint policy applied?

Metadata should be compact and stable.
If fields change names every week, comparisons become harder.
If fields are too vague, summaries lose their value.

## Minimal Example
A concise metadata set might include:
- `run_id`
- `experiment_group`
- `device_type`
- `precision`
- `seq_len`
- `micro_batch_size`
- `grad_accum_steps`
- `seed`

These fields make later summaries easier to align.

## Common Pitfalls
One pitfall is burying core run identity inside a free-form note.
Another is mixing immutable setup fields with mutable status fields under the same label.
A third is saving fields that sound precise but were never actually controlled.
A fourth is forgetting to record the seed for tiny reproducibility checks.

## Review Notes
Metadata discipline pays off later when many bounded runs exist side by side.
A reviewer should be able to scan a summary table and immediately tell why two runs differ.
That is much harder when the core setup lives only in memory or chat logs.
