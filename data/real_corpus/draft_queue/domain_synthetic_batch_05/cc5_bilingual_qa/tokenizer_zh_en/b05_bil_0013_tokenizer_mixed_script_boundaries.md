---
draft_status: candidate
topic_id: B05-BIL-0013
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-5
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---

# Tokenizer Boundaries and Mixed Scripts 13: Mixed-Script Boundary Decisions

## What we are checking
A small tokenizer probe on mixed punctuation.

```text
input_a = 'loss下降, keep lr=1e-4'
input_b = 'loss 下降，keep lr = 1e-4'
```

## Walkthrough
1. Read the string as alternating CJK spans, ASCII spans, digits, and punctuation.
2. Mark every location where a delimiter could split a token.
3. Compare whether the normalized form keeps `lr=1e-4` stable.

## Mini trace
```text
A -> [loss][下降][,][keep][lr=1e-4]
B -> [loss][下降][，][keep][lr][=][1e][-][4]
```

## Bilingual interpretation
- ZH: 第二个版本看起来更整洁，但它把学习率表达式拆散了。
- EN: The second version reads cleaner, but it fractures the learning-rate expression.

## Failure scenario
If the Chinese side keeps `lr=1e-4` intact while the English side breaks it apart, the model sees different local neighborhoods around the same concept.

## What to fix first
- preserve engineering literals
- normalize full-width punctuation deliberately
- avoid inserting decorative spaces around operator-like substrings

## Concrete anchor: failure scenario
This file treats the token boundary problem as a walkable trace, not a generic explanation.
