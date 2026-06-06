# Attention Backend Abstraction V2

This branch extends the local attention backend abstraction while keeping SDPA as the default behavior for existing training configs.

## Implemented Scope

- SDPA backend wrapper.
- Naive/manual causal attention baseline for CPU synthetic comparisons.
- FlashAttention2 optional guard that reports unavailable when `flash_attn` is missing.
- GQA helper for repeating key/value heads to query-head count.
- Backend availability checker.
- Documentation placeholders for FlexAttention and FlashAttention3 feasibility.

## Non-Goals

- No FlashAttention2 installation.
- No FlashAttention3 implementation.
- No FlexAttention implementation.
- No GPU profiling.
- No claim that any backend is faster than another.

## Local Validation

```powershell
.\.venv\Scripts\python.exe -m py_compile src\educode\attention_backends.py src\educode\attention_utils.py src\educode\tiny_model.py scripts\check_attention_backend_availability.py tests\test_attention_backends.py tests\test_attention_gqa.py
.\.venv\Scripts\python.exe scripts\check_attention_backend_availability.py
.\.venv\Scripts\python.exe tests\test_attention_backends.py
.\.venv\Scripts\python.exe tests\test_attention_gqa.py
git diff --check
```

## Future Gate

Backend profiling, FlashAttention2 runtime validation, FlexAttention experiments, or FlashAttention3 feasibility all require separate branches and explicit GPU/Modal cost confirmation.
