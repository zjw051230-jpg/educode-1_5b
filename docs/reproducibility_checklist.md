# Reproducibility Checklist

## 1. Config
- config path: `configs/windows/smoke_cuda_10m.json`
- config is JSON parseable
- config is validated before runs
- `run_config.json` snapshot is written per run

## 2. Code Version
- git commit hash should be recorded
- git branch should be recorded
- working tree should be clean before demo runs

## 3. Environment
Record and verify:
- Python version
- torch version
- CUDA availability
- GPU name
- GPU memory

## 4. Run Artifacts
Each run should generate:
- `run_metadata.json`
- `run_config.json`
- `metrics.jsonl`
- `generation_samples.jsonl`
- `checkpoints_manifest.json`
- `summary.md`

## 5. What Is Not Tracked
- checkpoints
- generated run directories
- logs
- raw datasets
- model weights

## 6. Current Known Reproducible Demo
- script: `scripts/run_resume_demo.py`
- underlying script: `scripts/run_50_step_toy_training.py`
- max_steps: `50`
- hardware: `RTX 4060 Ti`
- best documented result: `first_loss 9.188724 -> final_loss 4.837882`
- checkpoint reload match: `True`
