# T5.3 BPE 8k Tokenizer Artifact

## 1. Purpose
The purpose of T5.3 is to train a formal-path `educode_bpe_8k` tokenizer artifact using the current processed synthetic seed corpus.

This step validates the tokenizer artifact path, basic tokenizer behavior, and downstream artifact packaging without running any model training.

## 2. Files Added
- `scripts/train_bpe_8k_tokenizer.py`
- `scripts/inspect_bpe_8k_tokenizer.py`
- `tokenizers/educode_bpe_8k/tokenizer.json`
- `tokenizers/educode_bpe_8k/tokenizer_config.json`
- `tokenizers/educode_bpe_8k/special_tokens_map.json`
- `tokenizers/educode_bpe_8k/README.md`
- `tokenizers/educode_bpe_8k/vocab.json`
- `tokenizers/educode_bpe_8k/merges.txt`

## 3. Corpus Used
Tokenizer training used:
- `data/real_corpus/processed/synthetic_seed.processed.jsonl`
- train split only

Observed corpus counts:
- input docs: `8`
- train docs used: `7`
- validation docs excluded from tokenizer training: `1`

This corpus is the project-authored synthetic seed corpus only.
It is not a real or production corpus.

## 4. Tokenizer Config
Configured tokenizer settings:
- name: `educode_bpe_8k`
- type: `BPE`
- library: Hugging Face `tokenizers`
- target vocab size: `8192`
- observed vocab size: `1174`
- special tokens:
  - `<pad>` → id `0`
  - `<bos>` → id `1`
  - `<eos>` → id `2`
  - `<unk>` → id `3`

Implementation note:
- the tokenizer uses byte-level pre-tokenization and byte-level decoding
- this helps preserve round-trip behavior for English, Chinese, code, math text, and emoji samples even on a small corpus

## 5. Observed Result
Training completed successfully.

Observed result:
- target vocab size: `8192`
- observed vocab size: `1174`
- tokenizer artifact directory created successfully
- `tokenizer.json` saved successfully
- `tokenizer_config.json` saved successfully
- `special_tokens_map.json` saved successfully
- `README.md` saved successfully
- `vocab.json` saved successfully
- `merges.txt` saved successfully

The observed vocabulary is smaller than the target.
This is expected because the current synthetic corpus is too small to support a full 8k vocabulary.
This should be treated as a small-corpus limitation, not as a training failure.

## 6. Round Trip Results
Inspection samples and results:
- `hello world` → pass
- `你好，世界` → pass
- `Python code: print('hello')` → pass
- `Transformer models predict the next token.` → pass
- `loss = F.cross_entropy(logits, targets)` → pass
- `Emoji test 😊` → pass

All inspected round trips were exact in this T5.3 run.

## 7. What It Does Not Do
This step does not:
- train a model
- run model training
- claim production tokenizer quality
- use real external corpus data
- download data
- install packages
- execute `git push`

## 8. Limitations
Current limitations:
- the tokenizer was trained only on the synthetic seed corpus
- it is not a production tokenizer
- the corpus is too small and too narrow to realize a full 8k vocabulary
- the artifact validates the formal path shape, not real-data readiness
- a future broader corpus should be used to retrain the tokenizer before formal downstream claims

## 9. Next Step
Recommended next step:
- T5.4: validate `configs/windows/bpe_8k_formal_placeholder.json` against the trained `educode_bpe_8k` artifact
- or T6: validation loop planning for future train/validation usage
