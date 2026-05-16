---
draft_status: candidate
topic_id: BIL-004
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC5
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
---

# Mixed-Script Spacing Notes

## Concept
Q: 中英混排时，空格到底重要吗？
EN: In mixed-script text, do spaces really matter?

A: 很重要，因为空格既影响可读性，也影响 tokenizer 如何建立边界。
EN: Yes, because spaces affect readability and also shape how the tokenizer builds boundaries.

## Explanation
Q: 中文不是经常不靠空格吗？
EN: But Chinese often works without spaces, right?

A: 对，纯中文通常不依赖空格分词，但当中文和英文术语、数字、缩写连在一起时，是否加空格会改变 token pattern。
EN: Yes. Pure Chinese usually does not depend on spaces, but when Chinese touches English terms, numbers, or abbreviations, the presence or absence of spaces changes token patterns.

Q: 举个训练相关例子。
EN: Give a training-related example.

A: “在A100上训练” 和 “在 A100 上训练” 视觉含义接近，但 token 边界可能不同。
EN: “在A100上训练” and “在 A100 上训练” mean nearly the same visually, but their token boundaries may differ.

## Minimal Example
- 推荐在 synthetic bilingual Q&A 中使用稳定风格，而不是同一批次混用过多 spacing 样式。
- In synthetic bilingual Q&A, prefer a stable spacing style instead of mixing too many spacing patterns within the same batch.

- 如果一个术语在多文件中反复出现，最好保持同一种空格习惯，便于后续 review。
- If one term appears across many files, keep one spacing habit to make later review easier.

## Common Pitfalls
Q: 什么情况最容易制造无意义差异？
EN: What most easily creates meaningless variation?

A: 同一概念今天写“train loss”，明天写“train_loss”，后天写“trainloss”。
EN: Writing the same concept as “train loss” today, “train_loss” tomorrow, and “trainloss” later.

A: 这种差异不一定增加教育价值，反而可能让 tiny batch 分布更碎。
EN: That variation does not necessarily add educational value and can instead fragment tiny-batch distributions.

## Review Notes
- Draft queue only; review required before promotion.
- Spacing consistency is a style control tool, not a universal linguistic rule.
