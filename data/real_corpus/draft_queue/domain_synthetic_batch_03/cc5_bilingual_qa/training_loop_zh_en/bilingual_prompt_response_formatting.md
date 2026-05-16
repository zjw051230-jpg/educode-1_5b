---
draft_status: candidate
topic_id: BIL-008
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC5
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
---

# Bilingual Prompt and Response Formatting

## Concept
Q: 为什么 bilingual prompt/response formatting 要刻意设计？
EN: Why should bilingual prompt/response formatting be designed deliberately?

A: 因为问答模板决定了模型在哪些位置看到 instruction、context 和 answer。
EN: Because the Q&A template determines where the model sees instruction, context, and answer.

## Explanation
Q: 在中英双语里，最常见的格式目标是什么？
EN: What is the most common formatting goal in bilingual data?

A: 让中英文都能清楚地区分“问题部分”和“回答部分”，同时保持样本长度可控。
EN: Let both Chinese and English clearly distinguish the question part from the answer part while keeping sample length manageable.

Q: 这和 training loop 有什么关系？
EN: How does that relate to the training loop?

A: 如果模板边界混乱，loss 变化可能来自格式漂移，而不是来自内容质量。
EN: If template boundaries are messy, loss changes may come from format drift rather than content quality.

## Minimal Example
- Q: 什么是 attention mask？
- EN: Q: What is an attention mask?
- A: 它控制哪些位置可以被当前 token 看到。
- EN: A: It controls which positions the current token may attend to.

A: 这个示例里，中英文不是逐句直译，而是围绕同一教学点保持对齐。
EN: In this example, the Chinese and English are not sentence-for-sentence translations; they align around the same teaching point.

## Common Pitfalls
- 把双语样本写成两份互不相关的短文，而不是一组对应问答。
- Writing two unrelated mini-articles instead of one aligned Q&A sample.

- 模板里使用过多解释性前缀，挤占有效 token 预算。
- Using too many explanatory prefixes in the template and wasting token budget.

- 中文问题很短、英文回答很长，导致训练重心失衡。
- Making Chinese questions tiny and English answers much longer, causing imbalance.

## Review Notes
- Draft queue only; review required before promotion.
- Formatting should make the supervision boundary obvious to a reviewer, not merely decorative.
