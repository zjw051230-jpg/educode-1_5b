# RoPE Position Encoding V2

This branch adds RoPE helper functions and position-encoding schema support while keeping learned position embeddings as the default.

## Implemented Scope

- `rotate_half`.
- RoPE cos/sin cache helper.
- `apply_rotary_emb` for q/k tensors.
- Position encoding schema support for:
  - `learned`
  - `learned_position_embedding`
  - `rope`
- Rejection of invalid head dimensions and invalid scaling factors.
- Feasibility placeholders for NTK, YaRN, and LongRoPE.
- Synthetic passkey retrieval fixture generator.

## Non-Goals

- RoPE is not wired into `TinyDecoderOnlyTransformer`.
- Existing checkpoint assumptions are not changed.
- NTK, YaRN, and LongRoPE algorithms are not implemented.
- No GPU run, training, or long-context claim.

## Local Validation

```powershell
.\.venv\Scripts\python.exe -m py_compile src\educode\rope.py src\educode\position_encoding.py src\educode\config_validator.py scripts\validate_position_encoding.py scripts\generate_passkey_fixture.py tests\test_rope_cache.py tests\test_position_encoding.py
.\.venv\Scripts\python.exe scripts\validate_position_encoding.py
.\.venv\Scripts\python.exe scripts\generate_passkey_fixture.py --prefix-tokens 4 --suffix-tokens 4
.\.venv\Scripts\python.exe tests\test_rope_cache.py
.\.venv\Scripts\python.exe tests\test_position_encoding.py
git diff --check
```

## Future Gate

Wiring RoPE into the model or running long-context profiling requires checkpoint compatibility review, readiness validation, and explicit GPU/Modal cost confirmation.
