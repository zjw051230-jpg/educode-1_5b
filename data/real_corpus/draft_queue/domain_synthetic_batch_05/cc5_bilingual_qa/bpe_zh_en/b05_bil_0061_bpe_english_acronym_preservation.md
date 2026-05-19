---
draft_status: candidate
topic_id: B05-BIL-0061
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-5
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---

# BPE Merge Rules and Vocabulary Growth 61: English Acronym Preservation

## Mini lab
### Setup
Pairs observed in a tiny bilingual shard:
- `(A,100)` count 4
- `(吞,吐)` count 5
- `(token,budget)` count 4

### Rule
Pick the top 2 merges after applying a +2 bonus to known technical literals.

### Result
- chosen: `(A,100)` and `(吞,吐)`
- excluded: `(token,budget)`

### Interpretation
The lab shows that one bonus can rescue a hardware literal, but it may also crowd out a pedagogically useful phrase.

## Concrete anchor: tensor shape
This is a numeric toy lab, not a stock explanation block.

## Learning objective
Reason about merge-budget tradeoffs with tiny counts you can inspect manually.
