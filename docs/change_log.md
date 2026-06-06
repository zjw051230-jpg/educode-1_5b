# Change Log

## 2026-06-06 - feature/quantization-qlora-feasibility

- Technical direction: quantization and QLoRA feasibility guardrails.
- Modified files:
  - `src/educode/quantization.py`
  - `scripts/check_quantization_feasibility.py`
  - `tests/test_quantization_feasibility.py`
  - `docs/quantization_qlora_feasibility.md`
  - `docs/change_log.md`
- Local validation commands:
  - `.\.venv\Scripts\python.exe tests\test_quantization_feasibility.py` (red: missing quantization module before implementation)
  - `.\.venv\Scripts\python.exe -m py_compile src\educode\quantization.py scripts\check_quantization_feasibility.py tests\test_quantization_feasibility.py`
  - `.\.venv\Scripts\python.exe scripts\check_quantization_feasibility.py`
  - `.\.venv\Scripts\python.exe tests\test_quantization_feasibility.py`
  - `git diff --check`
- Validation result: passed; validator blocker count 0 and unit tests ran 4 tests successfully.
- Modal/GPU/training run: no.
- Tarball/checkpoint/raw data committed: no.
- Commit hash: pending.
- Push status: pending.
- Next step: review Modal image and CUDA constraints before any real QLoRA attempt.
- User cost confirmation needed: yes before any future GPU/Modal quantization run; no for this local branch.

## 2026-06-06 - feature/checkpoint-artifact-hygiene

- Technical direction: checkpoint, tarball, raw data, and imported artifact hygiene.
- Modified files:
  - `scripts/check_artifact_hygiene.py`
  - `tests/test_artifact_hygiene.py`
  - `docs/artifact_hygiene.md`
  - `docs/change_log.md`
- Local validation commands:
  - `.\.venv\Scripts\python.exe -m py_compile scripts\check_artifact_hygiene.py tests\test_artifact_hygiene.py`
  - `.\.venv\Scripts\python.exe scripts\check_artifact_hygiene.py`
  - `.\.venv\Scripts\python.exe tests\test_artifact_hygiene.py`
  - `git diff --check`
- Validation result: passed; blocker count 0; unit tests ran 5 tests successfully.
- Modal/GPU/training run: no.
- Tarball/checkpoint/raw data committed: no.
- Commit hash: recorded in final report after commit.
- Push status: recorded in final report after push.
- Next step: use the checker before future result-import commits.
- User cost confirmation needed: no, local-only checker.
