# Attention Backend Abstraction

This branch introduces a small attention backend abstraction for the decoder-only model. The default backend remains PyTorch SDPA.

## Implemented Scope

- `sdpa` remains the default backend.
- `naive` causal attention is available for small CPU/synthetic comparisons.
- `flash_attention_2` is represented as an optional backend with an availability guard.
- Missing `flash_attn` reports unavailable instead of breaking project imports.
- Bad backend names are rejected before model execution.

## Non-Goals

- This does not install FlashAttention2.
- This does not run GPU profiling.
- This does not claim SDPA is faster than naive attention or FlashAttention2.
- This does not change the default training backend.

## Local Validation

```powershell
.\.venv\Scripts\python.exe -m py_compile src\educode\attention_backends.py src\educode\tiny_model.py scripts\check_attention_backend_availability.py tests\test_attention_backends.py
.\.venv\Scripts\python.exe scripts\check_attention_backend_availability.py
.\.venv\Scripts\python.exe tests\test_attention_backends.py
git diff --check
```

## GPU/Modal Gate

Future backend profiling, including naive baseline measurement or FlashAttention2 benchmarking, requires a separate config/mode, explicit user cost confirmation, and a bounded A100 run. No such run is part of this branch.
