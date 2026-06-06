# Change Log

## 2026-06-06 - feature/reward-model-skeleton

- Technical direction: reward model and RLHF skeleton.
- Modified files:
  - `src/educode/reward_model.py`
  - `scripts/validate_reward_dataset.py`
  - `tests/test_reward_model.py`
  - `docs/reward_model_skeleton.md`
  - `docs/change_log.md`
- Local validation commands:
  - `.\.venv\Scripts\python.exe tests\test_reward_model.py` (red: missing reward model module before implementation)
  - `.\.venv\Scripts\python.exe -m py_compile src\educode\reward_model.py scripts\validate_reward_dataset.py tests\test_reward_model.py`
  - `.\.venv\Scripts\python.exe scripts\validate_reward_dataset.py`
  - `.\.venv\Scripts\python.exe tests\test_reward_model.py`
  - `git diff --check`
- Validation result: passed; validator blocker count 0 and unit tests ran 3 tests successfully.
- Modal/GPU/training run: no.
- Tarball/checkpoint/raw data committed: no.
- Commit hash: pending.
- Push status: pending.
- Next step: review whether reward modeling is needed before any PPO feasibility work.
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
