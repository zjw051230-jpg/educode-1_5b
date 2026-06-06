# Change Log

## 2026-06-06 - feature/model-card-reproducibility

- Technical direction: model card template, reproducibility checklist, and local environment capture.
- Modified files:
  - `docs/model_card_template.md`
  - `docs/reproducibility_checklist.md`
  - `docs/reproducibility_environment_summary.example.json`
  - `scripts/capture_environment_summary.py`
  - `tests/test_reproducibility_docs.py`
  - `docs/change_log.md`
- Local validation commands:
  - `.\.venv\Scripts\python.exe tests\test_reproducibility_docs.py` (red: missing script/docs before implementation)
  - `.\.venv\Scripts\python.exe -m py_compile scripts\capture_environment_summary.py tests\test_reproducibility_docs.py`
  - `.\.venv\Scripts\python.exe scripts\capture_environment_summary.py --output $env:TEMP\educode_reproducibility_environment_summary.json`
  - `.\.venv\Scripts\python.exe tests\test_reproducibility_docs.py`
  - `git diff --check`
- Validation result: passed; environment capture script ran locally and doc checks ran 2 tests successfully.
- Modal/GPU/training run: no.
- Tarball/checkpoint/raw data committed: no.
- Commit hash: pending.
- Push status: pending.
- Next step: fill the template only with evidence-backed claims for each reviewed run.
- User cost confirmation needed: no, local-only docs and environment capture.

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
