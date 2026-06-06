# Dataset Quality / Dedup Skeleton

This branch adds tiny, local-only dataset quality and near-duplicate utilities. It does not scan large corpora or modify any dataset files.

## Included

- Character, line, token, unique token, repetition, and ASCII-fraction metrics.
- Shingle Jaccard similarity.
- Pairwise near-duplicate detection for tiny fixtures.
- Synthetic dataset quality report script.

## Command

```powershell
.\.venv\Scripts\python.exe scripts\analyze_dataset_quality.py
```

## Guardrails

- Modal run: no.
- GPU run: no.
- Training run: no.
- Large raw/prepared data read: no.
- Dataset rewrite: no.
- Tarball/checkpoint touched: no.

## Future Work

- Add streaming-safe sampling from committed tiny fixtures.
- Add MinHash for larger batches only after a separate resource review.
- Add source-level quality gates before future training-data promotion.
