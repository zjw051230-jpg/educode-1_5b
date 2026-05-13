# T5.4 BPE 8k Config Linkage Validation

## 1. Purpose
The purpose of T5.4 is to validate config-level linkage between the formal BPE placeholder config and the trained `educode_bpe_8k` tokenizer artifact.

This step checks that the config now points to the real tokenizer artifact, that vocab sizes are aligned, and that repository-aware config validation passes.

## 2. Files Updated
- `configs/windows/bpe_8k_formal_placeholder.json`
- `scripts/inspect_bpe_8k_config_linkage.py`
- `docs/t5_4_bpe_8k_config_linkage.md`

## 3. Validation Result
Observed validation result:
- config status: `ready_for_config_smoke`
- tokenizer path: `tokenizers/educode_bpe_8k/tokenizer.json`
- tokenizer.vocab_size: `1174`
- loaded tokenizer vocab size: `1174`
- model.vocab_size: `1174`
- config validation: `passed`

The formal placeholder config is now linked to the trained tokenizer artifact at the config-validation level.

## 4. Observed Vocab Size
- observed vocab size = `1174`
- target vocab size = `8192`

## 5. Why Observed < Target
The observed vocabulary is smaller than the target because the current synthetic seed corpus is small and narrow.

This is expected for the current stage:
- the tokenizer artifact was trained only on the processed synthetic seed corpus
- the corpus does not contain enough variety or scale to realize a full 8192-token vocabulary
- the current linkage validation is about config/artifact correctness, not corpus adequacy for a final tokenizer

## 6. What It Does Not Do
This step does not:
- train a tokenizer
- train a model
- run model training
- download data
- install packages
- claim production tokenizer readiness
- execute `git push`

## 7. Next Step
Recommended next step:
- T6 validation loop plan
- or T5.5 BPE-based data/model/loss smoke
