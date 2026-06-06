# Muon Optimizer Experimental

This branch adds a guarded Muon experiment path while keeping AdamW as the default optimizer. Muon is experimental and requires explicit acknowledgement before construction.

## Implemented Scope

- Optimizer registry with `adamw` and `muon_experimental`.
- AdamW remains default.
- Newton-Schulz orthogonalization helper for synthetic 2D matrices.
- Experimental Muon optimizer step for 2D parameters.
- Parameter grouping helper:
  - 2D hidden matrices enter Muon candidates.
  - embeddings, norms, bias terms, and LM head enter AdamW side.
- Config validator rejects bad optimizer names.
- Muon config requires `optimizer.experimental_ack_required=true`.

## Non-Goals

- No real training.
- No claim that Muon improves loss, throughput, or stability.
- No production optimizer policy.
- No change to existing AdamW training configs.

## Local Validation

```powershell
.\.venv\Scripts\python.exe -m py_compile src\educode\optimizers.py src\educode\muon.py src\educode\config_validator.py scripts\validate_optimizer_registry.py tests\test_optimizer_registry.py tests\test_muon_experimental.py
.\.venv\Scripts\python.exe scripts\validate_optimizer_registry.py
.\.venv\Scripts\python.exe tests\test_optimizer_registry.py
.\.venv\Scripts\python.exe tests\test_muon_experimental.py
git diff --check
```

## Future Gate

Any AdamW vs Muon comparison requires a dedicated bounded training config, artifact validation, and explicit user cost confirmation. This branch only validates local synthetic behavior.
