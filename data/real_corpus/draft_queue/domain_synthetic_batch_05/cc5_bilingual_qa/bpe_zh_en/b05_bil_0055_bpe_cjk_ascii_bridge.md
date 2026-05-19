---
draft_status: candidate
topic_id: B05-BIL-0055
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-5
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---

# BPE Merge Rules and Vocabulary Growth 55: CJK-ASCII Bridge

## Config review
```yaml
max_new_merges: 8
literal_bonus:
  A100: 2
  fp16: 2
punctuation_penalty: 1
min_pair_count: 3
```

## Reading the config
This configuration prefers preserving known technical literals, but it can under-serve new bilingual terms if the literal list is too short.

## Concrete example
`token budget` appears often enough to deserve a merge, but receives no bonus because only hardware literals were listed.

## Concrete anchor: before/after comparison
The lesson comes from a config snippet and one missing entry, not from generic discussion.

## Learning objective
Learn to read merge-policy config as a set of tradeoffs about which concepts deserve stable local form.
