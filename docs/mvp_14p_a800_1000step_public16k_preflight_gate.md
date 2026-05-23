# MVP-14.P A800 300M 1000-step Public16k Preflight Gate

## Purpose

MVP-14.P prepares the next A800/A100 `300M` `1000-step` public16k execution by cleaning up the logging and path caveats recorded in MVP-10.

This is a preflight and logging cleanup gate only. It does not rent a GPU, enter A100/A800, run real training, train a tokenizer, train a model, or write checkpoints.

## Why This Gate Exists

MVP-10 recorded several caveats from the imported A800 runs:

- `validation_metrics.jsonl` was not written as a standalone artifact;
- MVP-9 `checkpoint_path` pointed into the `10step_execute` directory;
- `run_id` still contained a `10step_smoke` phrase during a later bounded run;
- scheduler fields were present in config/reporting but no scheduler was actually applied;
- output paths needed stricter config-to-artifact validation.

MVP-13.1 proved the public `16k` tokenizer can drive local model forward/loss. MVP-14.P ensures the next real GPU run will produce cleaner review artifacts.

## Logging Cleanup Completed

The A100 training script now supports:

- `run_id` derived from the current `config.run.run_name` instead of a hardcoded `10step` phrase;
- checkpoint save directory locked to the current `output_dir/checkpoints`;
- standalone `validation_metrics.jsonl` written at each evaluation step;
- `summary.json` validation row count tied to the actual `validation_metrics.jsonl` row count;
- honest scheduler logging with `scheduler_applied=false` and `scheduler_config_present_but_not_applied=true` when no scheduler is applied;
- post-run artifact validation helper for summary, metrics, validation metrics, run config, run metadata, checkpoint path, and checkpoint reload status.

## Config Review

Config reviewed:

```text
configs/a100/fineweb_edu_500mb_300m_1000step_public16k_execute.json
```

Key fields:

| field | value |
|---|---|
| run_name | `fineweb_edu_500mb_300m_1000step_public16k_execute` |
| output_dir | `experiments/a100/fineweb_edu_500mb_300m_1000step_public16k_execute` |
| tokenizer_path | `tokenizers/fineweb_edu_public_bpe_16k/tokenizer.json` |
| vocab_size | `16384` |
| train_path | `data/public_corpus/fineweb_edu_sample10bt_500mb/splits/fineweb_edu_500mb.train.jsonl` |
| val_path | `data/public_corpus/fineweb_edu_sample10bt_500mb/splits/fineweb_edu_500mb.val.jsonl` |
| max_steps | `1000` |
| eval_interval | `100` |
| checkpoint_interval | `1000` |
| no_training | `false` |

The hardware target is kept as `a100_cuda` because the current config validator accepts that canonical target. The `gpu` field still records the intended A100/A800 execution class.

## Dry-run Result

Command:

```text
.venv/Scripts/python.exe scripts/run_a100_300m_fineweb_edu_10step_training.py --config configs/a100/fineweb_edu_500mb_300m_1000step_public16k_execute.json --dry-run
```

Dry-run summary:

```text
experiments/a100/fineweb_edu_500mb_300m_1000step_public16k_execute/dry_run_summary.json
```

Observed values:

| field | value |
|---|---:|
| tokenizer_vocab_size | `16384` |
| exact_parameter_count | `336106496` |
| model_materialized_locally | `true` |
| memory_limited_local_dry_run | `false` |
| core_model_feature_parity | `true` |
| no_training | `true` |

The dry-run did not run forward training, backward, optimizer steps, checkpoint writes, or a training loop.

## Readiness Check Result

Command:

```text
.venv/Scripts/python.exe scripts/check_a100_execution_readiness.py --config configs/a100/fineweb_edu_500mb_300m_1000step_public16k_execute.json
```

Readiness summary:

```text
experiments/a100/fineweb_edu_500mb_300m_1000step_public16k_execute/execution_readiness_summary.json
```

Observed values:

| field | value |
|---|---:|
| ready_for_a100_execution | `true` |
| ready_for_a800_execution | `true` |
| blockers | `0` |
| caveats | `0` |
| tokenizer_vocab_size | `16384` |
| exact_parameter_count | `336106496` |
| max_steps | `1000` |
| eval_interval | `100` |
| checkpoint_interval | `1000` |

## Remaining Caveats

This preflight does not convert the next GPU run into a model-quality result.

The future run should still be described as:

- bounded training-systems validation;
- public16k tokenizer integration validation;
- not full pretraining;
- not a model-quality claim;
- not a long-run stability guarantee.

## Execution Command

A future approved execution should use:

```text
.venv/Scripts/python.exe scripts/run_a100_300m_fineweb_edu_10step_training.py --config configs/a100/fineweb_edu_500mb_300m_1000step_public16k_execute.json
```

Do not add `--dry-run` for the real execution.

## Stop Conditions

Stop before or during execution if any of the following occurs:

- config validation fails;
- tokenizer vocab does not equal `16384`;
- train or validation split is missing;
- output directory contains `10step`;
- run name contains `10step`;
- checkpoint path would resolve outside the current output directory;
- loss, validation loss, or gradients become non-finite;
- out-of-memory occurs;
- step count would exceed `1000`;
- `validation_metrics.jsonl` is not produced;
- checkpoint reload verification fails.

## What MVP-14.P Does Not Do

MVP-14.P does not:

- rent GPU capacity;
- enter A100/A800;
- run real training;
- run the `1000-step` execution;
- train a tokenizer;
- train a model;
- save checkpoints;
- download data;
- modify core model architecture;
- advance D20/E-line work;
- claim model quality.

## Next Step

Next step: MVP-14 A800 `300M` `1000-step` execution using the reviewed public16k config, followed by the post-run artifact validator and execution receipt.
