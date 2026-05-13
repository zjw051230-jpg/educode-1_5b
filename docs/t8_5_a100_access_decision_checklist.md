# T8.5 A100 Access Decision Checklist

## 1. Purpose
The purpose of T8.5 is to define the checklist for choosing a suitable cloud or hosted A100 environment for later 100M forward/loss smoke and 10-step training smoke work.

This step does not rent GPUs, does not enter an A100 environment, and does not run training.

## 2. Required Hardware
Required hardware baseline:
- `A100 40GB` minimum
- `A100 80GB` preferred
- CUDA visible through `nvidia-smi`
- enough disk for the repo, virtual environment, run artifacts, and checkpoints

## 3. Provider Decision Fields
The future provider decision should record:
- provider
- instance type
- GPU type
- VRAM
- hourly price
- disk size
- region
- SSH access
- persistent storage yes/no
- image type
- Python version
- CUDA / PyTorch compatibility

## 4. Minimum Environment
Minimum environment requirements:
- Git
- Python
- pip / venv
- CUDA driver
- PyTorch CUDA wheel
- `tokenizers`
- `transformers`
- `datasets`

## 5. Cost Guardrails
Cost guardrails for the first A100 access path:
- start with forward/loss smoke only
- then run a 10-step training smoke only
- stop before any long training
- record elapsed time and estimated cost
- do not leave the instance running idle

## 6. Data / Artifact Transfer
Data and artifact transfer rules:
- clone the repo from GitHub
- do not upload private data
- `experiments/` remains ignored
- checkpoints are not committed
- only reviewed summaries may be copied into docs

## 7. First A100 Run Ladder
Planned first A100 run ladder:
- A100 environment check
- config validation
- 100M forward/loss smoke
- 10-step training smoke
- profiling report
- then decide whether to move to 300M

## 8. Stop Conditions
Execution must stop if any of the following is true:
- the GPU is not an A100
- CUDA is unavailable
- `torch` cannot use CUDA
- the repo is not clean
- config validation fails
- the smoke step OOMs before the planned batch/context reductions are tried

## 9. Next Step
Recommended next step:
- T8.6 A100 provider selection record, after the user chooses a provider or instance.
