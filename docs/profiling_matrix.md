# Profiling Matrix

This file is generated from committed small JSON summaries. It does not read tarballs, checkpoints, raw data, or prepared data.

## Design Goal

Keep completed systems evidence and near-term experiment candidates in one reviewable place. The matrix helps decide the next local-prep or cost-gated GPU step without treating short profiling runs as quality evidence.

## Current Scope

- Read existing small imported summaries for the 5GB 3000-step run and SDPA profiling/preflight runs.
- Emit a committed JSON matrix and Markdown summary.
- Rank near-term candidates by systems value and risk.

## Non-goals

- No Modal execution.
- No GPU execution.
- No training, profiling, or preflight run.
- No tarball, checkpoint, raw-data, or prepared-data reads.

## Local Validation

```powershell
.\.venv\Scripts\python.exe -m py_compile scripts\build_profiling_matrix.py
.\.venv\Scripts\python.exe scripts\build_profiling_matrix.py
git diff --check
```

## GPU/Modal Gate

Future GPU commands are documented as candidates only. They require an explicit user cost gate before execution.

## Completed Evidence

| id | kind | context | batch | steps | backend | summary tokens/sec | avg step time | peak reserved GiB | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 5gb_3000step_training | training | 512 | 8 | 3000 | sdpa | 47973.37161 | N/A | 8.416016 | completed_imported |
| seq512_sdpa_50step_profile | profiling | 512 | 8 | 50 | sdpa | 44100.712407 | 0.371513 | 8.416016 | completed_imported |
| seq1024_bs4_10step_memory_preflight | memory_preflight | 1024 | 4 | 10 | sdpa | 27151.11506 | 0.603437 | 8.412109 | completed_imported |
| seq1024_bs4_50step_sdpa_profile | profiling | 1024 | 4 | 50 | sdpa | 41430.475003 | 0.395458 | 8.412109 | completed_imported |

## Boundaries

- Completed profiling rows are systems evidence, not model-quality evidence.
- SDPA has not been compared against naive attention or FlashAttention yet.
- Future GPU/Modal runs require explicit cost approval.
- Raw result tarballs and checkpoints are intentionally excluded.
