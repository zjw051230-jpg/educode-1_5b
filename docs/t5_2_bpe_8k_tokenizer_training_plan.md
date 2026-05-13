# T5.2 BPE 8k Tokenizer Training Plan

## 1. Purpose
The purpose of T5.2 is to define the formal training path for the future `educode_bpe_8k` tokenizer artifact.

This step stays at the planning level only.
It does not train the tokenizer, does not create tokenizer artifacts, and does not run model training.

## 2. Current Baseline
Current baseline state:
- synthetic seed corpus has been created
- intake and cleaning have been completed
- processed docs = 8
- train docs = 7
- val docs = 1
- dropped files = 0
- secrets found = false
- the current learned BPE path is only the toy BPE artifact with vocab size 311
- the formal BPE 8k artifact has not been created yet

## 3. Tokenizer Target
Planned tokenizer target:
- name: `educode_bpe_8k`
- type: `BPE`
- library: Hugging Face `tokenizers`
- target `vocab_size`: `8192`
- special tokens:
  - `<pad>`
  - `<bos>`
  - `<eos>`
  - `<unk>`
- artifact path:
  - `tokenizers/educode_bpe_8k/`

## 4. Training Corpus
Planned tokenizer training corpus:
- `data/real_corpus/processed/synthetic_seed.processed.jsonl`
- use only train split text for tokenizer training if possible
- do not use validation split text unless that choice is explicitly documented

Important limitations:
- the current corpus is very small and may not practically fill an 8192-token vocabulary
- if observed vocab size is below 8192, that is an expected limitation for the current corpus
- once larger real or permissively licensed corpus data is added later, the tokenizer should be retrained on the broader corpus

## 5. Required Artifacts
Future T5.3 should generate:
- `tokenizers/educode_bpe_8k/tokenizer.json`
- `tokenizer_config.json`
- `special_tokens_map.json`
- `README.md`
- `vocab.json` / `merges.txt` if available

## 6. Validation Checks
Future T5.3 must verify:
- tokenizer loads successfully
- observed vocab size
- special token ids
- English round trip
- Chinese round trip
- code snippet round trip
- math text round trip
- empty string behavior
- long text behavior

## 7. Config Integration
Config integration notes:
- `configs/windows/bpe_8k_formal_placeholder.json` is currently `not_ready`
- after T5.3 or T5.4, the formal path should point to `tokenizers/educode_bpe_8k/tokenizer.json`
- `model.vocab_size` must equal `tokenizer.vocab_size`
- if observed vocab size stays below 8192, a later decision is needed:
  - accept the observed vocab size for a small formal-path smoke
  - or increase corpus coverage before formal config validation

## 8. Risks
Known risks:
- the corpus may be too small to fill an 8k vocabulary
- the synthetic data distribution is too narrow
- the tokenizer may overfit formatting patterns in the synthetic corpus
- the final real-data tokenizer must be retrained on a better corpus
- this tokenizer must not be described as a production tokenizer

## 9. What T5.2 Does Not Do
This step does not:
- train the tokenizer
- create tokenizer artifacts
- train a model
- download data
- modify configs
- execute `git push`

## 10. Next Step
Recommended next step:
- T5.3: train `educode_bpe_8k` tokenizer on the current processed synthetic seed corpus as a formal-path smoke artifact.
