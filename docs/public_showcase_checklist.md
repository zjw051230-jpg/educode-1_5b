# Public Showcase Checklist

## 1. Safe Claims
Safe claims include:
- CS336-inspired modular LLM training system
- implemented dense Transformer toy training pipeline
- validated on toy data
- RTX 4060 Ti CUDA smoke and toy training
- checkpoint / generation / logging pipeline working

## 2. Claims to Avoid
Do not claim:
- trained a production LLM
- trained a 1.5B model
- trained on a real dataset
- achieved meaningful generation quality
- completed alignment / RLHF
- implemented MoE
- used A100/B200 already

## 3. Files Safe to Show
- `README.md`
- `docs/resume_project_report.md`
- `docs/resume_bullets.md`
- `docs/quickstart.md`
- `scripts/run_resume_demo.py`
- `src/educode` modules

## 4. Files / Artifacts Not for Git
- checkpoint `.pt` files
- generated `experiments` run directories
- raw datasets
- API keys
- local caches

## 5. Recommended GitHub Visibility
- Private is safest while iterating.
- Public is reasonable only after checking no large files, no secrets, and no private data.
- If public, keep scope honest and avoid claiming real pretraining.
