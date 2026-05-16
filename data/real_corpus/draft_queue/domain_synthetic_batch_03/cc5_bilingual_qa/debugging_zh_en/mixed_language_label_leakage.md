---
draft_status: candidate
topic_id: BIL-018
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC5
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
---

# Mixed-Language Label Leakage

## Concept
Q: 什么是 mixed-language label leakage？
EN: What is mixed-language label leakage?

A: 它指的是目标答案中泄露了不该提前出现的提示、标签或另一语言模板信号。
EN: It refers to target answers leaking prompts, labels, or template signals from another language earlier than intended.

## Explanation
Q: 这在 bilingual Q&A 里怎么发生？
EN: How can this happen in bilingual Q&A?

A: 例如中文问题后，本应输出中文解释，但 target 前缀残留了英文 answer label，导致监督目标混杂。
EN: For example, after a Chinese question, the model should output a Chinese explanation, but an English answer label remains at the front, mixing the supervision target.

Q: 为什么这不是小问题？
EN: Why is this not a minor issue?

A: 因为模型会把泄露结构学成正常模式，之后在生成时也可能错误切换语言或模板。
EN: Because the model may learn the leaked structure as normal and later switch language or template incorrectly during generation.

## Minimal Example
A: 问题要求“请用中文回答”，目标却以 “Answer:” 开头，再接中文段落，这就是一个轻量级泄露信号。
EN: If the prompt says “answer in Chinese” but the target begins with “Answer:” before a Chinese paragraph, that is a lightweight leakage signal.

## Common Pitfalls
- 只关注答案内容正确，不关注答案前缀是否错位。
- Checking whether the answer content is correct while ignoring wrong target prefixes.

- 把模板字段误拼进监督文本。
- Accidentally splicing template fields into the supervised text.

- 审阅时只做自然阅读，不做边界检查。
- Reviewing for readability only and not inspecting boundaries.

## Review Notes
- Draft queue only; review required before promotion.
- The goal is to surface leakage as a formatting/debugging issue before any training use.
