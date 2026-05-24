# MVP-19 A800 Streaming 3000-Step Plan

## Purpose

MVP-19 is the proposed bounded follow-up GPU run after MVP-18 restored the public16k streaming route.

This document is a plan draft only. It does not authorize GPU rental, run training, enter A100/A800, download data, train tokenizer/model artifacts, modify training main logic, or commit checkpoints, `raw.jsonl`, processed data, split files, or result tarballs.

## Baseline Requirements

Use `c2a46e5+` streaming code, including:

- `scripts/streaming_lm_batch_iterator.py`;
- streaming integration in `scripts/run_a100_300m_fineweb_edu_10step_training.py`;
- public16k configs with `data_loading_mode=streaming`;
- `host_ram_efficient_batching=true`;
- `batch_precompute_disabled=true`.

Use the prepared FineWeb-Edu 500MB train/validation splits. Do not fetch the 500MB corpus from Hugging Face inside the GPU container.

## Target Configuration

Config:

```text
configs/a100/fineweb_edu_500mb_300m_3000step_public16k_execute.json
```

Target settings:

| field | value |
|---|---:|
| model scale | 300M public16k |
| exact_parameter_count | `336106496` |
| tokenizer | `fineweb_edu_public_bpe_16k` |
| tokenizer_vocab_size | `16384` |
| batch_size | `8` |
| grad_accum / gradient_accumulation_steps | `4` |
| max_steps | `3000` |
| eval_interval | `300` |
| checkpoint_interval | `3000` |
| sequence_length | `512` |
| data_loading_mode | `streaming` |

## Recommended Resources

Use:

- A800/A100 40GB-class GPU;
- `48GiB+` container RAM, with `64GiB` acceptable if available;
- prepared 500MB split package already present on the GPU host;
- sufficient remote disk for logs and one checkpoint;
- no local checkpoint download by default.

MVP-18 validated the 1000-step version on `A800-SXM4-40GB` with `48GiB` container RAM.

## Execution Outline

1. Confirm the GPU checkout includes `c2a46e5+` streaming code.
2. Confirm prepared 500MB train/validation splits are already present on the GPU host.
3. Confirm the 3000-step config keeps `batch_size=8`, `gradient_accumulation_steps=4`, `max_steps=3000`, `eval_interval=300`, and `checkpoint_interval=3000`.
4. Execute only after explicit approval.
5. Run post-run artifact validation on the GPU host.
6. Package only small review artifacts.
7. Download only the small result package for local import and validation.
8. Do not download or commit checkpoint/raw/processed/split artifacts.

## Success Criteria

MVP-19 succeeds if the imported result package shows:

| criterion | expected value |
|---|---:|
| runtime_device | `cuda` |
| runtime_dtype | `bf16` |
| data_loading_mode | `streaming` |
| batch_size | `8` |
| gradient_accumulation_steps | `4` |
| max_steps | `3000` |
| metrics_rows | `3000` |
| validation_rows | `10` |
| loss_all_finite | `true` |
| val_loss_all_finite | `true` |
| grad_all_finite | `true` |
| checkpoint_reload_match | `true` |
| checkpoint_path_starts_with_output_dir | `true` |
| post_run_artifact_validation | passed |

The result should also preserve `host_ram_efficient_batching=true` and `batch_precompute_disabled=true`.

## Non-Commit Boundary

Do not commit:

- checkpoints;
- result tarballs;
- `raw.jsonl`;
- processed corpus files;
- train/validation split files;
- prepared split packages.

## Interpretation Boundary

MVP-19 would remain bounded training-systems evidence. It would validate longer streaming stability for the 300M public16k path, not final model quality.

If MVP-19 succeeds, the next route should be MVP-20 2GB prepared-corpus work on local/CPU infrastructure, plus scheduler/sampling cleanup before any quality-oriented claim.
