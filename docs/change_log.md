# Change Log

## 2026-06-06 - feature/dataset-quality-dedup

- Technical direction: dataset quality metrics and near-duplicate skeleton.
- Modified files:
  - `src/educode/data_quality.py`
  - `scripts/analyze_dataset_quality.py`
  - `tests/test_data_quality.py`
  - `docs/dataset_quality_dedup.md`
  - `docs/change_log.md`
- Local validation commands:
  - `.\.venv\Scripts\python.exe tests\test_data_quality.py` (red: missing data_quality module before implementation)
  - `.\.venv\Scripts\python.exe -m py_compile src\educode\data_quality.py scripts\analyze_dataset_quality.py tests\test_data_quality.py`
  - `.\.venv\Scripts\python.exe scripts\analyze_dataset_quality.py`
  - `.\.venv\Scripts\python.exe tests\test_data_quality.py`
  - `git diff --check`
- Validation result: passed; synthetic quality script completed and unit tests ran 3 tests successfully.
- Modal/GPU/training run: no.
- Tarball/checkpoint/raw data committed: no.
- Commit hash: pending.
- Push status: pending.
- Next step: review thresholds before using on sampled real corpus metadata.
- User cost confirmation needed: no, local-only tiny fixtures.

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
