# Sequence Packing / Data Utilization

This branch adds small sequence-packing utilities for future training data efficiency work. It uses synthetic document token lengths only and does not rewrite or read large datasets.

## Included

- Document length packing under a fixed context length.
- Token utilization report.
- Padding waste estimator.
- Local script for synthetic utilization checks.

## Command

```powershell
.\.venv\Scripts\python.exe scripts\analyze_token_utilization.py --context-length 1024
```

## Guardrails

- Modal run: no.
- GPU run: no.
- Training run: no.
- Raw/prepared data rewrite: no.
- Tarball/checkpoint touched: no.

## Future Work

- Add tokenizer-aware estimates from small committed fixtures.
- Add document-boundary separator accounting.
- Add cost-gated training tests only after a separate implementation review.
