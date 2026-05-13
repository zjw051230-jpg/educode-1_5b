# A100 Handoff Checklist

- first-session command checklist: `docs/t8_7_a100_first_session_commands.md`
- machine provider / instance type
- GPU type
- VRAM
- driver version
- CUDA shown by `nvidia-smi`
- Python version
- `which python` before and after `.venv` activation
- torch version
- tokenizers version
- git version
- checked-out commit hash
- repo clean
- `python scripts/check_tokenizer_env.py` passed
- `python scripts/inspect_a100_100m_config.py` passed
- install / network / environment problems noted
- session stopped cleanly within the planned `30-60 minutes`
