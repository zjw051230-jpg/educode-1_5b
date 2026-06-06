# Change Log

## 2026-06-06 - feature/training-report-generator

- Technical direction: training dashboard and lightweight report generation from imported artifacts.
- Modified files:
  - `scripts/build_training_report.py`
  - `tests/test_training_report_generator.py`
  - `docs/training_report_generator.md`
  - `docs/generated_reports/README.md`
  - `docs/generated_reports/training_report_summary.md`
  - `docs/change_log.md`
- Local validation commands:
  - `.\.venv\Scripts\python.exe tests\test_training_report_generator.py` (red: missing generator before implementation)
  - `.\.venv\Scripts\python.exe -m py_compile scripts\build_training_report.py tests\test_training_report_generator.py`
  - `.\.venv\Scripts\python.exe scripts\build_training_report.py`
  - `.\.venv\Scripts\python.exe tests\test_training_report_generator.py`
  - `git diff --check`
- Validation result: passed; generated report covered 4 imported artifact directories and unit tests ran 2 tests successfully.
- Modal/GPU/training run: no.
- Tarball/checkpoint/raw data committed: no.
- Commit hash: pending.
- Push status: pending.
- Next step: review the generated summary wording before considering a merge.
- User cost confirmation needed: no, local-only reporting.

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
