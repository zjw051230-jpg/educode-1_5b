# Change Log

## 2026-06-06 - feature/attention-backend-prep

- Branch: `feature/attention-backend-prep`
- Work completed: Added a local attention backend abstraction with SDPA default, CPU-only naive causal attention, and a FlashAttention availability guard.
- Modified files:
  - `src/educode/attention_backends.py`
  - `src/educode/tiny_model.py`
  - `scripts/check_attention_backend_availability.py`
  - `tests/test_attention_backends.py`
  - `docs/attention_backend_prep.md`
  - `docs/change_log.md`
- Local validation commands:
  - `.\.venv\Scripts\python.exe -m py_compile src\educode\attention_backends.py src\educode\tiny_model.py scripts\check_attention_backend_availability.py`
  - `.\.venv\Scripts\python.exe scripts\check_attention_backend_availability.py`
  - `.\.venv\Scripts\python.exe tests\test_attention_backends.py`
  - `git diff --check`
- Validation result: passed; availability status `passed`, blocker count `0`, and 5 unit tests passed.
- Modal/GPU/training executed: no / no / no.
- Tarball/checkpoint/raw data committed: no / no / no.
- Commit hash: recorded in final task report after commit.
- Push status: pending at authoring time.
- Next step: decide whether to merge backend abstraction before planning naive/FlashAttention profiling.
- User cost confirmation needed: yes for any future Modal/GPU backend profiling run; not needed for this local-only branch.
