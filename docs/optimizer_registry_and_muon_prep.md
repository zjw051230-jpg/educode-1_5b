# Optimizer Registry And Muon Prep

This branch prepares an optimizer registry for future AdamW vs Muon experiments. AdamW remains the default and only implemented optimizer.

## Implemented Scope

- Adds `src/educode/optimizers.py`.
- Creates AdamW through a registry helper.
- Adds `optimizer.name` validation for `adamw` and `muon_experimental`.
- Keeps `muon_experimental` guarded and unavailable for training by default.
- Adds a local CPU synthetic AdamW step test.

## Muon Caveat

Muon is not implemented here. The registry only reserves the name and prevents accidental use. A real Muon implementation needs a separate design note, formula/source review, optimizer-state tests, and bounded training gate before any comparison with AdamW.

## Non-Goals

- No training.
- No GPU or Modal run.
- No claim that Muon improves loss or throughput.
- No change to existing default optimizer behavior.

## Local Validation

```powershell
.\.venv\Scripts\python.exe -m py_compile src\educode\optimizers.py src\educode\config_validator.py scripts\validate_optimizer_registry.py tests\test_optimizer_registry.py
.\.venv\Scripts\python.exe scripts\validate_optimizer_registry.py
.\.venv\Scripts\python.exe tests\test_optimizer_registry.py
git diff --check
```

## Future GPU/Modal Gate

Any AdamW vs Muon comparison requires explicit user approval, a bounded config, artifact validation, and a cost gate. This branch only creates the local registry and guardrails.
