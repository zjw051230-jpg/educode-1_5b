# Config Schema Hardening

This branch adds an enhanced local config schema checker. It does not replace the existing readiness gates and does not run any experiment.

## Implemented Scope

- Infers or validates run type:
  - `training_execution`
  - `bounded_profile`
  - `memory_preflight`
- Keeps these existing configs valid:
  - 5GB 3000-step training
  - seq512 50-step SDPA profile
  - seq1024 10-step memory preflight
  - seq1024 50-step SDPA profile
- Adds extra checks for:
  - max step bounds
  - context length bounds
  - attention backend names
  - optimizer names
  - experimental Muon use
  - MoE enablement
  - checkpoint path escaping
  - result package naming when present

## Non-Goals

- No Modal run.
- No GPU use.
- No training.
- No replacement of `scripts/check_a100_execution_readiness.py`.
- No weakening of existing execution gates.

## Local Validation

```powershell
.\.venv\Scripts\python.exe -m py_compile src\educode\config_schema.py scripts\validate_config_schema_hardening.py tests\test_config_schema_hardening.py
.\.venv\Scripts\python.exe scripts\validate_config_schema_hardening.py
.\.venv\Scripts\python.exe tests\test_config_schema_hardening.py
git diff --check
```

## Future Gate

Future experimental configs should pass this schema checker before any cost-bearing A100/Modal run is proposed.
