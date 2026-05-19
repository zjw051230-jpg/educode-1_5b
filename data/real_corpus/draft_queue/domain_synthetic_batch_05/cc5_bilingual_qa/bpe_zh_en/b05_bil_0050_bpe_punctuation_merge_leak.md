---
draft_status: candidate
topic_id: B05-BIL-0050
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-5
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---

# BPE Merge Rules and Vocabulary Growth 50: Punctuation Merge Leak

## Merge review checklist
- Which pair preserves the actual engineering unit?
- Which pair is only frequent because punctuation repeats?
- Does one language side lose more local meaning after the merge budget is exhausted?
- Can the surviving merge still support a concrete example later in the sample?

## Tiny example
Budget: 1 remaining merge
Candidates: `(KV,cache)` vs `(吞,吐)`

The better choice depends on the learning goal, not only on count totals.

## Concrete anchor: small pseudo-run log
This checklist turns merge inspection into explicit decisions.

## Learning objective
Evaluate BPE choices against teaching usefulness, not just compression.
