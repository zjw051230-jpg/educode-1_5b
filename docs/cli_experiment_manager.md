# CLI Experiment Manager

This branch adds a local read-only CLI for project bookkeeping.

## Commands

```powershell
.\.venv\Scripts\python.exe scripts\educode_cli.py list-runs
.\.venv\Scripts\python.exe scripts\educode_cli.py validate-artifacts
.\.venv\Scripts\python.exe scripts\educode_cli.py build-report
.\.venv\Scripts\python.exe scripts\educode_cli.py show-branch-inventory
.\.venv\Scripts\python.exe scripts\educode_cli.py show-next-candidates
```

## Guardrails

- No execution command for model runs.
- No Modal command.
- No GPU use.
- No tarball reads.
- No checkpoint/raw data handling.
