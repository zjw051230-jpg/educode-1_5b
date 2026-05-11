# Quickstart

## 1. Requirements
Validated environment:
- Windows 11
- Python 3.11.9
- PyTorch 2.5.1+cu121
- NVIDIA RTX 4060 Ti 16GB
- CUDA available
- Git
- GitHub Desktop used for push/sync

Notes:
- A100/B200 are not required for the current demo
- no model download is required
- no dataset download is required
- no new package installation is required if `torch` is already available on the machine

## 2. Clone / Open Repository
Use your own repository URL:

```text
git clone <your-repo-url>
cd educode-1_5b
```

## 3. Run Demo
Primary demo command:

```text
python scripts/run_resume_demo.py
```

Fallback command:

```text
python scripts/run_50_step_toy_training.py
```

## 4. Expected Demo Behavior
The demo:
- runs bounded 50-step toy training
- creates an ignored run directory under `experiments/windows_cuda/`
- writes `metrics.jsonl`
- writes `generation_samples.jsonl`
- writes `summary.md`
- saves a checkpoint locally but does not track it in Git
- is expected to finish quickly on an RTX 4060 Ti

## 5. Expected Output
Expected high-level outcome:
- `max_steps = 50`
- loss remains finite
- `checkpoint reload match = True`
- generation preview is printed
- `experiments/` remains ignored by Git

## 6. Important Scope Note
Important scope notes:
- toy data only
- tiny model only
- not full LLM pretraining
- not 1.5B training
- generation quality is not meaningful yet
