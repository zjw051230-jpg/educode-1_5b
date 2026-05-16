# A2 A100 Mixed/Domain Preflight Checklist

## 1. Purpose
The purpose of this checklist is to define the required preflight checks before any future A100 mixed/domain controlled run is attempted.

This step does not enter an A100 machine, does not run training, and does not create a new A100 config.

## 2. Required Checks
Before any future A100 mixed/domain run:
- Git state is clean and synced
- A100 machine path is known
- persistent storage path is known
- Python venv path is known
- `torch.cuda.is_available()` is `True`
- tokenizer path exists
- mixed corpus split files exist
- config validates
- no checkpoint is committed
- run summaries are saved after execution
- the A100 machine is stopped or terminated after results are transferred

## 3. Checklist Items
- `git status` shows a clean working tree
- `git branch -vv` shows the intended synced branch
- the A100 machine hostname or access path is recorded
- the persistent storage directory for `experiments/` is recorded
- the correct Python venv is activated
- `python -c "import torch; print(torch.cuda.is_available())"` reports `True`
- `nvidia-smi` shows an `A100`
- `tokenizers/educode_bpe_mixed_domain_8k/tokenizer.json` exists
- `data/real_corpus/splits/mixed_domain_external.train.jsonl` exists
- `data/real_corpus/splits/mixed_domain_external.val.jsonl` exists
- the chosen A100 mixed/domain config validates before any run
- no `.pt`, `.pth`, or `.safetensors` files are staged for commit
- post-run `summary.md`, `summary.json`, and `metrics.jsonl` are retained
- any needed summary artifacts are copied out before machine shutdown
- the A100 machine is stopped or terminated after results are transferred

## 4. Stop Conditions
Stop before any A100 mixed/domain run if any of the following hold:
- git state is dirty
- branch is ahead or behind unexpectedly
- CUDA is unavailable
- GPU is not an `A100`
- tokenizer path is missing
- mixed corpus split files are missing
- config validation fails
- checkpoint artifacts are about to be committed

## 5. Next Step
Recommended next step:
- create the A100 300M mixed/domain config draft and a read-only validation script before any real A100 execution
