# MVP-26.F Modal Preflight Path Fix

## Failure Summary

The first Modal `preflight_2gb_1000` attempt reached the dry-run stage after memory inspection passed. Memory inspection confirmed streaming mode and host-RAM-safe batch handling, but dry-run failed before training with:

```text
ValueError: 'configs/a100/fineweb_edu_2gb_300m_1000step_public16k_execute.json' is not in the subpath of '/workspace/educode-1_5b' OR one path is relative and the other is absolute.
```

The failure occurred in `scripts/run_a100_300m_fineweb_edu_10step_training.py` inside `repo_relative_path(config_path)`. No Modal training step ran and no checkpoint was produced.

## Root Cause

The training script accepted `--config` as a raw `Path(args.config)`. When Modal passed a repo-relative config path such as `configs/a100/fineweb_edu_2gb_300m_1000step_public16k_execute.json`, the dry-run summary builder later called `repo_relative_path(config_path)`. The old `repo_relative_path()` called `path.relative_to(PROJECT_ROOT)` directly, which fails when `path` is relative and `PROJECT_ROOT` is absolute.

## Fix

`resolve_repo_path()` and `repo_relative_path()` now both support absolute paths and repo-relative paths:

- `resolve_repo_path()` returns absolute paths unchanged and resolves relative paths under `PROJECT_ROOT`.
- `repo_relative_path()` first resolves relative paths under `PROJECT_ROOT`, then writes repo-relative POSIX paths into summaries.
- `main()` resolves `args.config` before loading config and before passing the path into dry-run/training flows.
- `scripts/modal_a100_streaming_runner.py` now defensively passes absolute config paths to Modal remote commands while keeping `ModeSpec.config_path` repo-relative for receipts and policy readability.

## Local Validation

Commands run locally:

```bash
.venv/Scripts/python.exe -m py_compile scripts/run_a100_300m_fineweb_edu_10step_training.py scripts/modal_a100_streaming_runner.py
.venv/Scripts/python.exe tests/test_repo_path_resolution.py
.venv/Scripts/python.exe scripts/run_a100_300m_fineweb_edu_10step_training.py --config configs/a100/fineweb_edu_2gb_300m_1000step_public16k_execute.json --dry-run
```

`pytest` was checked first with `.venv/Scripts/python.exe -m pytest tests/test_repo_path_resolution.py`, but the current project venv does not have `pytest` installed, so the unittest fallback was used.

Validation results:

- `py_compile` passed for both updated scripts.
- `tests/test_repo_path_resolution.py` passed with `Ran 3 tests in 0.001s` and `OK`.
- Relative-config dry-run succeeded.
- Dry-run summary recorded `config_path=configs/a100/fineweb_edu_2gb_300m_1000step_public16k_execute.json`.
- Dry-run summary recorded `data_loading_mode=streaming`.
- Dry-run summary recorded `exact_parameter_count=336106496`.
- Dry-run summary recorded `no_training=true` and `no_checkpoint=true`.

## Next Modal Preflight Retry Command

After this fix is pushed or otherwise made available to the Modal-cloned repo, retry only the preflight mode:

```bash
modal run scripts/modal_a100_streaming_runner.py --mode preflight_2gb_1000
```

Do not run `train_2gb_1000` until `preflight_2gb_1000` completes successfully and training is explicitly approved.

## Cost Note

- The failed Modal preflight may have incurred short A100/A100-40GB runtime cost before the dry-run failure.
- Retrying `preflight_2gb_1000` will again incur Modal GPU runtime cost.
- The Modal Volume and uploaded `/prepared/fineweb_edu_2gb_prepared_splits.tar.gz` continue to incur storage cost until the volume or files are deleted.
