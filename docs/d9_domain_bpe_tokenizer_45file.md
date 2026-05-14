# D9 Domain BPE Tokenizer on 45-File Corpus

## 1. Purpose
The purpose of D9 is to retrain a domain BPE tokenizer artifact using the refreshed 45-file expanded synthetic corpus outputs from D8.

This step updates the tokenizer artifact to reflect the larger domain-shaped corpus without training a model or modifying model code.

## 2. Corpus Used
Input corpus:
- `data/real_corpus/processed/synthetic_expanded.processed.jsonl`

Selection rule:
- use records with `split = train` only

Observed corpus usage:
- processed docs available: `45`
- train docs used: `41`
- validation docs excluded from tokenizer training: `4`

## 3. Tokenizer Artifact
Artifact directory:
- `tokenizers/educode_bpe_domain_8k/`

Generated files:
- `tokenizer.json`
- `tokenizer_config.json`
- `special_tokens_map.json`
- `README.md`
- `vocab.json`
- `merges.txt`

Tokenizer settings:
- type: `BPE`
- target vocab size: `8192`
- special tokens:
  - `<pad>`
  - `<bos>`
  - `<eos>`
  - `<unk>`

## 4. Observed Vocab Size
Observed result:
- target vocab size: `8192`
- observed vocab size: `3988`

This is not treated as a failure.
The 45-file domain corpus is still small relative to the requested target vocabulary.

## 5. Special Token IDs
Observed token ids:
- `<pad>`: `0`
- `<bos>`: `1`
- `<eos>`: `2`
- `<unk>`: `3`

## 6. Round Trip Results
Inspection script:
- `scripts/inspect_domain_bpe_tokenizer_45file.py`

Test samples:
- `hello world`
- `你好，世界`
- `Python code: print('hello')`
- `Transformer models predict the next token.`
- `loss = F.cross_entropy(logits, targets)`
- `A100 2.15B seq512 optimizer profile`
- `Gradient clipping stabilizes training.`
- `JSONL data pipelines preserve document boundaries.`
- `Emoji test 😊`

Observed result:
- all round trips exact: `true`
- failed input count: `0`

## 7. Comparison with Previous Tokenizer
Previous expanded tokenizer:
- artifact: `tokenizers/educode_bpe_expanded_8k/`
- observed vocab size: `1846`

New domain tokenizer:
- artifact: `tokenizers/educode_bpe_domain_8k/`
- observed vocab size: `3988`

Interpretation:
- the new tokenizer still falls below the target `8192`
- but it captures substantially more distinct mergeable units than the previous expanded tokenizer because it is trained on the refreshed 45-file corpus with 41 train documents

## 8. What It Does Not Do
This step does not:
- download data
- copy external corpora
- train a model
- run model training
- modify model code
- perform `git push`

## 9. Limitations
- the tokenizer is still trained on a small synthetic educational corpus rather than a broad real-world dataset
- observed vocabulary remains below the target size because corpus coverage is still limited
- round-trip success on a small inspection set does not prove downstream model quality
- this step validates tokenizer artifact generation, not full data/model integration

## 10. Next Step
Recommended next step:
- D10 domain BPE data/model/loss smoke
