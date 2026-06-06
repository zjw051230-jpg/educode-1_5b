# Change Log

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

## 2026-06-06 - feature/muon-experimental-optimizer

- Time: 2026-06-06.
- Branch: `feature/muon-experimental-optimizer`.
- Technical direction: AdamW default optimizer registry and guarded Muon experimental path.
- Modified files:
  - `src/educode/optimizers.py`
  - `src/educode/muon.py`
  - `src/educode/config_validator.py`
  - `scripts/validate_optimizer_registry.py`
  - `tests/test_optimizer_registry.py`
  - `tests/test_muon_experimental.py`
  - `docs/muon_optimizer_experimental.md`
  - `docs/change_log.md`
- Local validation commands: recorded in `docs/muon_optimizer_experimental.md`.
- Validation result: passed; validator blocker count 0, 7 unit tests OK.
- Modal/GPU/training run: no.
- Tarball/checkpoint/raw data committed: no.
- Commit hash: recorded in final report after commit.
- Push status: recorded in final report after push.
- Next step: do a formula/source review before any real optimizer comparison.
- User cost confirmation needed: yes, before any AdamW vs Muon training run.
