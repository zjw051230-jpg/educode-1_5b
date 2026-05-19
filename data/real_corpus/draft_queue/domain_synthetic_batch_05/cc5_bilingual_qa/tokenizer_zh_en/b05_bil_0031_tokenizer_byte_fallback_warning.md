---
draft_status: candidate
topic_id: B05-BIL-0031
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-5
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---

# Tokenizer Boundaries and Mixed Scripts 31: Byte Fallback Warning

## Debugging diary
09:10 — I compared two bilingual prompts and noticed only the Chinese version exceeded the token budget.

09:14 — The visible text difference looked trivial: one full-width comma, one inserted space before `MB/s`.

09:19 — A manual trace showed the real issue.

```text
version_1: [吞吐][MB/s]
version_2: [吞吐][MB][/][s]
```

## What fooled the reviewer
The prompt still read fluently, so the first instinct was to blame the batch sampler. The boundary trace showed the problem was local formatting, not data selection.

## Concrete anchor: tensor shape
- observed drift: 2 extra tokens in the Chinese half
- local cause: width-normalization plus slash separation

## Repair decision
- Keep unit expressions like `MB/s` untouched.
- Normalize punctuation around them only if the token boundary stays stable.

## Learning objective
- ZH: 从局部切分证据定位 mixed-script token drift。
- EN: Learn to localize mixed-script token drift from a boundary-level trace.

## Short contrast
The wrong question is “Which sentence looks nicer?”
The better question is “Which literal survives the same way on both language sides?”
