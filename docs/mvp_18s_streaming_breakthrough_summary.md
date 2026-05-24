# MVP-18.S Streaming Breakthrough Summary

## 1. Purpose

MVP-18.S summarizes the path from the MVP-14/MVP-15 low-RAM fallback runs to the MVP-18 streaming run that restored the intended `batch_size=8` / `gradient_accumulation_steps=4` public16k A800 route.

This is a decision and documentation milestone only. It does not run training, enter A100/A800, train tokenizer/model artifacts, download data, modify training main logic, or commit checkpoints, `raw.jsonl`, processed data, split files, or result tarballs.

## 2. Timeline

| milestone | summary | interpretation |
|---|---|---|
| MVP-14 / MVP-15 | The A800 1000-step and 3000-step public16k runs completed only after falling back to `batch_size=1` / `gradient_accumulation_steps=1`. | These were useful training-systems fallback runs, but not the quality route. |
| MVP-16 | Host/container RAM was identified as the blocker. The old 1000-step precompute path was estimated at `129.024313 GiB` of Python precompute memory, and the old 3000-step path at `387.080954 GiB`. | The issue was host-side batch materialization, not GPU memory capacity. |
| MVP-17 | The streaming batch iterator was implemented and integrated into the public16k 1000/3000-step configs. | The new path avoids full-run token/sample/batch materialization while preserving model-facing batch shape. |
| MVP-18 | The A800 streaming 1000-step public16k run completed with `48GiB` container RAM, `batch_size=8`, and `gradient_accumulation_steps=4`. | The intended larger-batch public16k route is restored for bounded systems validation. |

## 3. Key Technical Breakthrough

The breakthrough is host-side batching, not model architecture.

The model still receives the same batch shape for each microbatch. The training loop still consumes `x` and `y` next-token tensors with the configured `batch_size` and `sequence_length`.

The difference is how the host prepares those batches:

- the old path pre-generated a full token buffer, full overlapping sliding-window sample list, and full run-sized batch list;
- the streaming path reads JSONL records incrementally;
- tokenization happens one document at a time;
- the host keeps only a rolling token buffer;
- next-token blocks and microbatches are yielded lazily;
- the training loop no longer needs a retained `max_steps * gradient_accumulation_steps` Python batch list.

This directly addresses host-RAM pressure. It does not require more GPU memory and does not imply that H200/B200 is needed for the current stage. The MVP-18 evidence supports continuing with A800/A100 40GB-class GPUs, provided the host/container RAM is `48GiB` or `64GiB` and data is prepared before the GPU run.

## 4. MVP-18 Result

| field | value |
|---|---:|
| run_id | `20260524_211036_fineweb_edu_500mb_300m_1000step_public16k_execute` |
| GPU | `A800-SXM4-40GB` |
| container RAM | `48GiB` |
| data_loading_mode | `streaming` |
| batch_size | `8` |
| gradient_accumulation_steps | `4` |
| max_steps | `1000` |
| tokens_seen | `16384000` |
| final_train_loss | `2.877289` |
| final_val_loss | `8.752452` |
| checkpoint_reload_match | `true` |
| post_run_artifact_validation | `passed` |

Additional imported result checks:

- `metrics_rows=1000`;
- `validation_rows=10`;
- `loss_all_finite=true`;
- `val_loss_all_finite=true`;
- `grad_all_finite=true`;
- `checkpoint_path_starts_with_output_dir=true`;
- `import_validation_status=passed`.

The remote checkpoint was about `1.9G`; it was not downloaded and was not committed.

## 5. Comparison to Low-RAM Runs

| field | MVP-14 low-RAM 1000-step | MVP-15 low-RAM 3000-step | MVP-18 streaming 1000-step |
|---|---:|---:|---:|
| data_loading_mode | pre-streaming fallback | pre-streaming fallback | `streaming` |
| container RAM | about `16GiB` | about `16GiB` | `48GiB` |
| batch_size | `1` | `1` | `8` |
| gradient_accumulation_steps | `1` | `1` | `4` |
| tokens_seen | `512000` | `1536000` | `16384000` |
| final_train_loss | `0.213472` | `0.114589` | `2.877289` |
| final_val_loss | `11.513049` | `12.515621` | `8.752452` |
| checkpoint_reload_match | `true` | `true` | `true` |
| post_run_artifact_validation | `passed` | `passed` | `passed` |

The MVP-18 train/validation loss pattern is healthier than the low-RAM fallback runs: train loss did not collapse near zero, and validation loss was lower than the fallback runs. This is still not a model-quality claim, but it is a better bounded systems signal.

MVP-14 and MVP-15 remain useful systems fallback evidence. They validated CUDA bf16 execution, logging, validation metrics, checkpoint reload, and artifact validation. MVP-18 is the new baseline for the next training route because it validates the intended streaming larger-batch path.

## 6. Remaining Caveats

The MVP-18 result still has important boundaries:

- `bounded_prefix_batches_only=true`;
- `scheduler_config_present_but_not_applied=true`;
- the corpus is still the prepared 500MB FineWeb-Edu public slice;
- 1000 steps is still a bounded training-systems run, not model quality proof;
- no 3000-step streaming result exists yet;
- no 2GB or 10GB data-scale run exists yet;
- no downstream evaluation has been run;
- checkpoint artifacts remain remote unless explicitly approved for a separate purpose.

## 7. Conclusion

MVP-17 and MVP-18 successfully removed the host-RAM precompute blocker for the public16k A800 route.

The next stage can choose among:

1. a 3000-step streaming run on the existing 500MB prepared corpus;
2. a 2GB FineWeb-Edu prepared-corpus expansion using local or CPU/data-host preparation;
3. a later 1B 10-step streaming smoke after the 300M streaming path and data logistics are stable.

The recommended hardware class remains A800/A100 40GB with `48GiB` or `64GiB` host/container RAM. H200/B200 is not needed for the immediate next step.
