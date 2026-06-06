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

## 2026-06-06 - feature/rope-position-encoding-v2

- Time: 2026-06-06.
- Branch: `feature/rope-position-encoding-v2`.
- Technical direction: RoPE helper, position encoding schema, and synthetic passkey fixture prep.
- Modified files:
  - `src/educode/rope.py`
  - `src/educode/position_encoding.py`
  - `src/educode/config_validator.py`
  - `scripts/validate_position_encoding.py`
  - `scripts/generate_passkey_fixture.py`
  - `tests/test_rope_cache.py`
  - `tests/test_position_encoding.py`
  - `docs/rope_position_encoding_v2.md`
  - `docs/change_log.md`
- Local validation commands: recorded in `docs/rope_position_encoding_v2.md`.
- Validation result: passed; validator blocker count 0, passkey fixture generated, 8 unit tests OK.
- Modal/GPU/training run: no.
- Tarball/checkpoint/raw data committed: no.
- Commit hash: recorded in final report after commit.
- Push status: recorded in final report after push.
- Next step: checkpoint compatibility review before wiring RoPE into the model.
- User cost confirmation needed: yes, before any long-context GPU run.
