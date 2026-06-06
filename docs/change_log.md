# Change Log

## 2026-06-06 - feature/distributed-config-memory-estimator

- Technical direction: distributed config schema, gradient accumulation accounting, and rough memory estimator.
- Modified files:
  - `src/educode/distributed_config.py`
  - `src/educode/grad_accum.py`
  - `src/educode/memory_estimator.py`
  - `scripts/validate_distributed_config.py`
  - `scripts/estimate_training_memory.py`
  - `tests/test_distributed_config.py`
  - `tests/test_grad_accum_accounting.py`
  - `tests/test_memory_estimator.py`
  - `docs/distributed_config_memory_estimator.md`
  - `docs/change_log.md`
- Local validation commands:
  - `.\.venv\Scripts\python.exe tests\test_distributed_config.py; .\.venv\Scripts\python.exe tests\test_grad_accum_accounting.py; .\.venv\Scripts\python.exe tests\test_memory_estimator.py` (red: missing modules before implementation)
  - `.\.venv\Scripts\python.exe -m py_compile src\educode\distributed_config.py src\educode\grad_accum.py src\educode\memory_estimator.py scripts\validate_distributed_config.py scripts\estimate_training_memory.py tests\test_distributed_config.py tests\test_grad_accum_accounting.py tests\test_memory_estimator.py`
  - `.\.venv\Scripts\python.exe scripts\validate_distributed_config.py`
  - `.\.venv\Scripts\python.exe scripts\estimate_training_memory.py`
  - `.\.venv\Scripts\python.exe tests\test_distributed_config.py`
  - `.\.venv\Scripts\python.exe tests\test_grad_accum_accounting.py`
  - `.\.venv\Scripts\python.exe tests\test_memory_estimator.py`
  - `git diff --check`
- Validation result: passed; validator blocker count 0, estimator script completed, and unit tests ran 7 tests successfully.
- Modal/GPU/training run: no.
- Tarball/checkpoint/raw data committed: no.
- Commit hash: pending.
- Push status: pending.
- Next step: review estimator assumptions before any distributed run planning.
- User cost confirmation needed: no for this local branch; yes before future distributed GPU execution.

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
