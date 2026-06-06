# Change Log

## 2026-06-06 - feature/lora-peft-skeleton

- Technical direction: LoRA / PEFT adapter skeleton.
- Modified files:
  - `src/educode/lora.py`
  - `src/educode/peft.py`
  - `scripts/validate_lora_peft.py`
  - `tests/test_lora_peft.py`
  - `docs/lora_peft_skeleton.md`
  - `docs/change_log.md`
- Local validation commands:
  - `.\.venv\Scripts\python.exe tests\test_lora_peft.py` (red: missing LoRA module before implementation)
  - `.\.venv\Scripts\python.exe -m py_compile src\educode\lora.py src\educode\peft.py scripts\validate_lora_peft.py tests\test_lora_peft.py`
  - `.\.venv\Scripts\python.exe scripts\validate_lora_peft.py`
  - `.\.venv\Scripts\python.exe tests\test_lora_peft.py`
  - `git diff --check`
- Validation result: passed; validator blocker count 0 and unit tests ran 4 tests successfully.
- Modal/GPU/training run: no.
- Tarball/checkpoint/raw data committed: no.
- Commit hash: pending.
- Push status: pending.
- Next step: review adapter config integration before any training-mode work.
- User cost confirmation needed: no, local-only skeleton.

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
