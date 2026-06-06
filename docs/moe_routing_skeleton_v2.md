# MoE Routing Skeleton V2

This branch adds local-only MoE routing scaffolding. The dense baseline remains unchanged and MoE is rejected when enabled in training configs.

## Implemented Scope

- `TopKRouter` with normalized top-k weights.
- Load-balancing auxiliary loss.
- Router z-loss.
- Expert capacity helper.
- Synthetic-safe token dispatch/combine helpers.
- MoE FFN skeleton that returns routing metadata.
- Config validation for `moe.enabled=false` and rejection for `moe.enabled=true`.

## Non-Goals

- MoE is not wired into the main training model.
- No expert parallelism.
- No GPU or Modal run.
- No quality, speed, or load-balancing claim on real training.

## Local Validation

```powershell
.\.venv\Scripts\python.exe -m py_compile src\educode\moe_routing.py src\educode\moe_layers.py src\educode\config_validator.py scripts\validate_moe_routing.py tests\test_moe_routing.py tests\test_moe_losses.py tests\test_moe_config.py
.\.venv\Scripts\python.exe scripts\validate_moe_routing.py
.\.venv\Scripts\python.exe tests\test_moe_routing.py
.\.venv\Scripts\python.exe tests\test_moe_losses.py
.\.venv\Scripts\python.exe tests\test_moe_config.py
git diff --check
```

## Future Gate

Any MoE training, routing load-balance claim, or throughput comparison requires a separate architecture branch, artifact validation updates, and explicit GPU/Modal cost confirmation.
