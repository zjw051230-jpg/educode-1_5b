# T8.6 A100 Provider Selection Record

## 1. Purpose
The purpose of T8.6 is to record the chosen A100 access path so later T8.7 / T8.x execution work can use a fixed first target.

## 2. Selected First Option
Selected first option:
- `selected_gpu`: single `A100 80GB`
- `estimated_price`: about `3 RMB/hour`
- `provider_type`: personal rental / private A100 provider
- `multi_gpu_available`: yes
- `first_use_multi_gpu`: no
- `expected first session`: `30-60 minutes`
- `first session purpose`:
  - environment check
  - repo clone/sync
  - config validation
  - 100M forward/loss smoke preparation

## 3. Why A100 80GB
Reasons for selecting A100 80GB first:
- `80GB` provides more memory headroom than `40GB`
- it is better suited for `100M` / `300M` smoke work
- it is closer to later `1.5B` preflight needs
- it reduces early OOM risk
- the price difference is acceptable for short smoke sessions

## 4. Why Not Multi-GPU Yet
Reasons for not using multi-GPU first:
- the current EduCode pipeline is single-GPU
- `DDP` / `FSDP` is not implemented yet
- multi-GPU rental would not help until distributed training support exists
- the first priority is validating the single-A100 path
- a distributed plan should be considered only after single-GPU `100M` / `300M` smoke passes

## 5. Security / Repo Rules
Security and repo rules:
- do not upload private data
- do not put tokens or secrets into files
- clone the repo cleanly
- keep `experiments/` ignored
- do not commit checkpoints
- do not leave the machine running idle

## 6. First A100 Session Goal
The first A100 session should do only the following:
- run `nvidia-smi`
- run Python / `torch` / CUDA checks
- clone or sync the repo
- check out the expected commit
- install minimal dependencies if needed
- run `scripts/inspect_a100_100m_config.py`
- only then decide whether to implement or run forward/loss smoke

## 7. Stop Conditions
Execution must stop if any of the following is true:
- the GPU is not an A100
- VRAM is lower than expected
- CUDA is unavailable
- `torch.cuda.is_available()` is false
- the repo cannot sync
- config validation fails
- the provider environment is unstable

## 8. Next Step
Recommended next step:
- T8.7 A100 first-session command checklist
