# Change Log

## 2026-06-06 - feature/experiment-planner

- Technical direction: experiment matrix and next-candidate planner.
- Modified files:
  - `scripts/build_experiment_matrix.py`
  - `tests/test_experiment_planner.py`
  - `docs/experiment_matrix.json`
  - `docs/experiment_matrix.md`
  - `docs/next_experiment_candidates.md`
  - `docs/change_log.md`
- Local validation commands:
  - `.\.venv\Scripts\python.exe -m py_compile scripts\build_experiment_matrix.py tests\test_experiment_planner.py`
  - `.\.venv\Scripts\python.exe scripts\build_experiment_matrix.py`
  - `.\.venv\Scripts\python.exe tests\test_experiment_planner.py`
  - `git diff --check`
- Validation result: passed; matrix status `passed`, blocker count 0, 4 unit tests OK.
- Modal/GPU/training run: no.
- Tarball/checkpoint/raw data committed: no.
- Commit hash: recorded in final report after commit.
- Push status: recorded in final report after push.
- Next step: review the matrix before choosing the next GPU-gated experiment.
- User cost confirmation needed: yes, before any candidate marked `planned_requires_gpu`.
