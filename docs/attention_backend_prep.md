# Attention Backend Prep

## Design Goal

Prepare a clear local-only attention backend path for SDPA, naive/manual attention, and future FlashAttention feasibility checks.

## Current Implementation Scope

- `sdpa` remains the default backend.
- `naive` causal attention is available for small CPU synthetic comparison tests.
- `flash_attention_2` is recognized as a supported config name, but only through an availability guard.
- The project does not install or require `flash_attn`.
- Tiny model attention now calls the backend abstraction without changing current SDPA configs.

## Non-goals

- No FlashAttention implementation claim.
- No GPU run.
- No Modal run.
- No training or profiling run.
- No backend performance comparison.

## Safety Boundaries

- Bad backend names are rejected.
- `flash_attention_2` raises a clear unavailable error when `flash_attn` is not installed.
- Existing training configs still default to `sdpa`.

## Local Validation

```powershell
.\.venv\Scripts\python.exe -m py_compile src\educode\attention_backends.py src\educode\tiny_model.py scripts\check_attention_backend_availability.py
.\.venv\Scripts\python.exe scripts\check_attention_backend_availability.py
.\.venv\Scripts\python.exe tests\test_attention_backends.py
git diff --check
```

## GPU/Modal Gate

Future backend profiling commands must remain behind explicit user cost approval. A future run might compare SDPA, naive, and FlashAttention, but this branch does not execute it.

Future command shape, not executed in this branch:

```text
modal run scripts/modal_a100_streaming_runner.py --mode <future_backend_profile_mode>
```
