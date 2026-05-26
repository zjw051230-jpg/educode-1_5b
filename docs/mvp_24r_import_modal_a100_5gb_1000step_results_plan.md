# MVP-24.R Import Modal A100 5GB 1000-Step Results Plan

## Purpose

Define the local import plan for a future Modal A100 5GB 1000-step result package.

This plan does not run Modal, train, extract a result package, or validate real training results in this step.

## Expected Result Package

```text
mvp24_a100_5gb_1000step_public16k_streaming_results.tar.gz
```

The package should be copied to the project root only after the future Modal training run completes. The package itself must remain uncommitted.

## Import Directory

Future import target:

```text
experiments/a100/fineweb_edu_5gb_300m_1000step_public16k_execute/results_imported_modal_streaming/
```

## Expected Files

The result package should contain exactly the small training result artifacts needed for review:

- `summary.json`
- `summary.md`
- `metrics.jsonl`
- `validation_metrics.jsonl`
- `run_config.json`
- `run_metadata.json`
- `post_run_artifact_validation_summary.json`

It must not include checkpoints, raw corpus files, processed corpus directories, split JSONL files, prepared package tarballs, or result package tarballs nested inside itself.

## Validator To Create Later

Create this validator during the import step:

```text
scripts/validate_mvp24_modal_a100_5gb_1000step_imported_results.py
```

The validator should read the imported files and verify the fields below.

## Expected Checks

The future import validator should require:

| field | expected value |
|---|---:|
| `success` | `true` |
| `max_steps` | `1000` |
| `batch_size` | `8` |
| `gradient_accumulation_steps` | `4` |
| `data_loading_mode` | `streaming` |
| `sampling_policy` | `shuffle_buffer` |
| `scheduler_policy` | `constant` |
| `bounded_prefix_batches_only` | `false` |
| `metrics_rows` | `1000` |
| `validation_rows` | `10` |
| `checkpoint_reload_match` | `true` |
| `post_run_artifact_validation.passed` | `true` |

Additional recommended checks:

- `tokenizer_vocab_size=16384`
- `exact_parameter_count=336106496`
- `loss_all_finite=true`
- `val_loss_all_finite=true`
- `grad_all_finite=true`
- `checkpoint_path_starts_with_output_dir=true`
- no imported checkpoint file exists under the import directory
- no imported `raw.jsonl`, `processed/`, or `splits/` path exists under the import directory

## Import Boundary

The future import commit may include small imported JSON/Markdown/JSONL result artifacts and validator output summaries. It must not include checkpoints or corpus data.
