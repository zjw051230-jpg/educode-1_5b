# D4 Expanded BPE Tokenizer

## 1. Purpose
The purpose of D4 is to train a new BPE tokenizer artifact using the processed expanded synthetic corpus train split only.

This step updates the tokenizer path to reflect the larger synthetic corpus intake from D3 without training a model or changing model code.

## 2. Corpus Used
Input corpus:
- `data/real_corpus/processed/synthetic_expanded.processed.jsonl`

Selection rule:
- prefer records with `split = train`

Observed corpus usage:
- input docs: `15`
- train docs used: `13`
- validation docs excluded from tokenizer training: `2`

## 3. Tokenizer Artifact
Artifact directory:
- `tokenizers/educode_bpe_expanded_8k/`

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
- observed vocab size: `1846`

This is not treated as a failure.
The current expanded synthetic corpus is still small relative to the requested target vocabulary.

## 5. Special Token IDs
Observed token ids:
- `<pad>`: `0`
- `<bos>`: `1`
- `<eos>`: `2`
- `<unk>`: `3`

## 6. Round Trip Results
Inspection script:
- `scripts/inspect_expanded_bpe_tokenizer.py`

Test samples:
- `hello world`
- `你好，世界`
- `Python code: print('hello')`
- `Transformer models predict the next token.`
- `loss = F.cross_entropy(logits, targets)`
- `A100 2.15B seq512 optimizer profile`
- `Emoji test 😊`

Observed result:
- all round trips exact: `true`
- failed input count: `0`

## 7. What It Does Not Do
This step does not:
- download data
- copy external corpora
- train a model
- run model training
- modify model code
- perform `git push`

## 8. Limitations
- the tokenizer is still trained on a small synthetic corpus rather than a broad real-world dataset
- observed vocabulary remains far below the target size because corpus coverage is limited
- round-trip success on a small inspection set does not prove downstream model quality
- this step validates tokenizer artifact generation, not full data/model integration

## 9. Next Step
Recommended next step:
- D5 expanded BPE data/model/loss smoke
