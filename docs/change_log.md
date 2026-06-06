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

## 2026-06-06 - feature/attention-backend-abstraction-v2

- Time: 2026-06-06.
- Branch: `feature/attention-backend-abstraction-v2`.
- Technical direction: SDPA/naive/FlashAttention2 guarded attention backend abstraction with GQA helper.
- Modified files:
  - `src/educode/attention_backends.py`
  - `src/educode/attention_utils.py`
  - `src/educode/tiny_model.py`
  - `scripts/check_attention_backend_availability.py`
  - `tests/test_attention_backends.py`
  - `tests/test_attention_gqa.py`
  - `docs/attention_backend_abstraction_v2.md`
  - `docs/change_log.md`
- Local validation commands: recorded in `docs/attention_backend_abstraction_v2.md`.
- Validation result: passed; availability checker blocker count 0, 8 unit tests OK.
- Modal/GPU/training run: no.
- Tarball/checkpoint/raw data committed: no.
- Commit hash: recorded in final report after commit.
- Push status: recorded in final report after push.
- Next step: review carefully before merging because `tiny_model.py` attention call path changes.
- User cost confirmation needed: yes, before any backend profiling run.
