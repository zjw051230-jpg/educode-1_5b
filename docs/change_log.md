# Change Log

## 2026-06-06 - feature/loss-metric-diagnostics

- Technical direction: loss curve and metric anomaly diagnostics for imported artifacts.
- Modified files:
  - `src/educode/diagnostics.py`
  - `scripts/analyze_loss_diagnostics.py`
  - `tests/test_loss_diagnostics.py`
  - `docs/loss_metric_diagnostics.md`
  - `docs/change_log.md`
- Local validation commands:
  - `.\.venv\Scripts\python.exe tests\test_loss_diagnostics.py` (red: missing diagnostics module before implementation)
  - `.\.venv\Scripts\python.exe -m py_compile src\educode\diagnostics.py scripts\analyze_loss_diagnostics.py tests\test_loss_diagnostics.py`
  - `.\.venv\Scripts\python.exe scripts\analyze_loss_diagnostics.py`
  - `.\.venv\Scripts\python.exe tests\test_loss_diagnostics.py`
  - `git diff --check`
- Validation result: passed; diagnostics script completed and unit tests ran 3 tests successfully.
- Modal/GPU/training run: no.
- Tarball/checkpoint/raw data committed: no.
- Commit hash: pending.
- Push status: pending.
- Next step: review diagnostics thresholds before merge.
- User cost confirmation needed: no, local-only diagnostics.

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
