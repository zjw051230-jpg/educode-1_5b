---
draft_status: candidate
topic_id: BIL-005
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC5
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
---

# Unicode Normalization Cautions

## Concept
Q: 为什么 bilingual draft 里也要小心 Unicode normalization？
EN: Why should bilingual drafts also be careful about Unicode normalization?

A: 因为视觉上相同的字符，有时底层编码组合并不相同。
EN: Because characters that look identical can have different underlying Unicode compositions.

## Explanation
Q: 这会对 tokenizer 造成什么影响？
EN: What effect can this have on tokenization?

A: tokenizer 和 BPE merge 看到的是字节与字符序列，而不是“人眼感觉一样”的文本。
EN: The tokenizer and BPE merges see byte and character sequences, not what humans perceive as equivalent text.

A: 如果同一术语在文件 A 和文件 B 中使用了不同 normalization 形式，统计上它们就可能像两个模式。
EN: If the same term appears in different normalization forms across files, statistics may treat them like two separate patterns.

## Minimal Example
Q: 在 bilingual Q&A 中有哪些高风险位置？
EN: What are high-risk spots in bilingual Q&A?

A: 带重音的英文借词、全角与半角符号、以及某些从不同编辑器复制来的引号。
EN: Loanwords with accents, full-width versus half-width symbols, and some quote characters copied from different editors.

A: 重点不是把一切都机械统一，而是知道什么时候“不统一”会制造无意义分裂。
EN: The point is not to normalize everything mechanically, but to know when inconsistency creates meaningless splits.

## Common Pitfalls
- 把 normalization 当成只和英文有关的问题。
- Treating normalization as an English-only problem.

- 只看显示效果，不检查同一术语在多文件中的一致性。
- Looking only at rendered text instead of cross-file consistency for the same term.

- 用过度 aggressive 的规则，反而抹掉本来需要保留的格式差异。
- Using overly aggressive rules that erase distinctions worth preserving.

## Review Notes
- Draft queue only; review required before promotion.
- This note is synthetic and highlights review heuristics rather than prescribing a specific normalization pipeline.
