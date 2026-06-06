# Serving API Skeleton

This branch adds a local serving API skeleton for future checkpoint inference. It uses a fake backend and does not load a real model.

## Scope

- Generate request and response schema.
- Fake deterministic model backend.
- Health response.
- Model metadata response.
- Optional FastAPI app builder with graceful fallback if FastAPI is unavailable.
- Local validator that does not start an HTTP server.

## Safety Boundaries

- No checkpoint is loaded.
- No server is started by validation.
- No GPU, Modal, training, profiling, or preflight is run.
- The fake backend is only a contract test fixture.

## Validation

```powershell
.\.venv\Scripts\python.exe -m py_compile src\educode\serving_schema.py src\educode\serving.py scripts\validate_serving_api.py tests\test_serving_schema.py
.\.venv\Scripts\python.exe scripts\validate_serving_api.py
.\.venv\Scripts\python.exe tests\test_serving_schema.py
git diff --check
```

Future real serving work requires checkpoint hygiene, inference memory planning, endpoint security review, and explicit approval before running a server or GPU-backed inference.
