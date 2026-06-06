# Change Log

## 2026-06-06 - feature/inference-eval-harness

- Branch: `feature/inference-eval-harness`
- Work completed: Added local-only generation helpers, evaluation harness, metadata-only checkpoint summary, smoke script, and unit tests.
- Modified files:
  - `src/educode/generation.py`
  - `src/educode/eval.py`
  - `scripts/run_generation_smoke.py`
  - `tests/test_generation_eval_harness.py`
  - `docs/inference_eval_harness.md`
  - `docs/change_log.md`
- Local validation commands:
  - `.\.venv\Scripts\python.exe -m py_compile src\educode\generation.py src\educode\eval.py scripts\run_generation_smoke.py tests\test_generation_eval_harness.py`
  - `.\.venv\Scripts\python.exe scripts\run_generation_smoke.py`
  - `.\.venv\Scripts\python.exe tests\test_generation_eval_harness.py`
  - `git diff --check`
- Validation result: passed; generation smoke passed and 4 unit tests passed.
- Modal/GPU/training executed: no / no / no.
- Tarball/checkpoint/raw data committed: no / no / no.
- Commit hash: recorded in final task report after commit.
- Push status: pending at authoring time.
- Next step: wire the harness to imported checkpoint metadata only after a separate checkpoint handling plan.
- User cost confirmation needed: yes for any future GPU checkpoint inference; not needed for this local-only branch.
