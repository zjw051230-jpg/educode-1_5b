# MVP-19.R Import Streaming 3000-step Results Plan

## Purpose

This plan describes how to import and validate the small result package after a future MVP-19 A800/A100 streaming 3000-step run.

This plan does not run training, enter A100/A800, download data, train tokenizer/model artifacts, modify training main logic, or commit checkpoints, `raw.jsonl`, processed data, split files, or result tarballs.

## Expected Result Package

Expected local package name:

```text
mvp19_a800_3000step_public16k_streaming_results.tar.gz
```

The package must contain only small review artifacts. It must not contain checkpoint files, raw corpus files, processed corpus files, split files, or prepared data packages.

## Import Directory

Import target:

```text
experiments/a100/fineweb_edu_500mb_300m_3000step_public16k_execute/results_imported_streaming/
```

The import step should create this directory if needed and copy only approved small files into it.

## Expected Files

The result package should contain:

- `summary.json`;
- `summary.md`;
- `metrics.jsonl`;
- `validation_metrics.jsonl`;
- `run_config.json`;
- `run_metadata.json`;
- `post_run_artifact_validation_summary.json`.

## Safety Inspection Before Extraction

Before extracting, inspect the archive member list and reject the package if it contains any of these:

- checkpoint files such as `*.pt`, `*.pth`, or `*.ckpt`;
- `raw.jsonl`;
- processed corpus directories;
- split files;
- prepared data packages;
- absolute paths;
- parent-directory traversal paths.

## Validator to Create

Create this local validator during MVP-19.R:

```text
scripts/validate_mvp19_a800_streaming_imported_results.py
```

It should validate the imported directory and write:

```text
experiments/a100/fineweb_edu_500mb_300m_3000step_public16k_execute/results_imported_streaming/import_validation_summary.json
```

## Expected Checks

The validator should require:

| field | expected value |
|---|---:|
| `max_steps` | `3000` |
| `batch_size` | `8` |
| `gradient_accumulation_steps` | `4` |
| `data_loading_mode` | `streaming` |
| `metrics_rows` | `3000` |
| `validation_rows` | `10` |
| `checkpoint_reload_match` | `true` |
| `post_run_artifact_validation.passed` | `true` |

Additional recommended checks:

- `runtime_device=cuda`;
- `runtime_dtype=bf16`;
- `tokenizer_vocab_size=16384`;
- `exact_parameter_count=336106496`;
- `loss_all_finite=true`;
- `val_loss_all_finite=true`;
- `grad_all_finite=true`;
- actual `metrics.jsonl` row count equals `3000`;
- actual `validation_metrics.jsonl` row count equals `10`;
- `checkpoint_path_starts_with_output_dir=true`;
- standalone post-run artifact validation reports success or zero blockers.

## Import Report Documents

After validation, MVP-19.R should create a concise report recording:

- run identity;
- GPU and host/container RAM;
- streaming settings;
- loss and validation metrics;
- checkpoint reload status;
- post-run artifact validation status;
- import validation status;
- artifact boundary confirming no checkpoint/raw/processed/splits/result tarball was committed.

## Commit Boundary

Allowed for local commit after validation:

- small imported review artifacts;
- the import validator;
- import validation summary;
- MVP-19.R report documents;
- README and experiment index updates.

Not allowed for commit:

- `mvp19_a800_3000step_public16k_streaming_results.tar.gz`;
- checkpoints;
- raw corpus files;
- processed corpus files;
- split files;
- prepared data packages.
