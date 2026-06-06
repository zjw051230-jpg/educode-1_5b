# Change Log

## 2026-06-07 - feature/eval-benchmark-harness

- Technical direction: local synthetic evaluation benchmark harness.
- Modified files:
  - `src/educode/eval_benchmarks.py`
  - `src/educode/eval_metrics.py`
  - `scripts/run_eval_benchmark_smoke.py`
  - `scripts/validate_eval_benchmark_harness.py`
  - `tests/test_eval_benchmark_harness.py`
  - `docs/eval_benchmark_harness.md`
  - `docs/change_log.md`
- Local validation commands:
  - `.\.venv\Scripts\python.exe tests\test_eval_benchmark_harness.py` (red: missing eval benchmark modules before implementation)
  - `.\.venv\Scripts\python.exe -m py_compile src\educode\eval_benchmarks.py src\educode\eval_metrics.py scripts\run_eval_benchmark_smoke.py scripts\validate_eval_benchmark_harness.py tests\test_eval_benchmark_harness.py`
  - `.\.venv\Scripts\python.exe scripts\run_eval_benchmark_smoke.py`
  - `.\.venv\Scripts\python.exe scripts\validate_eval_benchmark_harness.py`
  - `.\.venv\Scripts\python.exe tests\test_eval_benchmark_harness.py`
  - `git diff --check`
- Validation result: passed; smoke/validator scripts completed and unit tests ran 4 tests successfully.
- Modal/GPU/training run: no.
- Tarball/checkpoint/raw data committed: no.
- Commit hash: pending.
- Push status: pending.
- Next step: review before any real checkpoint evaluation.
- User cost confirmation needed: no for local harness; yes before real checkpoint inference.

## 2026-06-07 - branch asset inventory v2

- Technical direction: update branch inventory with second-batch data-driven branches, risk tiers, review order, GPU gates, and claims boundaries.
- Modified files:
  - `docs/branch_asset_inventory.md`
  - `docs/change_log.md`
- Local validation commands:
  - `git diff --check`
  - `git diff --cached --check`
- Validation result: passed; `git diff --check` reported no whitespace errors.
- Modal/GPU/training run: no.
- Tarball/checkpoint/raw data committed: no.
- Commit hash: pending.
- Push status: pending.
- Next step: review low-risk docs/reporting/data utility branches before model-internal or distributed branches.
- User cost confirmation needed: no, documentation-only inventory update.

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
