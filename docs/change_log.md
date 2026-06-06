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

## 2026-06-06 - feature/inference-kv-cache-harness-v2

- Time: 2026-06-06.
- Branch: `feature/inference-kv-cache-harness-v2`.
- Technical direction: local CPU inference, sampling, KV cache, PagedAttention skeleton, speculative interface, and eval harness.
- Modified files:
  - `src/educode/generation.py`
  - `src/educode/sampling.py`
  - `src/educode/kv_cache.py`
  - `src/educode/inference.py`
  - `src/educode/speculative.py`
  - `src/educode/paged_cache.py`
  - `src/educode/eval.py`
  - `scripts/run_generation_smoke.py`
  - `scripts/validate_inference_harness.py`
  - `tests/test_generation.py`
  - `tests/test_sampling.py`
  - `tests/test_kv_cache.py`
  - `tests/test_speculative_interface.py`
  - `tests/test_eval_harness.py`
  - `docs/inference_kv_cache_harness_v2.md`
  - `docs/change_log.md`
- Local validation commands: recorded in `docs/inference_kv_cache_harness_v2.md`.
- Validation result: passed; smoke passed, validator blocker count 0, 12 unit tests OK.
- Modal/GPU/training run: no.
- Tarball/checkpoint/raw data committed: no.
- Commit hash: recorded in final report after commit.
- Push status: recorded in final report after push.
- Next step: only connect to real checkpoints after a separate checkpoint-loading gate.
- User cost confirmation needed: yes, before any GPU checkpoint inference or latency measurement.
