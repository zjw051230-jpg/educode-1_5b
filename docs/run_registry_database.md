# Run Registry Database Skeleton

This branch adds a local, lightweight run registry skeleton for imported EduCode experiment artifacts. It is intended for tracking completed training, profiling, preflight, and smoke runs without touching raw result tarballs or checkpoint files.

## Scope

- Registry format: JSONL.
- Source artifacts: imported `summary.json` files under `experiments/**/results_imported*/`.
- Supported metadata: run id, run name, run type, success status, context length, batch size, grad accumulation, max steps, attention backend, runtime fields, losses, throughput, and GPU memory summaries.
- Query dimensions: run type, attention backend, context length, batch size, and success.
- External services: none.
- Original artifact mutation: none.

## Files

- `src/educode/run_registry.py`: schema, import helpers, JSONL read/write helpers, and query filters.
- `scripts/build_run_registry.py`: dry-run or optional output writer for imported run summaries.
- `tests/test_run_registry.py`: synthetic summary import, append/load/query coverage, and bad-entry rejection.

## Safety Boundaries

The registry reads small imported metadata files only. It does not read or unpack tarballs, does not load checkpoints, does not touch raw or prepared data, and does not start training or Modal jobs.

## Example Commands

Dry-run scan:

```powershell
.\.venv\Scripts\python.exe scripts\build_run_registry.py
```

Write a local JSONL registry when explicitly requested:

```powershell
.\.venv\Scripts\python.exe scripts\build_run_registry.py --output docs\generated\run_registry.jsonl
```

Filter for SDPA seq1024 profiles:

```powershell
.\.venv\Scripts\python.exe scripts\build_run_registry.py --run-type profile --attention-backend sdpa --context-length 1024
```

## Validation

Local validation for this branch:

```powershell
.\.venv\Scripts\python.exe -m py_compile src\educode\run_registry.py scripts\build_run_registry.py tests\test_run_registry.py
.\.venv\Scripts\python.exe scripts\build_run_registry.py
.\.venv\Scripts\python.exe tests\test_run_registry.py
git diff --check
```

This branch requires no GPU or Modal gate. Future production use should still keep artifact hygiene checks in front of any generated registry committed to git.
