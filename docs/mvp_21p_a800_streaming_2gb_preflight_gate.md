# MVP-21.P A800 Streaming 2GB Preflight Gate

## Purpose

MVP-21.P prepares A800/A100 execution configs and readiness artifacts for bounded 300M public16k streaming training on the locally prepared FineWeb-Edu 2GB corpus.

This step does not run model training, enter A100/A800, train a tokenizer, save checkpoints, download data, or make model-architecture changes.

## Why 2GB After 500MB

The 500MB FineWeb-Edu path validated public16k tokenizer integration, A800/A100 streaming batch formation, dry-run materialization, and bounded 1000/3000/5000-step logistics. The 2GB prepared corpus is the next data-scale step because it keeps the same model/tokenizer/training-system surface while testing larger prepared data logistics.

The 2GB step remains a training-systems milestone, not a model-quality claim.

## Input Corpus

| field | value |
|---|---:|
| dataset | `HuggingFaceFW/fineweb-edu` |
| dataset_config | `sample-10BT` |
| raw record_count | `449802` |
| raw total_text_bytes | `2147485975` |
| raw duplicate_text_hash_count | `434` |
| processed_count | `449367` |
| train_count | `426857` |
| val_count | `22510` |
| dropped_duplicate_count | `435` |
| total_text_bytes | `2145535856` |
| train_text_bytes | `2036973656` |
| val_text_bytes | `108562200` |

Train/val paths:

- `data/public_corpus/fineweb_edu_sample10bt_2gb/splits/fineweb_edu_2gb.train.jsonl`
- `data/public_corpus/fineweb_edu_sample10bt_2gb/splits/fineweb_edu_2gb.val.jsonl`

## Prepared Package

GPU host should receive:

```text
C:/Users/01/fineweb_edu_2gb_prepared_splits.tar.gz
```

Package size is `847344882` bytes. GPU host should not fetch Hugging Face data for this 2GB slice.

## Configs Created

| config | max_steps | eval_interval | checkpoint_interval | output_dir |
|---|---:|---:|---:|---|
| `configs/a100/fineweb_edu_2gb_300m_1000step_public16k_execute.json` | `1000` | `100` | `1000` | `experiments/a100/fineweb_edu_2gb_300m_1000step_public16k_execute` |
| `configs/a100/fineweb_edu_2gb_300m_3000step_public16k_execute.json` | `3000` | `300` | `3000` | `experiments/a100/fineweb_edu_2gb_300m_3000step_public16k_execute` |

Both configs keep:

- `data_loading_mode=streaming`
- `tokenizer_vocab_size=16384`
- `model_vocab_size=16384`
- `batch_size=8`
- `gradient_accumulation_steps=4`
- `sequence_length=512`
- `training.no_training=false`
- `checkpoint.no_commit_checkpoints=true`

## Memory Inspection Results

| config | current_precomputed_estimated_python_memory_gib | streaming_estimated_batch_tensor_memory_mib | streaming_expected_host_ram_safe | reduction_factor_estimate | sample policy |
|---|---:|---:|---|---:|---|
| 1000-step | `129.024313` | `0.062` | `true` | `919106.768` | max `100` records per split; does not read entire corpus |
| 3000-step | `387.080954` | `0.062` | `true` | `2757377.394` | max `100` records per split; does not read entire corpus |

The memory inspection confirms streaming mode avoids full-run host-side batch precomputation.

## Dry-run Results

| config | parameter_count | tokenizer_vocab_size | data_loading_mode | no_training | output_dir correct |
|---|---:|---:|---|---|---|
| 1000-step | `336106496` | `16384` | `streaming` | `true` | yes |
| 3000-step | `336106496` | `16384` | `streaming` | `true` | yes |

Dry-runs validated tokenizer loading, bounded streaming batch formation, local model materialization, exact parameter counting, and declared/core feature parity. They did not run forward, backward, optimizer step, checkpoint save, or training.

## Readiness Results

| config | ready_for_a800_execution | ready_for_a100_execution | blockers | caveats |
|---|---|---|---:|---:|
| 1000-step | `true` | `true` | `0` | `0` |
| 3000-step | `true` | `true` | `0` | `0` |

Readiness checks confirmed train/val/tokenizer paths exist, `data_loading_mode=streaming`, vocab sizes match `16384`, eval interval matches max steps, checkpoint interval equals max steps, checkpoint save path resolves inside output dir, and output dir basename matches run name.

## GPU Logistics

- Upload `C:/Users/01/fineweb_edu_2gb_prepared_splits.tar.gz` to the GPU host before execution.
- Extract it into `data/public_corpus/fineweb_edu_sample10bt_2gb/` on the GPU host.
- Do not fetch Hugging Face data on the GPU host.
- Start with the 2GB 1000-step config before attempting the 2GB 3000-step config.
- Copy back only small result packages and validation summaries unless a later step explicitly approves checkpoint transfer.

## Stop Conditions

Stop before training if any of these occur:

- prepared package missing or hash mismatch;
- train/val split files missing after extraction;
- config is not streaming;
- tokenizer/model vocab size differs from `16384`;
- exact parameter count differs from `336106496`;
- readiness reports blockers;
- GPU host attempts to fetch Hugging Face data for the 2GB slice.

Stop during or after a future run if any of these occur:

- CUDA OOM;
- non-finite train loss, validation loss, or gradients;
- checkpoint reload mismatch;
- post-run artifact validation failure.

## What MVP-21.P Does Not Do

- no model training;
- no tokenizer training;
- no A100/A800 session;
- no checkpoint creation;
- no raw/processed/split data committed;
- no prepared tarball committed;
- no model core architecture change;
- no model-quality claim.

## Next Step

After this commit is pushed and explicitly approved for GPU execution, the next run should start with `configs/a100/fineweb_edu_2gb_300m_1000step_public16k_execute.json`. Only attempt the 2GB 3000-step run after the 1000-step run succeeds with finite losses, checkpoint reload match, and post-run artifact validation.
