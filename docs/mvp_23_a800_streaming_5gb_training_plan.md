# MVP-23 A800 Streaming 5GB Training Plan

## Purpose

Prepare the 5GB FineWeb-Edu public16k A800/A100 training route after MVP-22.P creates and validates the 5GB prepared split package.

This is an execution plan only. It does not run training, enter A800/A100, train a tokenizer/model, create checkpoints, or change model architecture.

## Prepared Corpus Requirement

The 5GB training configs require these local/remote split paths:

```text
data/public_corpus/fineweb_edu_sample10bt_5gb/splits/fineweb_edu_5gb.train.jsonl
data/public_corpus/fineweb_edu_sample10bt_5gb/splits/fineweb_edu_5gb.val.jsonl
```

The GPU host should receive the MVP-22.P prepared package:

```text
C:/Users/01/fineweb_edu_5gb_prepared_splits.tar.gz
```

Package size is `2112167310` bytes, SHA-256 is `19a933ec5afc379d58751461ff56e8e89be4d3fbfc05e10df789c6541f8bcd5d`.

## Configs

| config | max_steps | eval_interval | checkpoint_interval | output_dir |
|---|---:|---:|---:|---|
| `configs/a100/fineweb_edu_5gb_300m_1000step_public16k_execute.json` | `1000` | `100` | `1000` | `experiments/a100/fineweb_edu_5gb_300m_1000step_public16k_execute` |
| `configs/a100/fineweb_edu_5gb_300m_3000step_public16k_execute.json` | `3000` | `300` | `3000` | `experiments/a100/fineweb_edu_5gb_300m_3000step_public16k_execute` |

Both configs keep:

- `data_loading_mode=streaming`
- `batch_size=8`
- `gradient_accumulation_steps=4`
- `sequence_length=512`
- public16k tokenizer vocab size `16384`
- model vocab size `16384`
- exact parameter target `336106496`
- `checkpoint.no_commit_checkpoints=true`

## Local Readiness Evidence

| config | memory inspection | dry-run | readiness |
|---|---|---|---|
| 1000-step | streaming host-RAM safe; batch tensor `0.062` MiB; old precompute estimate `129.024313` GiB | passed; `exact_parameter_count=336106496` | passed; blockers `0`, caveats `0` |
| 3000-step | streaming host-RAM safe; batch tensor `0.062` MiB; old precompute estimate `387.080954` GiB | passed; `exact_parameter_count=336106496` | passed; blockers `0`, caveats `0` |

## Execution Order

1. Upload and verify the 5GB prepared split package.
2. Extract under `data/public_corpus/fineweb_edu_sample10bt_5gb/`.
3. Verify `manifest.json`, `validation_summary.json`, `intake_summary.json`, `intake_validation_summary.json`, train split, and val split exist.
4. Run memory inspection, dry-run, and readiness for the 1000-step config.
5. Execute the 1000-step run only after explicit approval.
6. Run post-run artifact validation and package small result artifacts.
7. Attempt 3000-step only after 1000-step succeeds with finite losses, checkpoint reload match, and post-run artifact validation.

## Stop Conditions

Stop before training if any of these occur:

- 5GB package missing or hash mismatch;
- train/val split files missing;
- readiness reports blockers;
- config is not streaming;
- tokenizer/model vocab size differs from `16384`;
- exact parameter count differs from `336106496`;
- GPU host attempts Hugging Face fetch for the prepared 5GB slice.

Stop during or after training if any of these occur:

- CUDA OOM;
- non-finite train loss, validation loss, or gradients;
- checkpoint reload mismatch;
- post-run artifact validation failure.

## Claim Boundary

A future MVP-23 run is bounded training-systems evidence for prepared-data logistics, streaming batch stability, and artifact validation. It is not model-quality evidence.
