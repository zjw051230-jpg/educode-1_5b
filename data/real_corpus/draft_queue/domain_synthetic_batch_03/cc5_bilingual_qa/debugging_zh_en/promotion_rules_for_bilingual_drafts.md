---
draft_status: candidate
topic_id: BIL-016
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC5
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
---

# Promotion Rules for Bilingual Drafts

## Concept
Q: 为什么 bilingual draft 必须区分 candidate 和可训练语料？
EN: Why must bilingual drafts distinguish candidate status from trainable data?

A: 因为 draft 的目标是审阅和修订，不是直接进入正式训练链路。
EN: Because the goal of a draft is review and revision, not immediate entry into the formal training pipeline.

## Explanation
Q: promotion rule 的核心是什么？
EN: What is the core of a promotion rule?

A: 核心是：只有在内容、格式、边界、元数据都通过人工检查后，草稿才有资格进入下一阶段。
EN: The core idea is that only after content, formatting, boundaries, and metadata pass human review may a draft move forward.

Q: 这对 bilingual 数据特别重要吗？
EN: Is this especially important for bilingual data?

A: 是的，因为双语样本多了一层跨语言对齐风险，错误不一定在单语阅读时就能暴露。
EN: Yes, because bilingual samples add a cross-language alignment risk, and some problems do not surface during single-language reading.

## Minimal Example
- candidate 阶段关注：metadata 是否完整、问答是否原创、语言是否对齐。
- Candidate-stage checks: metadata completeness, originality of Q&A, and alignment between languages.

- promotion 前关注：是否存在翻译腔、模板漂移、编码问题、越界内容。
- Before promotion, check for translation artifacts, template drift, encoding problems, and out-of-scope content.

## Common Pitfalls
- 把“能读”误当成“能训”。
- Mistaking “readable” for “ready to train.”

- 只看中文或只看英文，不做双向审阅。
- Reviewing only Chinese or only English instead of both directions.

- 忘记保留 draft_review_only 元数据。
- Forgetting to preserve the draft_review_only metadata.

## Review Notes
- Draft queue only; review required before promotion.
- This note describes process discipline, not a promise that any current draft is approved.
