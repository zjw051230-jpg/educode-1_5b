---
draft_status: candidate
topic_id: BIL-002
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC5
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
---

# ZH and EN Punctuation Tokenization

## Concept
Q: 中英文混合语料里，标点为什么值得单独检查？
EN: Why is punctuation worth checking separately in mixed Chinese-English corpora?

A: 因为中文全角标点和英文半角标点在视觉上相似，但在字节和 token 分布上并不相同。
EN: Because Chinese full-width punctuation and English half-width punctuation look similar, but they differ in bytes and token distributions.

## Explanation
Q: 这会怎么影响 tokenizer 或 BPE merge？
EN: How does this affect the tokenizer or BPE merges?

A: 如果数据里同时存在 “,” 和 “，” ，模型会看到两个不同模式。
EN: If the data contains both "," and "，", the model sees two different patterns.

A: 在 bilingual Q&A 里，问号、冒号、括号尤其常见，所以它们是否独立成 token、是否和前后文本频繁合并，会影响序列稳定性。
EN: In bilingual Q&A, question marks, colons, and brackets appear often, so whether they become separate tokens or frequently merge with neighboring text affects sequence stability.

## Minimal Example
Q: 给两个对比句子。
EN: Give two contrasting sentences.

A: 句子一："为什么 loss 上升？"
EN: Sentence one: "为什么 loss 上升？"

A: 句子二: "Why does loss rise?"
EN: Sentence two: "Why does loss rise?"

A: 它们表达相似问题，但使用了不同脚本与不同问号系统。若 tokenizer 对这些模式分布差异很大，训练日志中的 token count 也会跟着摆动。
EN: They express similar questions, but use different scripts and question-mark systems. If the tokenizer distributes these patterns very differently, token counts in training logs will also swing.

## Common Pitfalls
Q: 常见错误有哪些？
EN: What are common mistakes?

A: 把标点规范化问题误当成语义问题。
EN: Treating punctuation normalization as a semantic issue.

A: 只检查可视文本，不检查 encode 后 token 数量变化。
EN: Checking only visible text and not the token-count change after encoding.

A: 在 review 时忽略中英文冒号、引号和括号的风格混用。
EN: Ignoring mixed styles of colons, quotes, and brackets during review.

## Review Notes
- Draft queue only; review required before promotion.
- Educational point: punctuation consistency is often a data quality issue before it becomes a modeling issue.
