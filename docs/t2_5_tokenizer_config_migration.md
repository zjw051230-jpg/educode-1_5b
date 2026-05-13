# T2.5 Tokenizer Config Migration

## 1. Purpose
The purpose of T2.5 is to split Windows tokenizer configs into byte smoke, toy BPE smoke, and formal BPE placeholder roles.

## 2. Files Added or Updated
- `src/educode/config_validator.py`
- `configs/windows/byte_smoke_10m.json`
- `configs/windows/bpe_toy_512_smoke.json`
- `configs/windows/bpe_8k_formal_placeholder.json`
- `configs/windows/smoke_cuda_10m.json`
- `scripts/inspect_bpe_config_validation.py`
- `scripts/inspect_tokenizer_configs.py`
- `docs/t2_5_tokenizer_config_migration.md`
- `README.md`
- `docs/experiment_index.md`

## 3. Config Split

### byte_smoke_10m.json
- ByteTokenizer / legacy smoke config
- `tokenizer.type = byte`
- `vocab_size = 256`
- should pass validation

### bpe_toy_512_smoke.json
- toy BPE artifact smoke config
- observed `vocab_size = 311`
- should pass validation

### bpe_8k_formal_placeholder.json
- future formal tokenizer config
- tokenizer artifact not created yet
- expected to fail validation until tokenizer exists

### smoke_cuda_10m.json
- legacy early smoke config
- superseded by split configs
- retained for history

## 4. Validation Results
Observed via `scripts/inspect_tokenizer_configs.py`:
- `configs/windows/byte_smoke_10m.json`: passed
- `configs/windows/bpe_toy_512_smoke.json`: passed
- `configs/windows/bpe_8k_formal_placeholder.json`: failed as expected because tokenizer artifact is not ready
- `configs/windows/smoke_cuda_10m.json`: failed as expected as a legacy early smoke config

## 5. Why This Matters
This matters because it:
- avoids mixing byte smoke and BPE smoke intent in the same Windows config name
- avoids config declarations drifting away from tokenizer artifact reality
- prepares the repo for formal tokenizer and real-data integration without pretending it is already ready

## 6. What It Does Not Do
This step does not:
- train a tokenizer
- train a model
- download data
- create the formal 8k tokenizer artifact
- modify the training loop

## 7. Next Step
Recommended next step:
- T3 small real dataset plan

Reason:
- `tokenizers` library is available
- toy BPE artifact already passed smoke validation
- config path validation is now explicit
- the next useful step is planning a small real dataset path instead of extending placeholder tokenizer work
