---
draft_status: candidate
topic_id: B05-BIL-0027
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-5
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---

# Tokenizer Boundaries and Mixed Scripts 27: Unicode NFKC Edge Case

## Failure analysis
A bilingual draft used the same glossary term in both languages, but the tokenizer treated the term boundary differently after one copy edit.

## Symptom
- Chinese side gained extra tokens around a slash-delimited term.
- English side kept the term intact.
- Downstream comparison reported a fake asymmetry.

## Failure slice
| string | local boundary result |
|---|---|
| `KV cache命中率` | `[KV][cache][命中率]` |
| `KV-cache 命中率` | `[KV][-][cache][命中率]` |

## Why the failure is subtle
The phrase still teaches the same idea semantically, but the model sees different local neighborhoods. That is enough to distort sequence statistics.

## Concrete anchor: numeric toy example
This analysis relies on a before/after slice, not on broad review language.

## Decision checklist
- Does the engineering literal stay grouped?
- Did punctuation introduce a new split?
- Does only one language side drift?

## Learning objective
Understand how a cosmetic edit can create a tokenizer-visible mismatch.
