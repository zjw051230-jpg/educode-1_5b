# Training Report Generator

The training report generator builds a small Markdown summary from imported artifact files already committed under `experiments/`.

It reads:

- `summary.json`
- `metrics.jsonl`
- `validation_metrics.jsonl`

It does not read root-level result tarballs, checkpoints, raw data, prepared data, or Modal volumes. It is intended for local evidence packaging and portfolio review, not for launching runs.

## Command

```powershell
.\.venv\Scripts\python.exe scripts\build_training_report.py
```

Default output:

```text
docs/generated_reports/training_report_summary.md
```

## Scope

- Summarizes run status, row counts, losses, throughput, and GPU memory when present.
- Compares seq512 and seq1024 profiling artifacts at a high level.
- Labels short profiling and preflight losses as sanity signals, not model-quality evidence.

## Guardrails

- Modal run: no.
- GPU run: no.
- Training run: no.
- Tarball/checkpoint/raw data read: no.
- Tarball/checkpoint/raw data commit: no.
