# Tokenizer Stats Analyzer

This branch adds a tiny tokenizer statistics analyzer for small fixture text. It does not train a tokenizer and does not process large datasets.

## Included

- Token frequency counter.
- Bytes-per-token estimator.
- Special token rate.
- Unknown token rate when an unknown token is configured.
- Compression-ratio proxy.

## Command

```powershell
.\.venv\Scripts\python.exe scripts\analyze_tokenizer_stats.py
```

## Guardrails

- Modal run: no.
- GPU run: no.
- Training run: no.
- Tokenizer training: no.
- Real data package touched: no.

## Future Use

Use this as a lightweight stats layer before deciding whether tokenizer retraining is justified.
