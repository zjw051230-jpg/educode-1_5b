# W10.1 Config Loader Only

## 1. Purpose
This step only implements a minimal JSON config loader.

## 2. Files Added
- `src/educode/config_loader.py`
- `scripts/inspect_config.py`

## 3. What It Does
This step:
- reads JSON
- returns a dict
- prints a compact summary
- supports inspection of `configs/windows/smoke_cuda_10m.json`

## 4. What It Does Not Do
This step does not:
- train
- initialize a model
- import torch
- implement tokenizer / model / training
- validate the full schema
- download data or models

## 5. Test Command
Executed command:

```text
python D:/Projects/educode-1_5b/scripts/inspect_config.py configs/windows/smoke_cuda_10m.json
```

## 6. Observed Result
`inspect_config.py` successfully loaded the Windows smoke config and printed the expected summary fields, including hardware target, tokenizer settings, model dimensions, training batch settings, and attention backend.

## 7. Next Step
Suggested W10.2:
- config validator only
- check target
- check `d_model % num_heads == 0`
- check vocab size consistency
- still do not write training code
