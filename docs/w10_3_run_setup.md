# W10.3 Run Setup Only

## 1. Purpose
This step only implements run setup.

## 2. Files Added
- `src/educode/run_setup.py`
- `scripts/create_run_setup.py`

## 3. What It Does
This step:
- reads config
- validates config
- generates `run_id`
- creates `experiments/<stage>/<run_id>/`
- copies `run_config.json`
- writes `run_metadata.json`

## 4. What It Does Not Do
This step does not:
- train
- initialize a model
- import torch
- implement tokenizer / model / training
- write metrics
- save checkpoints
- generate text

## 5. Test Command
Executed command:

```text
python D:/Projects/educode-1_5b/scripts/create_run_setup.py configs/windows/smoke_cuda_10m.json --stage windows_cuda --short-name smoke_setup
```

## 6. Observed Result
- run setup succeeded
- generated `run_id`: `20260510_195409_windows_cuda_smoke_setup`
- generated `run_dir`: `experiments/windows_cuda/20260510_195409_windows_cuda_smoke_setup/`
- `run_config.json` exists
- `run_metadata.json` exists

## 7. Git Tracking Decision
This step does not commit the actual `experiments/<stage>/<run_id>/` directory.
`create_run_setup.py` generates a local `experiments/<stage>/<run_id>/` run directory.
These generated run directories are ignored by default in `.gitignore`.
They may be kept locally for inspecting `run_config.json` and `run_metadata.json`.
Only the run setup code and documentation are committed.
If a future run summary is worth including in reports, it should be copied or rewritten into `docs/` rather than committing the whole experiment run directory.
Selected summaries may be committed later, but large logs and checkpoints should not be committed.

## 8. Next Step
Suggested W10.4:
- toy data + ByteTokenizer only
- still do not initialize a model
- still do not train
