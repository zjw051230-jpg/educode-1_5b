---
draft_status: candidate
topic_id: BIL-020
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC5
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
---

# Bilingual Reserved Topic Triage

## Concept
Q: reserved topic triage 在 bilingual draft queue 中是什么意思？
EN: What does reserved topic triage mean in a bilingual draft queue?

A: 它表示对已经分配但尚未正式晋级的 topic 做完整性和范围检查。
EN: It means checking assigned-but-not-promoted topics for completeness and scope discipline.

## Explanation
Q: triage 时主要看什么？
EN: What do you mainly inspect during triage?

A: 看 topic 是否已生成、文件名是否匹配 registry、文件类型是否正确、内容是否仍在教学主题范围内。
EN: Inspect whether the topic was generated, whether the filename matches the registry, whether the file type is correct, and whether the content still stays inside the educational scope.

Q: 为什么对 bilingual worker 特别需要这个步骤？
EN: Why is this step especially useful for a bilingual worker?

A: 因为 bilingual 文件既要满足格式约束，又要满足语言对齐约束，遗漏点更多。
EN: Because bilingual files must satisfy both formatting constraints and cross-language alignment constraints, so there are more ways to drift.

## Minimal Example
- 检查 BIL-001 到 BIL-020 是否全部存在。
- Check whether all files from BIL-001 to BIL-020 exist.

- 检查 .md 是否带 YAML metadata，.py 是否带注释 metadata。
- Check that .md files carry YAML metadata and .py files carry comment metadata.

- 检查内容是否为原创 synthetic educational examples。
- Check that the content remains original synthetic educational material.

## Common Pitfalls
- 只检查文件数量，不检查每个 topic_id 是否对应正确文件。
- Checking file counts only and not topic-to-file mapping.

- 只检查文件后缀，不检查 header 元数据。
- Checking extensions only and not header metadata.

- 看到内容完整就忽略越界主题。
- Ignoring scope drift because the file looks complete.

## Review Notes
- Draft queue only; review required before promotion.
- This triage note is procedural and intended for self-checking within the worker scope.
