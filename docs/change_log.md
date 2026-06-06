# Change Log

## 2026-06-06 - feature/preference-optimization-skeleton

- Technical direction: DPO / preference optimization skeleton.
- Modified files:
  - `src/educode/preference.py`
  - `src/educode/dpo.py`
  - `scripts/validate_preference_dataset.py`
  - `tests/test_dpo_loss.py`
  - `docs/preference_optimization_skeleton.md`
  - `docs/change_log.md`
- Local validation commands:
  - `.\.venv\Scripts\python.exe tests\test_dpo_loss.py` (red: missing DPO module before implementation)
  - `.\.venv\Scripts\python.exe -m py_compile src\educode\preference.py src\educode\dpo.py scripts\validate_preference_dataset.py tests\test_dpo_loss.py`
  - `.\.venv\Scripts\python.exe scripts\validate_preference_dataset.py`
  - `.\.venv\Scripts\python.exe tests\test_dpo_loss.py`
  - `git diff --check`
- Validation result: passed; validator blocker count 0 and unit tests ran 3 tests successfully.
- Modal/GPU/training run: no.
- Tarball/checkpoint/raw data committed: no.
- Commit hash: pending.
- Push status: pending.
- Next step: review preference data policy before any real data ingestion.
- User cost confirmation needed: no for this local skeleton; yes before future GPU training.

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
