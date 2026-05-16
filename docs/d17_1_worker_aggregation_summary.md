# D17.1 Worker Aggregation Summary

## 1. Purpose
The purpose of this summary is to aggregate the six worker receipts for the `domain_synthetic_batch_03` draft queue and preserve the expected worker-level delivery picture for D17.1.

## 2. Worker Receipt Summary
Worker receipt summary provided for D17.1 aggregation:
- `CC-1`: 20 topic files, 16 md / 4 py
- `CC-2`: 20 topic files, 12 md / 8 py
- `CC-3`: 20 topic files, 16 md / 4 py
- `CC-4`: 20 topic files, 14 md / 6 py
- `CC-5`: 20 topic files, 16 md / 4 py
- `CC-6`: 20 topic files, 4 md / 16 py

## 3. Known Notes
Known notes across the worker receipts:
- some workers used `git status` instead of `git diff` because the generated files were untracked
- some secret/token hits were explanatory-only rather than credential-like
- no worker ran intake, tokenizer training, or model training
- no worker created a git commit
- no worker performed a git push

## 4. Validation Interpretation
These worker summaries are useful as receipt-style aggregation records.
The authoritative D17.1 pass/fail decision still comes from the registry-driven validator and the observed draft queue contents.

Observed validator counts differed from the worker receipt counts for two workers:
- `CC-3`: validated as `15` markdown / `5` python
- `CC-6`: validated as `5` markdown / `15` python

These observed counts are the authoritative D17.1 state.
The receipt summary above is preserved as the worker-reported delivery picture rather than the final validator output.

## 5. Current State
All aggregated outputs remain:
- draft-only
- review-only
- `approved_for_training: false`
- outside the formal corpus and intake pipeline

## 6. Next Step
Recommended next step:
- D17.2 draft corpus review gate
