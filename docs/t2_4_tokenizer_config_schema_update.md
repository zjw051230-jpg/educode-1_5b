# T2.4 Tokenizer Config Schema Update

## 1. Purpose
The purpose of T2.4 is to bring `tokenizer.path` and `tokenizer.artifact_dir` into the config schema and validator path.

## 2. Files Added or Updated
- `docs/config_schema.md`
- `src/educode/config_validator.py`
- `configs/windows/bpe_toy_512_smoke.json`
- `scripts/inspect_bpe_config_validation.py`

## 3. What It Does
This step:
- makes BPE tokenizer config require `tokenizer.path`
- makes the validator check tokenizer artifact paths
- makes the validator check loaded tokenizer vocab size
- makes the validator check `model.vocab_size == tokenizer.vocab_size`
- adds a toy BPE smoke config for config validation

## 4. What It Does Not Do
This step does not:
- run training
- replace the formal training loop
- modify `ByteTokenizer`
- create the formal 8k tokenizer
- download data or models
- modify the 1.5B config

## 5. Validation Result
BPE toy smoke config:
- config: `configs/windows/bpe_toy_512_smoke.json`
- tokenizer vocab size: `311`
- loaded tokenizer vocab size: `311`
- model vocab size: `311`
- validation result: `passed`

## 6. Legacy Config Note
- `configs/windows/smoke_cuda_10m.json` is an early smoke config
- it still declares `bpe` / `8192` but does not provide `tokenizer.path`
- under the updated validator it now fails with: `bpe tokenizer requires tokenizer.path`
- that config should be migrated later or split into byte-smoke and bpe-formal variants
- this step does not force that migration, to avoid breaking the already validated toy pipeline history

## 7. Next Step
Recommended next step:
- T2.5: migrate / split tokenizer configs

Suggested scope:
- byte smoke config
- bpe toy config
- formal bpe 8k config placeholder
