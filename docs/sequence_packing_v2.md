# Sequence Packing v2

This branch extends sequence packing utilities with document boundary metadata and mask skeletons. It uses synthetic fixtures only.

## Included

- Sequence packing estimator.
- Document boundary metadata builder.
- Padding waste estimator.
- Loss mask skeleton.
- Cross-document attention flag.
- JSON report script.

## Commands

```powershell
.\.venv\Scripts\python.exe scripts\build_packing_report.py
.\.venv\Scripts\python.exe scripts\analyze_token_utilization_v2.py
```

## Guardrails

- Modal run: no.
- GPU run: no.
- Training run: no.
- Raw data rewrite: no.
- Tarball/checkpoint touched: no.
