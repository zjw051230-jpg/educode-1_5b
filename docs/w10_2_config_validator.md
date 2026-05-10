# W10.2 Config Validator Only

## 1. Purpose
This step only implements a minimal read-only config validator.

## 2. Files Added or Updated
- `src/educode/config_validator.py`
- `scripts/inspect_config.py`
- `tests/fixtures/bad_config_invalid_heads.json`

## 3. What It Checks
This validator checks:
- required top-level sections
- hardware target
- Windows smoke bounds
- tokenizer / model vocab consistency
- model dimension consistency
- training positive values
- attention backend

## 4. What It Does Not Do
This step does not:
- train
- initialize a model
- import torch
- implement tokenizer / model / training
- use pydantic or jsonschema
- auto-modify config
- download data or models

## 5. Test Commands
Executed commands:

```text
python D:/Projects/educode-1_5b/scripts/inspect_config.py configs/windows/smoke_cuda_10m.json
python D:/Projects/educode-1_5b/scripts/inspect_config.py tests/fixtures/bad_config_invalid_heads.json
```

## 6. Observed Result
- good config validation passed
- bad config validation failed as expected
- observed error summary:
  - `tokenizer.vocab_size must match model.vocab_size`
  - `d_model must be divisible by num_heads`

## 7. Next Step
Suggested W10.3:
- run setup only
- generate `run_id`
- create `experiments/windows_cuda/<run_id>/`
- write `run_metadata.json`
- still do not train or initialize a model
