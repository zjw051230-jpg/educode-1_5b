# MoE Routing Prep

This branch prepares a local MoE routing skeleton while keeping the current dense decoder baseline unchanged.

## Implemented Scope

- Adds `TopKRouter` with top-k expert selection and normalized routing weights.
- Adds `ExpertMLP` and `SparseMoESkeleton` for shape and routing metadata tests.
- Adds optional `moe` config validation fields.
- Keeps `moe.enabled=false` valid.
- Rejects `moe.enabled=true` in training configs because MoE is prepared-only.

## Non-Goals

- MoE is not wired into `TinyDecoderOnlyTransformer`.
- No MoE training.
- No GPU or Modal run.
- No quality or throughput claim.

## Local Validation

```powershell
.\.venv\Scripts\python.exe -m py_compile src\educode\moe_layers.py src\educode\config_validator.py scripts\validate_moe_routing.py tests\test_moe_routing.py
.\.venv\Scripts\python.exe scripts\validate_moe_routing.py
.\.venv\Scripts\python.exe tests\test_moe_routing.py
git diff --check
```

## Future GPU/Modal Gate

MoE should not be enabled for training until there is a separate architecture plan, dispatch/load-balancing implementation, artifact validator updates, and explicit user cost confirmation.
