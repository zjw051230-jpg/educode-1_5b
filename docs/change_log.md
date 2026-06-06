# Change Log

## 2026-06-06 - feature/activation-checkpointing-v2

- Technical direction: activation checkpointing / recompute controls v2.
- Modified files:
  - `src/educode/activation_checkpointing.py`
  - `src/educode/memory_knobs.py`
  - `scripts/validate_activation_checkpointing.py`
  - `tests/test_activation_checkpointing.py`
  - `docs/activation_checkpointing_v2.md`
  - `docs/change_log.md`
- Local validation commands:
  - `.\.venv\Scripts\python.exe tests\test_activation_checkpointing.py` (red: missing activation checkpointing module before implementation)
  - `.\.venv\Scripts\python.exe -m py_compile src\educode\activation_checkpointing.py src\educode\memory_knobs.py scripts\validate_activation_checkpointing.py tests\test_activation_checkpointing.py`
  - `.\.venv\Scripts\python.exe scripts\validate_activation_checkpointing.py`
  - `.\.venv\Scripts\python.exe tests\test_activation_checkpointing.py`
  - `git diff --check`
- Validation result: passed; validator blocker count 0 and unit tests ran 4 tests successfully.
- Modal/GPU/training run: no.
- Tarball/checkpoint/raw data committed: no.
- Commit hash: pending.
- Push status: pending.
- Next step: review block boundaries before any integration with training code.
- User cost confirmation needed: no for local branch; yes before GPU profiling.

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
