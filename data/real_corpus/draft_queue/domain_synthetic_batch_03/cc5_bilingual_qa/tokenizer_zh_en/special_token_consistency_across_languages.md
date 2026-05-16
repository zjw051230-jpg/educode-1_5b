---
draft_status: candidate
topic_id: BIL-007
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC5
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
---

# Special Token Consistency Across Languages

## Concept
Q: special token 为什么要在中英文样本里保持一致？
EN: Why should special tokens remain consistent across Chinese and English samples?

A: 因为 special token 承担的是结构作用，而不是语言本身的内容作用。
EN: Because special tokens serve a structural role rather than a language-content role.

## Explanation
Q: 结构作用具体指什么？
EN: What does a structural role mean here?

A: 它们可能表示样本开始、回答开始、分隔段落或结束位置。
EN: They may indicate sample start, answer start, segment boundaries, or end positions.

A: 如果中文样本用一种边界标记，英文样本又用另一种，模型会把“语言差异”和“模板差异”混在一起学。
EN: If Chinese samples use one boundary marker and English samples use another, the model learns language differences and template differences at the same time.

## Minimal Example
Q: 一个好的做法是什么？
EN: What is one good practice?

A: 在 bilingual Q&A 中，尽量让同一轮问答使用统一的开头、分隔和结尾标记。
EN: In bilingual Q&A, try to keep the same start, separator, and ending markers across both languages.

A: 这样比较 train loss 时，更容易把变化归因到内容而不是模板差异。
EN: This makes it easier to attribute train-loss changes to content rather than template drift.

## Common Pitfalls
- 把中文 prompt 和英文 prompt 写成两套完全不同的模板。
- Writing Chinese and English prompts as two entirely different templates.

- 在部分样本里省略结束标记，导致对齐不稳定。
- Omitting end markers in only some samples and creating unstable alignment.

- 用太多稀有控制符，增加 review 难度。
- Using too many rare control markers and making review harder.

## Review Notes
- Draft queue only; review required before promotion.
- The educational point is template consistency, not any specific special-token inventory.
