# MVP-19 A800 Streaming 3000-Step Plan

## Purpose

MVP-19 is the proposed follow-up GPU execution after MVP-18 restored the intended public16k streaming batch path.

This plan is an execution outline only. It does not authorize GPU rental, run training, download data, train a tokenizer/model, change training logic, or commit checkpoints, raw corpus files, processed data, split files, or result tarballs.

## Baseline Code and Data

Use `c2a46e5+` streaming code, including:

- `scripts/streaming_lm_batch_iterator.py`;
- streaming integration in `scripts/run_a100_300m_fineweb_edu_10step_training.py`;
- `data.data_loading_mode = "streaming"` in the public16k execution configs.

Use the prepared FineWeb-Edu 500MB train/validation split package. Do not fetch the 500MB corpus from Hugging Face inside the GPU container.

## Target Config

Config:

```text
configs/a100/fineweb_edu_500mb_300m_3000step_public16k_execute.json
```

Target settings:

| field | value |
|---|---:|
| model scale | 300M public16k |
| tokenizer | `fineweb_edu_public_bpe_16k` |
| tokenizer_vocab_size | `16384` |
| exact_parameter_count | `336106496` |
| max_steps | `3000` |
| eval_interval | `300` |
| checkpoint_interval | `3000` |
| batch_size | `8` |
| gradient_accumulation_steps | `4` |
| sequence_length | `512` |
| data_loading_mode | `streaming` |
| host_ram_efficient_batching | `true` |
| batch_precompute_disabled | `true` |

## Recommended Runtime Resources

Use an A800/A100-class single GPU environment with:

- `A800` or `A100` `40GB` GPU memory class or better;
- `48GiB+` host/container RAM;
- prepared split package uploaded before execution;
- enough disk for logs and one remote checkpoint;
- no requirement to download the checkpoint locally after the run.

MVP-18 validated the 1000-step streaming path with `A800-SXM4-40GB` and `48GiB` container RAM.

## Execution Outline

1. Confirm the repository checkout includes `c2a46e5+` streaming code.
2. Confirm the prepared 500MB public16k train/validation splits exist on the GPU host.
3. Confirm the 3000-step config still uses `data_loading_mode=streaming` and `batch_size=8` / `gradient_accumulation_steps=4`.
4. Run the configured 3000-step execution after explicit approval.
5. Run post-run artifact validation on the GPU host.
6. Package only small review artifacts.
7. Download the small result artifact package for local import and review.
8. Do not download or commit the checkpoint by default.

## Success Criteria

MVP-19 succeeds if the imported result package shows:

| criterion | expected value |
|---|---:|
| runtime_device | `cuda` |
| runtime_dtype | `bf16` |
| max_steps | `3000` |
| batch_size | `8` |
| gradient_accumulation_steps | `4` |
| data_loading_mode | `streaming` |
| metrics_rows | `3000` |
| validation_rows | `10` |
| loss_all_finite | `true` |
| val_loss_all_finite | `true` |
| grad_all_finite | `true` |
| checkpoint_reload_match | `true` |
| checkpoint_path_starts_with_output_dir | `true` |
| post_run_artifact_validation | passed |

The run should also record `host_ram_efficient_batching=true` and `batch_precompute_disabled=true`.

## Artifact Policy

Commit only small review artifacts and documentation after local validation.

Do not commit:

- checkpoint files;
- result tarballs;
- `raw.jsonl`;
- processed corpus files;
- train/validation split files;
- large package files.

## Interpretation Boundary

MVP-19 would remain bounded training-systems evidence. It would validate that the restored streaming 300M public16k path can run for 3000 steps with the intended larger batch settings, but it would not establish model quality or downstream capability.

If MVP-19 succeeds, the next recommended planning step is MVP-20 2GB public-corpus preparation on local or CPU/data-host infrastructure, followed by scheduler/sampling cleanup before any quality-oriented run.
