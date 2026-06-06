# Change Log

## 2026-06-06 - feature/sequence-packing-data-utilization

- Technical direction: sequence packing and token utilization estimation.
- Modified files:
  - `src/educode/packing.py`
  - `scripts/analyze_token_utilization.py`
  - `tests/test_sequence_packing.py`
  - `docs/sequence_packing_data_utilization.md`
  - `docs/change_log.md`
- Local validation commands:
  - `.\.venv\Scripts\python.exe tests\test_sequence_packing.py` (red: missing packing module before implementation)
  - `.\.venv\Scripts\python.exe -m py_compile src\educode\packing.py scripts\analyze_token_utilization.py tests\test_sequence_packing.py`
  - `.\.venv\Scripts\python.exe scripts\analyze_token_utilization.py`
  - `.\.venv\Scripts\python.exe tests\test_sequence_packing.py`
  - `git diff --check`
- Validation result: passed; synthetic utilization script completed and unit tests ran 3 tests successfully.
- Modal/GPU/training run: no.
- Tarball/checkpoint/raw data committed: no.
- Commit hash: pending.
- Push status: pending.
- Next step: review separator and tokenizer-aware packing assumptions.
- User cost confirmation needed: no, local-only synthetic estimator.

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
