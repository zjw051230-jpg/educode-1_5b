---
draft_status: candidate
topic_id: B05-BIL-0068
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-5
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---

# Concept Contrasts and Evaluation Caution 68: Alignment Versus Translation

## Numeric toy example
Suppose a bilingual review score has two parts:
- fluency: 5/5
- anchor preservation: 2/5

The total average is 3.5/5, which can hide a real failure if the teaching goal depends on anchor preservation.

## Why the number matters
A high fluency score cannot compensate for a collapsed contrast when the sample is meant to teach a boundary.

## Concrete anchor: config snippet
The anchor is a two-metric split that exposes the hidden weakness.

## Learning objective
Interpret bilingual quality scores in a way that protects conceptual distinctions.
