# MVP-6 A100 Training Command Placeholder

## Existing Training Script Candidates
Current repo training-script candidates that may inform a future A100 adaptation:
- `scripts/run_50_step_mixed_domain_bpe_training.py`
- `scripts/run_100_step_mixed_domain_bpe_training.py`
- `scripts/run_50_step_domain_bpe_training.py`
- `scripts/run_100_step_domain_bpe_training.py`
- `scripts/run_50_step_small_real_data_training.py`
- `scripts/run_100_step_small_real_data_training.py`

These scripts are existing bounded training references, but none of them is currently a dedicated FineWeb-Edu public-corpus A100 `10-step` script.

## Placeholder Command
Planned future command placeholder:

```text
.venv/Scripts/python.exe scripts/run_a100_300m_fineweb_edu_10step_training.py --config configs/a100/fineweb_edu_50mb_300m_10step_smoke.json
```

## MVP-6 Scope Note
Important MVP-6 scope rule:
- do not create `scripts/run_a100_300m_fineweb_edu_10step_training.py` in MVP-6
- do not adapt the training loop in MVP-6
- do not run training in MVP-6

## Follow-up Rule
If no existing script can be directly reused for the FineWeb-Edu public-corpus A100 path, then MVP-7 should implement or adapt the actual training script in a later bounded step.
