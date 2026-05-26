# MVP-21.R Import 2GB Streaming Results Plan

## Purpose

This plan describes how to import future A800/A100 2GB streaming result packages after approved GPU execution. It does not run training, enter A800/A100, download data, train tokenizers/models, or commit checkpoints or large corpus artifacts.

## 1000-step Primary Result Package

Expected local package name:

```text
mvp21_a800_2gb_1000step_public16k_streaming_results.tar.gz
```

Import directory:

```text
experiments/a100/fineweb_edu_2gb_300m_1000step_public16k_execute/results_imported_streaming/
```

## 3000-step Optional Result Package

Only import this package if the 3000-step follow-up was explicitly approved and completed after 1000-step success.

Expected local package name:

```text
mvp22_a800_2gb_3000step_public16k_streaming_results.tar.gz
```

Import directory:

```text
experiments/a100/fineweb_edu_2gb_300m_3000step_public16k_execute/results_imported_streaming/
```

## 5000-step Optional Result Package

Only import this package if the 5000-step follow-up was explicitly approved and completed after 3000-step success.

Expected local package name:

```text
mvp23_a800_2gb_5000step_public16k_streaming_results.tar.gz
```

Import directory:

```text
experiments/a100/fineweb_edu_2gb_300m_5000step_public16k_execute/results_imported_streaming/
```

## Expected Files

Each result package should contain only:

- `summary.json`
- `summary.md`
- `metrics.jsonl`
- `validation_metrics.jsonl`
- `run_config.json`
- `run_metadata.json`
- `post_run_artifact_validation_summary.json`

Reject the package if it contains checkpoints, raw corpus files, processed corpus files, split files, prepared data packages, absolute paths, or parent-directory traversal entries.

## Expected Validation Checks

For the 1000-step import, require:

| field | expected value |
|---|---:|
| `max_steps` | `1000` |
| `batch_size` | `8` |
| `gradient_accumulation_steps` | `4` |
| `data_loading_mode` | `streaming` |
| `metrics_rows` | `1000` |
| `validation_rows` | `10` |
| `tokenizer_vocab_size` | `16384` |
| `exact_parameter_count` | `336106496` |
| `checkpoint_reload_match` | `true` |
| `post_run_artifact_validation.passed` | `true` |
| `loss_all_finite` | `true` |
| `val_loss_all_finite` | `true` |
| `grad_all_finite` | `true` |

For the optional 3000-step import, require the same checks except:

| field | expected value |
|---|---:|
| `max_steps` | `3000` |
| `metrics_rows` | `3000` |
| `validation_rows` | `10` |

For the optional 5000-step import, require the same checks except:

| field | expected value |
|---|---:|
| `max_steps` | `5000` |
| `metrics_rows` | `5000` |
| `validation_rows` | `10` |

Recommended additional checks:

- summary train path uses `data/public_corpus/fineweb_edu_sample10bt_2gb/splits/fineweb_edu_2gb.train.jsonl`;
- summary val path uses `data/public_corpus/fineweb_edu_sample10bt_2gb/splits/fineweb_edu_2gb.val.jsonl`;
- checkpoint path starts with the matching 2GB output dir;
- copied files are small review artifacts only.

## Commit Boundary

Allowed after future validation:

- small imported review artifacts;
- import validator;
- import validation summary;
- report documents;
- README and experiment index updates.

Not allowed:

- result tarballs;
- checkpoints;
- raw corpus files;
- processed corpus files;
- split files;
- prepared data packages.
