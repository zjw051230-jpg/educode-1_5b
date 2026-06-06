# FlashAttention Feasibility

This branch adds a local-only FlashAttention2 feasibility checker. It prepares an optional future path without installing dependencies, running GPU code, or claiming measured performance.

## Implemented Scope

- Records local Python, platform, PyTorch, CUDA, and `flash_attn` package availability.
- Treats missing `flash_attn` as an unavailable/caveat state, not as a project import failure.
- Provides a disabled future config shape for `profiling.attention_backend = flash_attention_2`.
- Rejects bad future configs such as unknown backends, enabling FlashAttention while keeping SDPA, or unsupported dtypes.

## Non-Goals

- No `flash_attn` installation.
- No Modal run.
- No GPU use.
- No training, profiling, or throughput claim.
- No assertion that FlashAttention2 will work on Windows exactly as it would on Modal Linux/CUDA.

## Local Validation

```powershell
.\.venv\Scripts\python.exe -m py_compile scripts\check_flashattention_feasibility.py tests\test_flashattention_feasibility.py
.\.venv\Scripts\python.exe scripts\check_flashattention_feasibility.py
.\.venv\Scripts\python.exe tests\test_flashattention_feasibility.py
git diff --check
```

## Future GPU/Modal Gate

Any real FlashAttention2 validation needs a separate branch and explicit user approval for dependency installation risk and A100 cost. The first real run should be bounded and should compare against the existing SDPA profile only after artifact validation is ready.
