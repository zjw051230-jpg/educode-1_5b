# T8.7 A100 First-Session Command Checklist

## 1. Purpose
The purpose of T8.7 is to prepare an exact first-session command checklist for the selected single `A100 80GB` path so the first real machine login can verify the environment quickly and stop cleanly before any training work begins.

This step does not enter the A100 machine, does not run forward/loss smoke, and does not run training.

## 2. Session Goal
The first A100 session should do only the following:
- confirm the machine is really an `A100`
- confirm VRAM is acceptable for the selected path
- confirm Python and Git are available
- clone or sync the repo cleanly
- create and activate a local `.venv`
- install only the minimal reviewed dependencies
- run the tokenizer environment check
- run the A100 100M config inspection script
- stop and report back before any forward/loss smoke or training step

## 3. Machine Check
Run these commands first and record their outputs:

```text
nvidia-smi
python --version
which python
git --version
```

Stop immediately if the GPU is not an `A100`, if VRAM is lower than expected, or if Python / Git is missing.

## 4. Repo Setup
If the repo is not present on the machine yet, use:

```text
git clone https://github.com/zjw051230-jpg/educode-1_5b.git
cd educode-1_5b
git status
git log --oneline -n 5
git checkout <expected_commit>
git status
```

If the repo already exists on the machine, sync it only through an approved clean-path workflow and do not overwrite local uncommitted changes.

## 5. Python Environment
Create and activate a dedicated virtual environment inside the repo:

```text
python -m venv .venv
source .venv/bin/activate
python --version
which python
python -m pip install --upgrade pip setuptools wheel
```

After activation, `which python` should point to the repo-local `.venv` path.

## 6. Dependency Check
Install only the reviewed minimum dependencies for this first session:

```text
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install tokenizers transformers datasets
python -c "import torch; print(torch.__version__); print(torch.version.cuda); print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'no cuda')"
python -c "import tokenizers; print(tokenizers.__version__)"
```

Record the reported `torch` version, CUDA version, CUDA availability, device name, and `tokenizers` version.

## 7. Project Checks
From the repo root with the virtual environment active, run:

```text
python scripts/check_tokenizer_env.py
python scripts/inspect_a100_100m_config.py
```

Both commands must pass before deciding whether the later forward/loss smoke step is ready.

## 8. Stop Conditions
Execution must stop if any of the following is true:
- `nvidia-smi` is unavailable
- the GPU is not an `A100`
- VRAM is below the expected target for the selected session
- Python or Git is missing
- the repo cannot be cloned or synced cleanly
- the repo is not on the expected commit
- the working tree is dirty before project checks begin
- the virtual environment is not the active Python path
- `torch.cuda.is_available()` is `False`
- dependency installation fails
- `python scripts/check_tokenizer_env.py` fails
- `python scripts/inspect_a100_100m_config.py` fails
- the provider environment is unstable or should be shut down to avoid idle cost

## 9. What Not To Run Yet
Do not run any of the following during the first session:
- no training scripts
- no checkpoint-producing runs
- no profiling runs
- no multi-GPU / `DDP` / `FSDP` work
- no data upload or secret placement
- no long idle session
- no `scripts/inspect_a100_100m_forward_loss_smoke.py` run unless that future step is explicitly implemented and approved later

## 10. Information To Report Back
Report the following after the first session:
- provider / instance type
- GPU model and VRAM from `nvidia-smi`
- driver version and CUDA shown by `nvidia-smi`
- `python --version`
- `which python` before and after `.venv` activation
- `git --version`
- checked-out commit hash
- whether the repo was clean
- `torch` version
- `torch.version.cuda`
- `torch.cuda.is_available()` result
- `tokenizers` version
- result of `python scripts/check_tokenizer_env.py`
- result of `python scripts/inspect_a100_100m_config.py`
- any install, network, or environment problems
- whether the session stopped cleanly within the planned `30-60 minutes`

## 11. Next Step
Recommended next step after a clean T8.7 session:
- review the reported outputs and decide whether to implement or run the future A100 `100M` forward/loss smoke step.
