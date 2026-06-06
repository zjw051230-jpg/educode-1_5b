# Inference And Evaluation Harness

## Design Goal

Prepare a local-only inference, generation, and lightweight evaluation harness for future checkpoint analysis.

## Current Implementation Scope

- Greedy token generation.
- Temperature sampling with optional top-k and top-p filtering.
- Small next-token loss and perplexity evaluation over token-id fixtures.
- Metadata-only checkpoint inspection for JSON metadata sidecars.
- CPU-only generation smoke script using a tiny randomly initialized model.

## Non-goals

- No real checkpoint loading.
- No Modal run.
- No GPU run.
- No training run.
- No quality or benchmark claim.

## Safety Boundaries

- Metadata inspection reports `loads_model_weights=false`.
- The smoke script constructs a tiny local model only.
- Future checkpoint inference remains behind a separate explicit run plan.

## Local Validation

```powershell
.\.venv\Scripts\python.exe -m py_compile src\educode\generation.py src\educode\eval.py scripts\run_generation_smoke.py tests\test_generation_eval_harness.py
.\.venv\Scripts\python.exe scripts\run_generation_smoke.py
.\.venv\Scripts\python.exe tests\test_generation_eval_harness.py
git diff --check
```

## GPU/Modal Gate

Future imported-checkpoint inference may need GPU or large checkpoint access. That is a future execution path and is not run in this branch.

Future command shape, not executed in this branch:

```text
python scripts/run_generation_smoke.py --checkpoint <future_imported_checkpoint>
```
