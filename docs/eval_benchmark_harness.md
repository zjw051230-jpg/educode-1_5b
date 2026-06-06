# Evaluation Benchmark Harness

This branch adds a local synthetic evaluation benchmark harness. It does not download external benchmarks and does not load a real checkpoint.

## Included

- Benchmark task schema.
- Exact-match evaluator.
- Multiple-choice evaluator.
- Perplexity helper for fake logits.
- Evaluator registry.
- JSON smoke output.

## Commands

```powershell
.\.venv\Scripts\python.exe scripts\run_eval_benchmark_smoke.py
.\.venv\Scripts\python.exe scripts\validate_eval_benchmark_harness.py
```

## Guardrails

- Modal run: no.
- GPU run: no.
- Training run: no.
- External benchmark download: no.
- Real checkpoint load: no.
