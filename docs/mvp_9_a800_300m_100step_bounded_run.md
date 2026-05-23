# MVP-9 A800 300M 100-step Bounded Run

## 1. Purpose
The purpose of MVP-9 is to record the imported result artifacts from the completed remote A800-SXM4-40GB FineWeb-Edu `300M` `100-step` bounded training run.

This run extends MVP-8 beyond the shortest smoke and adds a stronger short-range stability check.
It still does not support model-quality claims.

## 2. Imported Result Package
Imported source bundle:
- `mvp9_a800_300m_100step_results.tar.gz`

Imported controlled directory:
- `experiments/a100/fineweb_edu_50mb_300m_100step_execute/results_imported/`

Imported small artifacts:
- `summary.json`
- `summary.md`
- `metrics.jsonl`
- `run_config.json`
- `run_metadata.json`

No checkpoint files were imported or committed in this step.

## 3. Run Identity
Observed run facts:
- machine class: `A800-SXM4-40GB`
- corpus: `FineWeb-Edu 50MB public corpus`
- tokenizer: `educode_bpe_mixed_domain_8k`
- parameter_count: `319329280`
- runtime_device: `cuda`
- runtime_dtype: `bf16`
- max_steps: `100`

## 4. Result Summary
Observed summary values:
- first_train_loss: `9.181210`
- final_train_loss: `2.413716`
- final_val_loss: `8.900962`
- loss_all_finite: `true`
- val_loss_all_finite: `true`
- grad_all_finite: `true`
- checkpoint_reload_match: `true`
- metrics_rows: `100`
- validation_rows: `5`
- tokens_seen: `1638400`
- elapsed_seconds: `33.971051`
- approximate_tokens_per_sec: `48229.299267`

## 5. Imported Validation
Validation script:
- `scripts/validate_a800_imported_training_results.py`

Imported-validation result:
- `status = success`
- `metrics_rows = 100`
- `validation_rows_in_metrics = 5`
- `final_step_present = true`
- `checkpoint_reload_match = true`

Imported validation summary:
- `experiments/a100/fineweb_edu_50mb_300m_100step_execute/results_imported/import_validation_summary.json`

## 6. Known Caveats
Recorded caveats:
- `core_model_feature_parity=false` because the config declares `rope` while the current core model path still uses `learned_position_embedding`
- `validation_metrics.jsonl` was not written separately; validation rows are embedded inside `metrics.jsonl`
- `checkpoint_path` points into the `10step_execute` directory even though the `100-step` run succeeded and `checkpoint_reload_match=true`; this is a logging/path caveat, not a training failure

## 7. Interpretation
Compared with the 10-step smoke, the 100-step bounded run adds more evidence that the short-range training loop remains numerically stable across repeated optimizer steps and periodic validation.

This imported result should still be interpreted as:
- a bounded training run
- a training systems validation result
- not a model-quality evaluation
- not final architecture validation

Validation loss should not be interpreted as a quality conclusion in this bounded setup.

## 8. Artifact Policy
This step does not commit:
- checkpoints
- raw data
- processed/splits large local artifacts
- the tar.gz bundle itself

## 9. Next Step
Recommended next step:
- compare MVP-8 and MVP-9 together as training-loop validation and decide whether the next approved scale step should stay bounded or move to a larger reviewed public-corpus/A100-A800 systems validation
