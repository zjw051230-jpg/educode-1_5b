# MVP-20.S.R Import Streaming 5000-Step Results Plan

## Purpose

This plan describes how to import and validate the optional MVP-20.S 5000-step streaming result package if it is produced after a successful MVP-19 3000-step primary run.

This import plan does not run training, enter A100/A800, download data, train tokenizer/model artifacts, or commit checkpoints, raw corpus files, processed data, split files, or result tarballs.

## Result Package

Expected local package name:

```text
mvp20s_a800_5000step_public16k_streaming_results.tar.gz
```

The tarball remains local-only and must not be committed.

## Import Directory

Import target:

```text
experiments/a100/fineweb_edu_500mb_300m_5000step_public16k_execute/results_imported_streaming/
```

## Expected Files

The package should contain only:

- `summary.json`;
- `summary.md`;
- `metrics.jsonl`;
- `validation_metrics.jsonl`;
- `run_config.json`;
- `run_metadata.json`;
- `post_run_artifact_validation_summary.json`.

Reject the package if it contains checkpoint files, raw corpus files, processed corpus files, split files, prepared data packages, absolute paths, or parent-directory traversal entries.

## Validator to Create Later

Create this validator during the future import step:

```text
scripts/validate_mvp20s_a800_streaming_imported_results.py
```

The validator should write:

```text
experiments/a100/fineweb_edu_500mb_300m_5000step_public16k_execute/results_imported_streaming/import_validation_summary.json
```

## Expected Checks

The validator should require:

| field | expected value |
|---|---:|
| `max_steps` | `5000` |
| `batch_size` | `8` |
| `grad_accum` / `gradient_accumulation_steps` | `4` |
| `data_loading_mode` | `streaming` |
| `metrics_rows` | `5000` |
| `checkpoint_reload_match` | `true` |
| `post_run_artifact_validation.passed` | `true` |

Recommended additional checks:

- actual `metrics.jsonl` rows equal `5000`;
- actual `validation_metrics.jsonl` rows equal summary `validation_rows`;
- `validation_rows=10` expected;
- `tokenizer_vocab_size=16384`;
- `exact_parameter_count=336106496`;
- `loss_all_finite=true`;
- `val_loss_all_finite=true`;
- `grad_all_finite=true`;
- `checkpoint_path_starts_with_output_dir=true`.

## Commit Boundary

Allowed after future validation:

- small imported review artifacts;
- import validator;
- import validation summary;
- report documents;
- README and experiment index updates.

Not allowed:

- `mvp20s_a800_5000step_public16k_streaming_results.tar.gz`;
- checkpoints;
- raw corpus files;
- processed corpus files;
- split files;
- prepared data packages.
