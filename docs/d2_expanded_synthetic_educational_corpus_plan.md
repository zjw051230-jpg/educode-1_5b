# D2 Expanded Synthetic Educational Corpus Plan

## 1. Purpose
说明本步规划 project-authored expanded synthetic educational corpus，用于扩大安全可控训练语料。

## 2. Current Baseline
- current synthetic seed corpus: 8 files
- train docs: 7
- val docs: 1
- BPE observed vocab: 1174
- A100 2.15B seq512 50-step profile passed
- 当前不能继续长训，原因是数据太小

## 3. Target Scale
规划第一版 expanded synthetic corpus：
- target raw size: 100KB - 1MB
- target docs: 50 - 200 small documents
- file types: .md, .txt, .py
- language mix: English + Chinese technical notes
- domain: CS / ML / Python / Transformer / training systems

## 4. Content Categories
- tokenizer explanations
- transformer decoder notes
- attention and masking notes
- logits / loss / cross entropy
- training loop explanations
- optimizer and gradient clipping notes
- checkpointing and resume notes
- generation and sampling notes
- CUDA / GPU profiling notes
- data pipeline and JSONL examples
- Python code snippets
- algorithm notes
- bilingual technical Q&A

## 5. Generation Rules
- all content must be project-authored
- no copying external articles
- no course PDF/textbook excerpts
- no private data
- no secrets
- each file should be small and inspectable
- include metadata where useful
- avoid pretending synthetic data is real-world corpus

## 6. Directory Plan
后续 D2.1 可创建：
`data/real_corpus/raw/synthetic_expanded/`

子目录可包括：
- `ml_notes/`
- `python_examples/`
- `transformer_notes/`
- `training_systems/`
- `bilingual_notes/`

## 7. Manifest Plan
后续应创建/更新：
`data/real_corpus/metadata/source_manifest.synthetic_expanded.jsonl`

source_id:
`source_synthetic_expanded_000001`

source_category:
`synthetic_examples`

- allowed_for_training: true
- allowed_to_commit: true
- privacy_risk: none
- license_or_ownership: project_authored

## 8. Intake Plan
D3 应扩展或复用 intake script：
- read synthetic_expanded source
- process .md/.txt/.py
- secret scan
- output processed JSONL
- create train/val split
- write summary

## 9. Tokenizer Plan
D4 应：
- train updated BPE tokenizer
- expect observed vocab closer to target but still may be below 8k
- update tokenizer/model config linkage

## 10. What D2 Does Not Do
- 不创建 corpus 内容
- 不复制数据
- 不训练 tokenizer
- 不训练模型
- 不进入 A100

## 11. Next Step
D2.1: create expanded synthetic corpus source decision and directory skeleton.
