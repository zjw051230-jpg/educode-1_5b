---
draft_status: candidate
topic_id: BIL-009
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC5
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
---

# Language Balance in Tiny Batches

## Concept
Q: tiny batch 里为什么要关注语言平衡？
EN: Why care about language balance in tiny batches?

A: 因为 batch 很小时，少量样本就足以让梯度方向明显偏向某一语言模式。
EN: Because when batches are tiny, only a few samples can noticeably steer gradients toward one language pattern.

## Explanation
Q: 这是不是要求每个 batch 都必须 50/50？
EN: Does this mean every batch must be exactly 50/50?

A: 不一定。更实际的目标是避免连续很多步都只看到单一语言或单一模板。
EN: Not necessarily. A more practical goal is to avoid long stretches where the model sees only one language or one template.

Q: 如果某一步中文更多，会怎样？
EN: What if one step contains more Chinese?

A: 单步偏斜通常可以接受，但如果整个短跑实验长期偏斜，就会让验证观察失真。
EN: A one-step skew is usually acceptable, but if a whole short run stays skewed, validation observations become misleading.

## Minimal Example
A: 假设 4 个样本的 mini-batch 中，3 个是中文 tokenizer 问题，1 个是英文 checkpoint 问题。
EN: Suppose a 4-sample mini-batch contains three Chinese tokenizer questions and one English checkpoint question.

A: 这未必错误，但如果下一个 batch 还是相同分布，就值得记录。
EN: That is not necessarily wrong, but if the next batch repeats the same pattern, it is worth logging.

## Common Pitfalls
- 只统计样本数，不统计 token 数。
- Counting samples only and not token volume.

- 只看语言比例，不看主题比例。
- Watching language ratios while ignoring topic ratios.

- 把偶然波动误判成系统性偏差。
- Misreading random fluctuation as systematic bias.

## Review Notes
- Draft queue only; review required before promotion.
- The point is to teach balancing intuition for smoke-scale loops, not to define a production sampler.
