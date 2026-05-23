# MVP-13 300M 1000-step Preparation

## 1. Status

MVP-13 is complete as a planning and decision step once its docs and draft configs are committed.

This step prepares the next A100/A800 route without running local training, GPU training, tokenizer training, or data download.

## 2. Decision Summary

Decision: use the public FineWeb-Edu `16k` tokenizer as the intended tokenizer for the next public-corpus `300M` `1000-step` run, but do not run the GPU experiment directly.

Required next gate: MVP-13.1 local public `16k` data/model/loss smoke.

## 3. New Configs

Local smoke config:

```text
configs/windows/fineweb_edu_500mb_public16k_data_model_loss_smoke.json
```

Purpose: verify data/model/loss compatibility for the public `16k` tokenizer without training.

GPU execution draft:

```text
configs/a100/fineweb_edu_500mb_300m_1000step_public16k_execute.json
```

Purpose: draft the later bounded A100/A800 `300M` `1000-step` run after MVP-13.1 passes.

## 4. New Planning Docs

Tokenizer decision:

```text
docs/mvp_13_tokenizer_decision_for_300m_1000step.md
```

Bounded run plan:

```text
docs/mvp_13_300m_1000step_bounded_run_plan.md
```

Local smoke plan:

```text
docs/mvp_13_1_public16k_data_model_loss_smoke_plan.md
```

Preparation summary:

```text
docs/mvp_13_300m_1000step_preparation.md
```

## 5. Evidence Carried Forward

### MVP-9 A800 100-step result

MVP-9 remains the strongest completed GPU training-systems evidence:

- `max_steps=100`;
- `exact_parameter_count=319329280`;
- `metrics_rows=100`;
- `validation_rows=5`;
- `tokens_seen=1638400`;
- `checkpoint_reload_match=true`;
- finite train loss, validation loss, and gradients.

### MVP-11.1 500MB corpus

The FineWeb-Edu `500MB` corpus path is available locally:

- `train_count=103619`;
- `val_count=5498`;
- `processed_count=109117`;
- raw, processed, and split files remain local-only and ignored.

### MVP-12 public tokenizer

The public `16k` tokenizer is available:

- `observed_vocab_size=16384`;
- `round_trip_fail_count=0`;
- `unk_token_count_on_samples=0`;
- `token_count_ratio_public_vs_mixed=0.707934` on sampled FineWeb-Edu text.

## 6. MVP-10 Cleanup Requirements Preserved

Before the later GPU run, the runner/reporting path must:

- write standalone `validation_metrics.jsonl`;
- derive checkpoint path from the current run output directory;
- use a run ID that accurately says `1000step`;
- avoid claiming a scheduler unless the execution script applies one;
- run post-run artifact validation;
- preserve the distinction between current `learned_position_embedding` execution and future RoPE architecture goals.

## 7. Scope Boundary

MVP-13 did not:

- run model training;
- run the MVP-13.1 smoke;
- enter A100/A800;
- train a tokenizer;
- download new data;
- modify core model code;
- advance D20/E work;
- commit raw corpus files, processed/splits files, checkpoints, or result bundles.

## 8. Recommended Next Step

Next step: implement and run MVP-13.1 local public `16k` data/model/loss smoke.

Only after that smoke passes should a later MVP approve the A100/A800 `300M` `1000-step` public-tokenizer execution.
