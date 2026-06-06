# Change Log

## 2026-06-06 - feature/memory-knobs-activation-checkpointing

- Technical direction: activation checkpointing and memory knob controls.
- Modified files:
  - `src/educode/memory.py`
  - `scripts/validate_memory_knobs.py`
  - `tests/test_memory_knobs.py`
  - `docs/memory_knobs_activation_checkpointing.md`
  - `docs/change_log.md`
- Local validation commands:
  - `.\.venv\Scripts\python.exe tests\test_memory_knobs.py` (red: missing memory module before implementation)
  - `.\.venv\Scripts\python.exe -m py_compile src\educode\memory.py scripts\validate_memory_knobs.py tests\test_memory_knobs.py`
  - `.\.venv\Scripts\python.exe scripts\validate_memory_knobs.py`
  - `.\.venv\Scripts\python.exe tests\test_memory_knobs.py`
  - `git diff --check`
- Validation result: passed; validator blocker count 0 and unit tests ran 3 tests successfully.
- Modal/GPU/training run: no.
- Tarball/checkpoint/raw data committed: no.
- Commit hash: pending.
- Push status: pending.
- Next step: review integration with model block boundaries before any profiling run.
- User cost confirmation needed: no for this local branch; yes before future GPU profiling.

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
