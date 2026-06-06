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

## 2026-06-06 - feature/moe-routing-skeleton-v2

- Time: 2026-06-06.
- Branch: `feature/moe-routing-skeleton-v2`.
- Technical direction: MoE router, losses, capacity helper, dispatch/combine skeleton, and disabled-by-default config guard.
- Modified files:
  - `src/educode/moe_routing.py`
  - `src/educode/moe_layers.py`
  - `src/educode/config_validator.py`
  - `scripts/validate_moe_routing.py`
  - `tests/test_moe_routing.py`
  - `tests/test_moe_losses.py`
  - `tests/test_moe_config.py`
  - `docs/moe_routing_skeleton_v2.md`
  - `docs/change_log.md`
- Local validation commands: recorded in `docs/moe_routing_skeleton_v2.md`.
- Validation result: passed; validator blocker count 0, 9 unit tests OK.
- Modal/GPU/training run: no.
- Tarball/checkpoint/raw data committed: no.
- Commit hash: recorded in final report after commit.
- Push status: recorded in final report after push.
- Next step: review architecture boundaries before any MoE model integration.
- User cost confirmation needed: yes, before any MoE GPU run.
