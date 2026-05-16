---
draft_status: candidate
topic_id: RTS-019
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC4
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
---

# Source Category Count Reporting

## Concept
Source category count reporting explains what mixture of data sources appeared in a run.
It is a bookkeeping aid for experiment interpretation.

## Explanation
When a training input stream mixes several synthetic or curated categories, reviewers may want simple counts.
The goal is not to reconstruct every sample.
The goal is to summarize the composition seen by the run.

A compact report might track:
- source category name
- sample count
- estimated token count
- percentage of total

These counts become useful when comparing runs that differ in data mix.
They also help validate that a sampling policy behaved as expected.

## Minimal Example
A summary might report:
- runtime_systems_notes: 40%
- transformer_architecture_notes: 35%
- bilingual_qa_notes: 25%

That does not prove anything about model quality.
It simply records what the run consumed.

## Common Pitfalls
A common mistake is treating approximate counts as exact provenance.
Another is omitting whether the unit is samples or tokens.
A third is reporting counts once at launch but not after filtering or truncation changes.
A fourth is making category names too informal to compare across runs.

## Review Notes
Count reporting is most useful when it answers a later question quickly.
If someone asks why two runs differ, source composition is often one of the first things to check.
That is why even simple count summaries can be high-value runtime metadata.
