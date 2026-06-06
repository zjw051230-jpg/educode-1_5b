# RoPE Position Encoding Prep

This branch prepares RoPE helper code and config validation for future long-context experiments. It does not wire RoPE into the current dense decoder training path.

## Implemented Scope

- Adds RoPE cache construction.
- Adds rotary application helper for synthetic q/k-style tensors.
- Adds position encoding schema values: `learned`, `learned_position_embedding`, and `rope`.
- Keeps current learned-position model behavior unchanged.
- Rejects unknown `model.position_encoding` values and invalid `rope_theta`.

## Non-Goals

- RoPE is not connected to `TinyDecoderOnlyTransformer`.
- No checkpoint compatibility change.
- No training.
- No GPU or Modal run.
- No long-context performance claim.

## Local Validation

```powershell
.\.venv\Scripts\python.exe -m py_compile src\educode\position_encoding.py src\educode\config_validator.py scripts\validate_rope_position_encoding.py tests\test_position_encoding.py
.\.venv\Scripts\python.exe scripts\validate_rope_position_encoding.py
.\.venv\Scripts\python.exe tests\test_position_encoding.py
git diff --check
```

## Future GPU/Modal Gate

Connecting RoPE to the model requires a separate branch, checkpoint compatibility review, and local/gated tests before any A100 run. Future long-context profiling requires explicit user cost confirmation.
