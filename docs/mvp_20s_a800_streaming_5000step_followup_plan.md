# MVP-20.S A800 Streaming 5000-Step Follow-up Plan

## Purpose

MVP-20.S is an optional streaming 5000-step follow-up for the same one-hour A800/A100 session after MVP-19 completes the primary 3000-step run.

This plan is a queue follow-up only. It does not authorize training by itself and does not make model-quality claims.

## Why After 3000-step

The 5000-step run should happen only after the 3000-step run proves the longer streaming path is stable in the current session.

Required prior evidence in the same GPU session:

- 3000-step `success=true`;
- finite train/validation losses;
- finite gradients;
- `checkpoint_reload_match=true`;
- post-run artifact validation passed;
- no OOM or host instability;
- at least `30` minutes remaining.

## Config Path

Use:

```text
configs/a100/fineweb_edu_500mb_300m_5000step_public16k_execute.json
```

Key settings:

| field | value |
|---|---:|
| data_loading_mode | `streaming` |
| batch_size | `8` |
| gradient_accumulation_steps | `4` |
| max_steps | `5000` |
| eval_interval | `500` |
| checkpoint_interval | `5000` |
| sequence_length | `512` |
| tokenizer_vocab_size | `16384` |

## Expected Runtime

MVP-18 1000-step elapsed time was `343.899789` seconds. A linear 5000-step estimate is about `1719.498945` seconds, or about `28.7` minutes.

Plan for `28-35` minutes of training time, plus validation and packaging buffer.

## Success Criteria

The 5000-step follow-up succeeds if the result package shows:

- `success=true`;
- `metrics_rows=5000`;
- `validation_rows=10`;
- `checkpoint_reload_match=true`;
- post-run artifact validation passed;
- `loss_all_finite=true`;
- `val_loss_all_finite=true`;
- `grad_all_finite=true`;
- `data_loading_mode=streaming`;
- `batch_size=8`;
- `gradient_accumulation_steps=4`.

## Caveats

- The corpus is still the prepared 500MB FineWeb-Edu public slice.
- `bounded_prefix_batches_only=true` remains a caveat.
- This is not a model-quality claim.
- No downstream evaluation is included.
- Scheduler/sampling cleanup is still needed before quality-oriented claims.

## Copyback Boundary

Copy back only:

- `summary.json`;
- `summary.md`;
- `metrics.jsonl`;
- `validation_metrics.jsonl`;
- `run_config.json`;
- `run_metadata.json`;
- `post_run_artifact_validation_summary.json`.

Do not copy back checkpoint/raw/processed/split artifacts.

## Next Decision

If both 3000-step and 5000-step streaming runs are stable, the next decision should move to one of:

1. 2GB prepared public-corpus expansion;
2. scheduler/sampling cleanup;
3. a later larger-model smoke only after 300M streaming and data logistics are stable.
