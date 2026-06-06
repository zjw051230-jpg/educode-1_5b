# Change Log

## 2026-06-06 - feature/moe-routing-prep

- Technical direction: MoE routing and expert skeleton, guarded away from default dense training.
- Modified files:
  - `src/educode/moe_layers.py`
  - `src/educode/config_validator.py`
  - `scripts/validate_moe_routing.py`
  - `tests/test_moe_routing.py`
  - `docs/moe_routing_prep.md`
  - `docs/change_log.md`
- Local validation commands:
  - `.\.venv\Scripts\python.exe -m py_compile src\educode\moe_layers.py src\educode\config_validator.py scripts\validate_moe_routing.py tests\test_moe_routing.py`
  - `.\.venv\Scripts\python.exe scripts\validate_moe_routing.py`
  - `.\.venv\Scripts\python.exe tests\test_moe_routing.py`
  - `git diff --check`
- Validation result: passed; validator blocker count 0, router synthetic checks passed, 5 unit tests OK.
- Modal/GPU/training run: no.
- Tarball/checkpoint/raw data committed: no.
- Commit hash: recorded in final report after commit.
- Push status: recorded in final report after push.
- Next step: design real MoE dispatch/load-balancing before enabling training.
- User cost confirmation needed: yes, before any future MoE GPU run.
