# Change Log

## 2026-06-07 - feature/run-registry-database

- Technical direction: local run registry metadata store for imported experiment summaries.
- Modified files:
  - `src/educode/run_registry.py`
  - `scripts/build_run_registry.py`
  - `tests/test_run_registry.py`
  - `docs/run_registry_database.md`
  - `docs/change_log.md`
- Local validation commands:
  - `.\.venv\Scripts\python.exe -m py_compile src\educode\run_registry.py scripts\build_run_registry.py tests\test_run_registry.py`
  - `.\.venv\Scripts\python.exe scripts\build_run_registry.py`
  - `.\.venv\Scripts\python.exe tests\test_run_registry.py`
  - `git diff --check`
- Validation result: passed; dry-run registry scan found 12 imported summary records, wrote no output file, and touched no tarballs.
- Modal/GPU/training run: no.
- Tarball/checkpoint/raw data committed: no.
- Commit hash: pending.
- Push status: pending.
- Next step: review whether registry output should be generated as an explicit artifact in a later branch.
- User cost confirmation needed: no, local metadata-only tool.

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
