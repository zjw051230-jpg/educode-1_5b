# MVP-15 A800 3000-step Public16k Bounded Run Plan

## Purpose

MVP-15 defines a conditional `300M` public16k `3000-step` bounded follow-up run on the FineWeb-Edu `500MB` public corpus.

This is not execution approval. It prepares the second queue item for a future A800/A100 rental after the MVP-14 `1000-step` run succeeds.

## Why 3000-step After 1000-step

The `1000-step` run remains the primary gate because it validates the public16k config, logging cleanup, checkpoint path discipline, and runtime stability with lower cost. A `3000-step` follow-up is useful only after that gate passes because it adds longer short-run stability evidence while still staying bounded enough for a one-hour queue.

## Input Corpus

| field | value |
|---|---|
| dataset_id | `HuggingFaceFW/fineweb-edu` |
| dataset_config | `sample-10BT` |
| source_slice | `500MB` |
| license | `odc-by` |
| train_path | `data/public_corpus/fineweb_edu_sample10bt_500mb/splits/fineweb_edu_500mb.train.jsonl` |
| val_path | `data/public_corpus/fineweb_edu_sample10bt_500mb/splits/fineweb_edu_500mb.val.jsonl` |

## Tokenizer

| field | value |
|---|---|
| tokenizer_source | `fineweb_edu_public_bpe_16k` |
| tokenizer_path | `tokenizers/fineweb_edu_public_bpe_16k/tokenizer.json` |
| vocab_size | `16384` |
| special tokens | `<|endoftext|>`, `<|pad|>`, `<|unk|>` |

## Config Path

```text
configs/a100/fineweb_edu_500mb_300m_3000step_public16k_execute.json
```

Key run bounds:

| field | value |
|---|---:|
| max_steps | `3000` |
| eval_interval | `300` |
| checkpoint_interval | `3000` |
| batch_size | `8` |
| gradient_accumulation_steps | `4` |
| sequence_length | `512` |
| global_batch_tokens | `16384` |

## Expected Runtime

Expected runtime depends on provider setup time and GPU class. The run is prepared as a conditional second item for a `1×A800/A100 40GB` rental window. Use `1 hour` only if setup is already fast; use `2 hours` if environment restore, upload/download, or dependency checks are uncertain.

## Success Criteria

A completed MVP-15 run should satisfy:

| check | expected |
|---|---|
| metrics_rows | `3000` |
| validation_rows | `>= 10` |
| loss_all_finite | `true` |
| val_loss_all_finite | `true` |
| grad_all_finite | `true` |
| checkpoint_reload_match | `true` |
| tokenizer_vocab_size | `16384` |
| checkpoint_path | inside `experiments/a100/fineweb_edu_500mb_300m_3000step_public16k_execute` |

Post-run validation command:

```text
.venv/Scripts/python.exe scripts/validate_a800_public16k_run_artifacts.py --output-dir experiments/a100/fineweb_edu_500mb_300m_3000step_public16k_execute
```

## Artifact Policy

Commit or copy back only small review artifacts:

- `summary.json`
- `summary.md`
- `metrics.jsonl`
- `validation_metrics.jsonl`
- `run_config.json`
- `run_metadata.json`
- `post_run_artifact_validation_summary.json`

Do not commit or copy back checkpoints, raw corpus files, processed corpus files, split corpus files, or result bundles containing checkpoints.

## What MVP-15 Does Not Prove

Even if MVP-15 succeeds, it does not prove:

- model quality;
- final generalization;
- final architecture quality;
- long-run stability;
- production-grade training throughput;
- that RoPE or FlashAttention-2 has been implemented;
- unbiased sampling quality, because this remains a bounded prefix-batch run unless the script changes sampling.

## Next Decision

If the `3000-step` run is stable, choose the next route explicitly:

- larger public corpus slice;
- `1B` smoke/profile path;
- sampling improvements before longer runs;
- tokenizer or corpus-quality improvements before additional step stacking.
