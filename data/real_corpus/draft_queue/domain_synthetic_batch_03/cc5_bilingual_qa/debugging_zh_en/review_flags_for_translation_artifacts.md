---
draft_status: candidate
topic_id: BIL-017
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC5
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
---

# Review Flags for Translation Artifacts

## Concept
Q: 什么是 bilingual draft 里的 translation artifact？
EN: What is a translation artifact in a bilingual draft?

A: 它是指文本为了追求表面对照而留下的不自然表达、错位重心或机械句式。
EN: It is unnatural wording, misplaced emphasis, or mechanical phrasing left behind by trying too hard to mirror another language.

## Explanation
Q: 为什么这会影响教育语料质量？
EN: Why does this affect educational data quality?

A: 因为教学问答需要清晰解释概念，而翻译腔会把注意力从概念本身转移到奇怪表达上。
EN: Because educational Q&A should explain concepts clearly, while translation artifacts shift attention from the concept to awkward wording.

Q: review 时要看哪些信号？
EN: What signals should reviewers watch for?

A: 看是否出现逐句硬对齐、中文不自然重复主语、英文过度模仿中文句式等现象。
EN: Watch for forced sentence-by-sentence alignment, unnatural repetition of subjects in Chinese, or English that imitates Chinese syntax too literally.

## Minimal Example
A: 好的 bilingual Q&A 应该围绕同一知识点保持一致，而不是要求每句话字面映射。
EN: Good bilingual Q&A should stay aligned around the same concept, not force literal sentence mapping line by line.

## Common Pitfalls
- 把“不一样”当作错误，把“自然表达”误判为不忠实。
- Treating any difference as an error and natural phrasing as disloyal.

- 为了形式对称，牺牲解释清晰度。
- Sacrificing clarity just to preserve visual symmetry.

- 只检查语法，不检查语气是否像教学文本。
- Checking grammar only and not whether the tone still sounds educational.

## Review Notes
- Draft queue only; review required before promotion.
- This file teaches review heuristics for synthetic bilingual writing rather than translation doctrine.
