# Change Log

## 2026-06-06 - feature/config-schema-hardening

- Technical direction: enhanced config schema hardening for future local and GPU-gated experiments.
- Modified files:
  - `src/educode/config_schema.py`
  - `scripts/validate_config_schema_hardening.py`
  - `tests/test_config_schema_hardening.py`
  - `docs/config_schema_hardening.md`
  - `docs/change_log.md`
- Local validation commands:
  - `.\.venv\Scripts\python.exe -m py_compile src\educode\config_schema.py scripts\validate_config_schema_hardening.py tests\test_config_schema_hardening.py`
  - `.\.venv\Scripts\python.exe scripts\validate_config_schema_hardening.py`
  - `.\.venv\Scripts\python.exe tests\test_config_schema_hardening.py`
  - `git diff --check`
- Validation result: passed; 4 existing configs remained valid, 8 bad config classes rejected, 4 unit tests OK.
- Modal/GPU/training run: no.
- Tarball/checkpoint/raw data committed: no.
- Commit hash: recorded in final report after commit.
- Push status: recorded in final report after push.
- Next step: consider wiring this checker into future readiness scripts without weakening existing gates.
- User cost confirmation needed: no for local schema checks; yes before any future GPU-gated config.
