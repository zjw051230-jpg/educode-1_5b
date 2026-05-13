# T8.4 A100 Execution Runbook

## 1. Purpose
The purpose of T8.4 is to prepare an execution runbook for a future real A100 machine so that environment checks, repo sync, config validation, and forward/loss smoke can be completed quickly once A100 access exists.

This step does not enter an A100 machine, does not run training, and does not execute the smoke path.

## 2. Preconditions
Preconditions for future execution:
- an `A100 40GB` or `A100 80GB` machine is available
- SSH or terminal access is available
- Git is installed
- Python is available
- the CUDA driver is visible through `nvidia-smi`
- the repo is accessible
- the target commit is known

## 3. Repository Setup Commands
Future A100 repository setup command template:

```text
git clone https://github.com/zjw051230-jpg/educode-1_5b.git
cd educode-1_5b
git status
git log --oneline -n 5
```

If the repo already exists on the target machine, use `git pull`, GitHub Desktop, or another approved sync path instead of recloning.
Do not overwrite local uncommitted changes.

## 4. Python Environment Setup
Recommended future A100 Python environment steps:

```text
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
```

PyTorch installation should remain a reviewed placeholder step:
- use the official PyTorch CUDA wheel that matches the real A100 environment
- record `torch.__version__`
- record `torch.version.cuda`
- do not install random packages without review

Expected dependencies:
- `torch`
- `tokenizers`
- `transformers`
- `datasets`

## 5. Environment Verification Commands
Future A100 environment verification commands:

```text
nvidia-smi
python --version
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'no cuda')"
python -c "import tokenizers; print(tokenizers.__version__)"
```

## 6. Project Verification Commands
Future project verification commands:

```text
python scripts/check_tokenizer_env.py
python scripts/inspect_a100_100m_config.py
```

If the future A100 forward/loss smoke script has been implemented by that time, then run:

```text
python scripts/inspect_a100_100m_forward_loss_smoke.py
```

That script is not implemented yet in the current repo state.

## 7. Expected A100 Smoke Output
Future T8.5 / later A100 smoke reporting should record:
- GPU name
- total VRAM
- torch version
- CUDA version
- config path
- model parameter count
- input shape
- logits shape
- loss value
- loss finite
- memory allocated
- memory reserved
- elapsed time

## 8. Stop Conditions
Execution must stop if any of the following is true:
- `nvidia-smi` is unavailable
- the GPU is not an A100
- `torch.cuda.is_available()` is `False`
- config validation fails
- tokenizer artifact is missing
- the repo is not on the expected commit
- the working tree is dirty
- OOM occurs on forward before trying the planned batch/context reductions

## 9. Artifact Policy
Artifact policy for the A100 line:
- `experiments/` stays ignored
- checkpoints are not committed
- raw logs are not committed by default
- summarized reports may be copied into docs after review
- no secrets may appear in logs

## 10. Next Step
Recommended next step:
- T8.5 implement the A100 forward/loss smoke script once real A100 access is available.
