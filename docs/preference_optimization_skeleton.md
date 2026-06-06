# Preference Optimization / DPO Skeleton

This branch adds a small preference optimization skeleton for future instruction or preference tuning work. It does not train a model or load a real preference dataset.

## Included

- `PreferencePair` schema.
- Preference pair validation.
- DPO loss helper for already-computed policy/reference log probabilities.
- Synthetic validator script.

## Command

```powershell
.\.venv\Scripts\python.exe scripts\validate_preference_dataset.py
```

## Guardrails

- Modal run: no.
- GPU run: no.
- Training run: no.
- Real preference data read: no.
- Tarball/checkpoint/raw data touched: no.

## Future Work

- Define preference data source policy.
- Add tokenizer and logprob interface integration.
- Add cost-gated training only after model-card and artifact guardrails are reviewed.
