# T8.2 A100 Environment Preflight Checklist

## 1. Purpose
The purpose of T8.2 is to define the environment checks that should be completed before any A100 machine is used for the EduCode-1.5B A100 line.

This step does not enter an A100 machine, does not run training, and does not change the A100 config draft.

## 2. Current Local Baseline
Current local baseline:
- local GPU: `RTX 2080 Ti`
- `torch` works locally
- `tokenizers` works locally
- A100 config draft exists
- A100 config has not been run yet

## 3. Required A100 Environment
Required checks before any future A100 smoke step:
- `nvidia-smi` is available
- GPU name contains `A100`
- total VRAM is `40GB` or `80GB`
- Python is `3.11` or the chosen approved version
- `torch` is installed
- `torch.cuda.is_available()` is `True`
- `torch.version.cuda` is recorded
- `tokenizers` is installed
- the repo is cloned
- the correct commit is checked out
- the working tree is clean

## 4. Required Commands
Commands that should be run later on the actual A100 machine:
- `git status`
- `git log --oneline -n 5`
- `python --version`
- `python -c "import torch; print(torch.__version__); print(torch.cuda.is_available()); print(torch.version.cuda)"`
- `nvidia-smi`
- `python scripts/inspect_a100_100m_config.py`

## 5. Storage / Artifact Rules
Storage and artifact rules for the future A100 line:
- `experiments/` must remain Git-ignored
- checkpoints must not be committed
- metrics and summaries may be copied into docs only after review
- large data must not be committed

## 6. Failure Handling
Failure handling rules:
- no CUDA -> stop
- GPU not A100 -> stop or record that a different hardware path is being used
- `torch` unavailable -> an explicit install decision is required before any run attempt
- config validation failure -> fix the config path before training
- OOM during a future smoke step -> reduce batch size, context length, or model size before training

## 7. What T8.2 Does Not Do
This step does not:
- rent cloud GPUs
- run A100 training
- download data
- modify the config
- install dependencies

## 8. Next Step
Recommended next step:
- T8.3 A100 100M forward/loss smoke plan or script, only after an A100 environment is actually available.
