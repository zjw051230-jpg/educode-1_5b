# MVP-21 A800 Streaming 2GB Training Plan

## Purpose

MVP-21 should use the locally prepared FineWeb-Edu 2GB split package for a bounded 300M public16k streaming training run on A800/A100, without fetching public corpus data on the GPU host.

This is a future execution plan only. MVP-20 did not enter A800/A100, run training, train a tokenizer, or change model architecture.

## Prerequisites

- MVP-20 package exists locally: `C:/Users/01/fineweb_edu_2gb_prepared_splits.tar.gz`.
- Package SHA-256 matches `1c02cdf74e5a883ac1fcbee2cb9ebcf5917b8de145aaf4bdc59b1da6c120d51a`.
- GPU host has enough disk for the extracted train/val splits plus run artifacts.
- GPU host has sufficient host RAM for streaming mode; the training path must keep `data_loading_mode=streaming`.
- Public 16k tokenizer remains `tokenizers/fineweb_edu_public_bpe_16k/tokenizer.json` with vocab size `16384`.

## Proposed Config Shape

Create a future execution config by copying the current public16k 300M streaming config and changing only the run/output/data fields needed for 2GB data.

Recommended initial config path:

```text
configs/a100/fineweb_edu_2gb_300m_3000step_public16k_execute.json
```

Recommended fields:

| field | value |
|---|---|
| train_path | `data/public_corpus/fineweb_edu_sample10bt_2gb/splits/fineweb_edu_2gb.train.jsonl` |
| val_path | `data/public_corpus/fineweb_edu_sample10bt_2gb/splits/fineweb_edu_2gb.val.jsonl` |
| tokenizer_path | `tokenizers/fineweb_edu_public_bpe_16k/tokenizer.json` |
| tokenizer_vocab_size | `16384` |
| model_size_label | `300m` |
| exact parameter target | `336106496` |
| sequence_length | `512` |
| batch_size | `8` |
| gradient_accumulation_steps | `4` |
| data_loading_mode | `streaming` |
| max_steps | `3000` first |
| eval_interval | `300` |
| checkpoint_interval | `3000` |

If the 3000-step run succeeds with finite losses, checkpoint reload match, and artifact validation, the prepared 5000-step 2GB follow-up config can be used only if enough rental time remains.

## Remote Execution Order

1. Upload `fineweb_edu_2gb_prepared_splits.tar.gz` to the GPU host.
2. Extract it under `data/public_corpus/fineweb_edu_sample10bt_2gb/`.
3. Verify package hash and `intake_validation_summary.json` counts.
4. Run config inspection and dry-run/readiness checks.
5. Run the bounded 3000-step streaming training command only after explicit approval.
6. Run post-run artifact validation.
7. Package only small result files for copyback.

## Stop Conditions

Stop before training if any of these occur:

- package hash mismatch;
- missing train/val split path;
- intake validation counts differ from MVP-20 manifest;
- config is not streaming;
- tokenizer vocab size is not `16384`;
- exact parameter count differs from `336106496`;
- readiness script reports blockers;
- GPU host attempts to fetch Hugging Face data for the 2GB slice.

Stop during/after training if any of these occur:

- CUDA OOM;
- non-finite train loss, val loss, or gradients;
- checkpoint reload mismatch;
- post-run artifact validation failure.

## Expected Claim Boundary

A future MVP-21 run would still be bounded training-systems evidence. It can support claims about data logistics, streaming stability, artifact validation, and loss finiteness, but not broad model quality.
