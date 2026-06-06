# Change Log

## 2026-06-06 - feature/lora-peft-v2

- Technical direction: LoRA / PEFT v2 utilities.
- Modified files:
  - `src/educode/lora.py`
  - `src/educode/peft.py`
  - `scripts/validate_lora_peft_v2.py`
  - `tests/test_lora_peft_v2.py`
  - `docs/lora_peft_v2.md`
  - `docs/change_log.md`
- Local validation commands:
  - `.\.venv\Scripts\python.exe tests\test_lora_peft_v2.py` (red: missing LoRA module before implementation)
  - `.\.venv\Scripts\python.exe -m py_compile src\educode\lora.py src\educode\peft.py scripts\validate_lora_peft_v2.py tests\test_lora_peft_v2.py`
  - `.\.venv\Scripts\python.exe scripts\validate_lora_peft_v2.py`
  - `.\.venv\Scripts\python.exe tests\test_lora_peft_v2.py`
  - `git diff --check`
- Validation result: passed; validator blocker count 0 and unit tests ran 5 tests successfully.
- Modal/GPU/training run: no.
- Tarball/checkpoint/raw data committed: no.
- Commit hash: pending.
- Push status: pending.
- Next step: review adapter checkpoint policy before any training branch.
- User cost confirmation needed: no for local branch; yes before LoRA training.

## 2026-06-06 - branch asset inventory

- Technical direction: branch inventory and review sequencing for experimental assets.
- Modified files:
  - `docs/branch_asset_inventory.md`
  - `docs/change_log.md`
  - `README.md`
- Local validation commands:
  - `git diff --check`
  - `git diff --cached --check`
- Validation result: passed; `git diff --check` reported no whitespace errors.
- Modal/GPU/training run: no.
- Tarball/checkpoint/raw data committed: no.
- Commit hash: pending.
- Push status: pending.
- Next step: review low-risk documentation/reporting branches before model-internal branches.
- User cost confirmation needed: no, documentation-only inventory.

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
