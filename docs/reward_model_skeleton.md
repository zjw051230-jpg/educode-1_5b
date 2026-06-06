# Reward Model / RLHF Skeleton

This branch adds a small reward-model skeleton for future RLHF-style experiments. It does not implement PPO or run any RL training.

## Included

- Reward pair schema.
- Reward head module.
- Pairwise ranking loss.
- Synthetic local validator.
- PPO is documented as future feasibility work only.

## Command

```powershell
.\.venv\Scripts\python.exe scripts\validate_reward_dataset.py
```

## Guardrails

- Modal run: no.
- GPU run: no.
- Training run: no.
- Real reward data read: no.
- Tarball/checkpoint/raw data touched: no.

## Future Work

- Define reward data policy.
- Decide whether reward modeling is needed before DPO/SFT paths.
- Add cost-gated training only after dataset and artifact hygiene review.
