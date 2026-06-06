# Change Log

## 2026-06-06 - feature/qlora-quantization-v2

- Technical direction: QLoRA and quantization feasibility v2.
- Modified files:
  - `src/educode/quantization.py`
  - `scripts/check_quantization_feasibility_v2.py`
  - `scripts/validate_qlora_config.py`
  - `tests/test_quantization_v2.py`
  - `docs/qlora_quantization_v2.md`
  - `docs/dora_loftq_feasibility.md`
  - `docs/change_log.md`
- Local validation commands:
  - `.\.venv\Scripts\python.exe tests\test_quantization_v2.py` (red: missing quantization module before implementation)
  - `.\.venv\Scripts\python.exe -m py_compile src\educode\quantization.py scripts\check_quantization_feasibility_v2.py scripts\validate_qlora_config.py tests\test_quantization_v2.py`
  - `.\.venv\Scripts\python.exe scripts\check_quantization_feasibility_v2.py`
  - `.\.venv\Scripts\python.exe scripts\validate_qlora_config.py`
  - `.\.venv\Scripts\python.exe tests\test_quantization_v2.py`
  - `git diff --check`
- Validation result: passed; feasibility scripts completed and unit tests ran 4 tests successfully.
- Modal/GPU/training run: no.
- Tarball/checkpoint/raw data committed: no.
- Commit hash: pending.
- Push status: pending.
- Next step: review real 4-bit load risks before any GPU branch.
- User cost confirmation needed: no for local branch; yes before QLoRA training.

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
