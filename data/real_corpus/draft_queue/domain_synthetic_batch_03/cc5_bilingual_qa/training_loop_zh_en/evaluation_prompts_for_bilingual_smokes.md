---
draft_status: candidate
topic_id: BIL-012
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC5
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
---

# Evaluation Prompts for Bilingual Smokes

## Concept
Q: bilingual smoke run 的 evaluation prompt 应该关注什么？
EN: What should evaluation prompts focus on in bilingual smoke runs?

A: 它们应该足够短、足够清晰，并能暴露语言切换、术语保持和回答边界问题。
EN: They should be short, clear, and able to expose language switching, terminology retention, and answer-boundary issues.

## Explanation
Q: 为什么不能一开始就用很长的综合题？
EN: Why not start with long comprehensive prompts?

A: 因为 smoke 阶段的目标是快速发现明显异常，而不是证明全面能力。
EN: Because the goal of a smoke stage is to quickly reveal obvious failures, not to prove broad capability.

Q: 评价时看什么信号？
EN: What signals do you inspect during evaluation?

A: 看模型是否遵守语言要求、是否保留关键术语、是否把回答截断在奇怪位置。
EN: Check whether the model follows the language requirement, preserves key terms, and avoids cutting off answers at strange points.

## Minimal Example
- Prompt: “用中文解释 attention mask，并保留英文术语 attention mask。”
- Prompt: “Explain checkpoint reload in English, but keep the term 验证集 as Chinese.”

A: 这类 prompt 可以快速暴露跨语言术语保留是否稳定。
EN: Prompts like these quickly reveal whether cross-language term retention is stable.

## Common Pitfalls
- 用过难 prompt，导致失败原因难以归因。
- Using prompts that are too hard and making failures hard to attribute.

- 所有评测 prompt 都是同一语言，失去双语 smoke 的意义。
- Making every evaluation prompt single-language and losing the point of a bilingual smoke.

- 只看表面流畅度，不看 instruction follow。
- Looking only at fluency and not instruction following.

## Review Notes
- Draft queue only; review required before promotion.
- These prompts are educational smoke examples, not a benchmark suite.
