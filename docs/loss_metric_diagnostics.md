# Loss Metric Diagnostics

This branch adds a CPU-only diagnostics layer for imported `metrics.jsonl` and `validation_metrics.jsonl` files.

## What It Checks

- JSONL parsing for committed imported artifact metrics.
- Finite train loss checks.
- Non-finite loss step reporting.
- Simple adjacent-step spike detection.
- Rolling average helper for small local analysis.
- Validation divergence caveat when validation loss is much higher than train loss.
- Mean `tokens_per_sec` when throughput fields are present.

## Command

```powershell
.\.venv\Scripts\python.exe scripts\analyze_loss_diagnostics.py
```

Optional report outputs:

```powershell
.\.venv\Scripts\python.exe scripts\analyze_loss_diagnostics.py --output-json docs/generated_reports/loss_diagnostics.json --output-md docs/generated_reports/loss_diagnostics.md
```

## Guardrails

- Modal run: no.
- GPU run: no.
- Training run: no.
- Tarball/checkpoint/raw data read: no.
- The diagnostics are not model-quality claims; they are local sanity and anomaly checks.
