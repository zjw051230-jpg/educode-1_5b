# MVP-6 A100 Transfer Checklist

## Files Required on A100
Required files for a future A100 FineWeb-Edu smoke session:
- config: `configs/a100/fineweb_edu_50mb_300m_10step_smoke.json`
- tokenizer: `tokenizers/educode_bpe_mixed_domain_8k/tokenizer.json`
- tokenizer artifact directory: `tokenizers/educode_bpe_mixed_domain_8k/`
- train split local artifact: `data/public_corpus/fineweb_edu_sample10bt_50mb/splits/fineweb_edu_50mb.train.jsonl`
- val split local artifact: `data/public_corpus/fineweb_edu_sample10bt_50mb/splits/fineweb_edu_50mb.val.jsonl`
- preflight script: `scripts/preflight_a100_fineweb_edu_smoke.py`
- training script placeholder path: `scripts/run_a100_300m_fineweb_edu_10step_training.py`

## Commands to Verify Environment
Recommended future environment checks:

```text
nvidia-smi
python --version
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available()); print(torch.cuda.device_count()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'no cuda'); print(torch.version.cuda)"
python -c "import tokenizers; print(tokenizers.__version__)"
git status --short --branch
git rev-parse HEAD
```

## Commands to Verify Data
Recommended future data checks:

```text
python -c "from pathlib import Path; print(Path('data/public_corpus/fineweb_edu_sample10bt_50mb/splits/fineweb_edu_50mb.train.jsonl').exists())"
python -c "from pathlib import Path; print(Path('data/public_corpus/fineweb_edu_sample10bt_50mb/splits/fineweb_edu_50mb.val.jsonl').exists())"
python -c "from pathlib import Path; print(Path('tokenizers/educode_bpe_mixed_domain_8k/tokenizer.json').exists())"
```

## Commands to Run Preflight
Future preflight command:

```text
python scripts/preflight_a100_fineweb_edu_smoke.py --config configs/a100/fineweb_edu_50mb_300m_10step_smoke.json
```

## Where Outputs Go
Planned output root:
- `experiments/a100/fineweb_edu_50mb_300m_10step_smoke/`

Expected small artifacts to review first:
- `preflight_summary.json`
- `metrics.jsonl`
- small logs
- compact summary JSON / markdown if added later

## What to Copy Back
Copy back only the small reviewed artifacts by default:
- `metrics.jsonl`
- `summary.json`
- small logs
- preflight summary

Do not copy back huge checkpoints unless explicitly needed for a later reviewed step.

## Terminate GPU Reminder
After logs and summary artifacts are transferred back:
- stop or terminate the A100 machine
- do not leave the GPU instance running idle
- record shutdown time and any incomplete transfer notes
