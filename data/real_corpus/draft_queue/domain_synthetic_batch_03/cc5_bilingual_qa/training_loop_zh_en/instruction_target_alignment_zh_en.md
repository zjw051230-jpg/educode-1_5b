---
draft_status: candidate
topic_id: BIL-011
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC5
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
---

# Instruction and Target Alignment for ZH and EN Data

## Concept
Q: instruction-target alignment 在双语数据里是什么意思？
EN: What does instruction-target alignment mean in bilingual data?

A: 它表示问题的要求、回答的内容和回答语言彼此匹配。
EN: It means the request, the answer content, and the answer language all match each other.

## Explanation
Q: 为什么这个问题在双语里更容易出错？
EN: Why is this easier to get wrong in bilingual settings?

A: 因为一条样本可能同时包含中文指令、英文术语和中英混合答案，边界稍乱就可能让 target 对错位置。
EN: Because one sample may contain a Chinese instruction, English terms, and a mixed answer, so slight boundary confusion can misplace the target.

Q: 对训练有什么后果？
EN: What is the consequence for training?

A: 模型可能学到“看到中文问题时输出英文模板”之类的次优模式。
EN: The model may learn suboptimal habits such as outputting an English template after a Chinese question.

## Minimal Example
Q: 示例？
EN: Example?

A: 如果问题写“请用中文解释 BPE merge”，而答案主体却变成英文长段落，alignment 就变差了。
EN: If the question says “please explain BPE merge in Chinese” but the answer becomes a long English paragraph, alignment worsens.

A: 反过来，若目标是双语回答，就要在 instruction 里明确写出这一点。
EN: Conversely, if the goal is a bilingual answer, the instruction should state that clearly.

## Common Pitfalls
- 语言要求没有写清楚，却希望回答自动保持某种比例。
- Leaving the language requirement implicit and hoping the answer balances itself.

- 问题在讲 tokenizer，答案却跑到训练硬件细节。
- Asking about the tokenizer while answering about hardware details.

- 为了“像双语”而故意把内容打散，反而破坏监督目标。
- Forcing a bilingual feel by scattering content and weakening the supervision target.

## Review Notes
- Draft queue only; review required before promotion.
- Alignment is about request-answer fit, not literal translation symmetry.
