# Change Log

## 2026-06-06 - feature/distributed-launch-feasibility

- Technical direction: FSDP / ZeRO / Megatron feasibility docs and protected launch command planner.
- Modified files:
  - `scripts/plan_distributed_launch.py`
  - `scripts/check_fsdp_zero_feasibility.py`
  - `tests/test_distributed_launch_planner.py`
  - `docs/fsdp_zero_megatron_feasibility.md`
  - `docs/distributed_launch_planner.md`
  - `docs/change_log.md`
- Local validation commands:
  - `.\.venv\Scripts\python.exe tests\test_distributed_launch_planner.py` (red: missing launch planner before implementation)
  - `.\.venv\Scripts\python.exe -m py_compile scripts\plan_distributed_launch.py scripts\check_fsdp_zero_feasibility.py tests\test_distributed_launch_planner.py`
  - `.\.venv\Scripts\python.exe scripts\plan_distributed_launch.py`
  - `.\.venv\Scripts\python.exe scripts\check_fsdp_zero_feasibility.py`
  - `.\.venv\Scripts\python.exe tests\test_distributed_launch_planner.py`
  - `git diff --check`
- Validation result: passed; launch planner scripts completed and unit tests ran 4 tests successfully.
- Modal/GPU/training run: no.
- Tarball/checkpoint/raw data committed: no.
- Commit hash: pending.
- Push status: pending.
- Next step: review command templates before any multi-GPU execution plan.
- User cost confirmation needed: no for local planner; yes before future distributed launch.

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
