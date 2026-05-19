---
draft_status: candidate
topic_id: B05-BIL-anti-template-self-check
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-5
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---

# Anti-Template Self Check

## How this batch differs from batch_04
- It does not reuse a fixed Concept / Explanation / Minimal Example / Common Pitfalls / Review Notes scaffold.
- It spreads generation across tokenizer_zh_en, bpe_zh_en, and concept_contrast_zh_en instead of letting one loop dominate the full run.
- Python files implement topic logic directly instead of generic row-summary helpers.

## Heading and shape diversity
- Some markdown files are diaries, some are checklists, some are labs, some are tables, and some are short Q&A exchanges.
- Even when headings repeat at a high level, the body anchor changes: token trace, merge ranking, failure slice, config snippet, metric reading, or comparison table.

## Learning-objective discipline
- Every manifest row carries a unique learning_objective tied to one local focus and one concrete anchor.
- The generation registry was built before writing files so the batch could reserve different file stems, writing forms, and anchors.

## Concrete-anchor distribution
- tensor shape: 10
- mini code trace: 10
- failure scenario: 10
- decision checklist: 10
- before/after comparison: 10
- debugging transcript: 10
- numeric toy example: 10
- config snippet: 10
- metrics interpretation: 10
- small pseudo-run log: 10

## Python anti-template checks
- tokenizer .py files run mixed-script segmentation traces.
- bpe .py files rank merge pairs with literal-aware scoring.
- concept_contrast .py files score anchor preservation and claim escalation.

## Residual duplication risk
- Because the batch remains within three related bilingual subtopics, some vocabulary naturally overlaps.
- The remaining risk is semantic neighborhood overlap, not full-structure scaffold repetition.
