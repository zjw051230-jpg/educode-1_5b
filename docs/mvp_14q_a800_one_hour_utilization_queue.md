# MVP-14.Q A800 One-Hour Utilization Queue

## Purpose

MVP-14.Q prepares a one-hour A800/A100 utilization queue so the next rental session does not waste the remaining minimum billing window after the primary `300M` public16k `1000-step` run.

This is preparation only. It does not rent GPU capacity, enter A100/A800, run real training, train a tokenizer, train a model, download data, or write checkpoints.

## Why Queue Extra Work

Some A800/A100 providers bill in one-hour minimum blocks. The reviewed `1000-step` run is the required first execution, but it may leave usable time in the same rental window. A pre-reviewed follow-up queue keeps the session disciplined: continue only if the primary run succeeds and stop otherwise.

## Primary Run

MVP-14 public16k `1000-step` bounded run:

| field | value |
|---|---|
| config | `configs/a100/fineweb_edu_500mb_300m_1000step_public16k_execute.json` |
| output_dir | `experiments/a100/fineweb_edu_500mb_300m_1000step_public16k_execute` |
| tokenizer | `tokenizers/fineweb_edu_public_bpe_16k/tokenizer.json` |
| tokenizer_vocab_size | `16384` |
| max_steps | `1000` |
| eval_interval | `100` |
| checkpoint_interval | `1000` |

Command:

```text
.venv/Scripts/python.exe scripts/run_a100_300m_fineweb_edu_10step_training.py --config configs/a100/fineweb_edu_500mb_300m_1000step_public16k_execute.json
```

## Follow-up Run

MVP-15 public16k `3000-step` bounded follow-up:

| field | value |
|---|---|
| config | `configs/a100/fineweb_edu_500mb_300m_3000step_public16k_execute.json` |
| output_dir | `experiments/a100/fineweb_edu_500mb_300m_3000step_public16k_execute` |
| tokenizer | `tokenizers/fineweb_edu_public_bpe_16k/tokenizer.json` |
| tokenizer_vocab_size | `16384` |
| max_steps | `3000` |
| eval_interval | `300` |
| checkpoint_interval | `3000` |

Command:

```text
.venv/Scripts/python.exe scripts/run_a100_300m_fineweb_edu_10step_training.py --config configs/a100/fineweb_edu_500mb_300m_3000step_public16k_execute.json
```

## Recommended Rental

- Recommended minimum: `1×A800/A100 40GB` for `1 hour`.
- Safer rental: `2 hours` if provider setup, environment restore, upload/download, or dependency checks are slow.
- Do not start the follow-up run if copy-back, validation, or shutdown time would be squeezed.

## Execution Policy

Always run the `1000-step` config first.

Run the `3000-step` follow-up only if all conditions are true:

- `1000-step` `summary.success = true`;
- `checkpoint_reload_match = true`;
- no non-finite train loss, validation loss, or gradient signal;
- no OOM occurred;
- at least `20–25` minutes remain in the rental window after primary validation and copy-back planning.

Do not run the `3000-step` config if the `1000-step` run fails, produces non-finite values, OOMs, misses validation artifacts, or fails checkpoint reload verification.

Do not run a `5000-step` or larger queue item in this rental unless the user explicitly authorizes it.

## What to Copy Back

Copy back these review artifacts for each completed run:

- `summary.json`
- `summary.md`
- `metrics.jsonl`
- `validation_metrics.jsonl`
- `run_config.json`
- `run_metadata.json`
- `post_run_artifact_validation_summary.json`

## What Not to Copy Back

Do not copy back or commit:

- checkpoints;
- raw corpus files;
- processed corpus files;
- split corpus files;
- result bundles containing checkpoints.

## Stop Conditions

Stop the queue before or during execution if any of the following occurs:

- config validation fails;
- tokenizer vocab does not equal `16384`;
- train, validation, or tokenizer path is missing;
- output directory contains stale `10step` or `100step` identity;
- checkpoint path would resolve outside the current run output directory;
- loss, validation loss, or gradients become non-finite;
- out-of-memory occurs;
- primary `1000-step` summary success is not true;
- checkpoint reload verification fails;
- `validation_metrics.jsonl` is missing;
- less than `20–25` minutes remain for the follow-up run;
- the user has not explicitly authorized any run beyond the prepared `1000-step` primary and conditional `3000-step` follow-up.

## Post-run Validation

Use the general public16k artifact validator for either completed run:

```text
.venv/Scripts/python.exe scripts/validate_a800_public16k_run_artifacts.py --output-dir experiments/a100/fineweb_edu_500mb_300m_1000step_public16k_execute
```

or:

```text
.venv/Scripts/python.exe scripts/validate_a800_public16k_run_artifacts.py --output-dir experiments/a100/fineweb_edu_500mb_300m_3000step_public16k_execute
```

The older `scripts/validate_a800_1000step_public16k_run_artifacts.py` remains a 1000-step-specific compatibility helper. New queue reviews should use the general public16k validator.
