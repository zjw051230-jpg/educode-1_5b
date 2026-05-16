---
draft_status: candidate
topic_id: BIL-013
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC5
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
---

# Sequence-Length Pressure in Bilingual Examples

## Concept
Q: 为什么 bilingual example 更容易带来 sequence-length pressure？
EN: Why do bilingual examples more easily create sequence-length pressure?

A: 因为同一教学点往往要用两种语言表达，文本自然更长。
EN: Because the same teaching point often gets expressed in two languages, so the text naturally grows longer.

## Explanation
Q: 长度压力会影响什么？
EN: What does length pressure affect?

A: 它会影响 batch size、显存占用、attention mask 大小，以及被截断的信息量。
EN: It affects batch size, memory use, attention-mask size, and how much information gets truncated.

Q: 如果 seq len 不够怎么办？
EN: What if the sequence length is too small?

A: 你可以缩短模板、减少重复解释、或者把一个大问答拆成更小的样本。
EN: You can shorten the template, reduce repeated explanation, or split one large Q&A into smaller samples.

## Minimal Example
A: 一个中文问答 70 tokens，配上英文解释后变成 125 tokens，就可能让原本稳定的 tiny batch 需要重新裁剪。
EN: A Chinese Q&A that costs 70 tokens can become 125 tokens after adding English explanation, which may force a once-stable tiny batch to be cropped again.

## Common Pitfalls
- 以为 line 数不多就一定 token 数不高。
- Assuming a small line count always implies a small token count.

- 只压缩英文，不压缩中文模板冗余。
- Compressing only English while leaving redundant Chinese template text untouched.

- 截断后不检查答案尾部是否被切断。
- Truncating without checking whether the answer tail was severed.

## Review Notes
- Draft queue only; review required before promotion.
- Length pressure is especially visible in bilingual educational drafts because alignment often duplicates structure.
