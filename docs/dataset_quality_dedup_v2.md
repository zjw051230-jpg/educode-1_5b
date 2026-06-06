# Dataset Quality / Dedup v2

This branch extends tiny dataset quality and dedup utilities without scanning real large datasets.

## Included

- Exact duplicate detector.
- Shingle generator and Jaccard similarity.
- Near-duplicate detector for tiny fixtures.
- Quality metrics: doc length, line length, control char ratio, repetition ratio, and low-information flag.
- MinHash feasibility placeholder.
- Local report script.

## Command

```powershell
.\.venv\Scripts\python.exe scripts\analyze_dataset_quality_v2.py
```

## Guardrails

- Modal run: no.
- GPU run: no.
- Training run: no.
- Real large data read: no.
- Raw/prepared data rewrite: no.
