# MVP-8 A800 300M 10-step Training Smoke

## 1. Purpose
The purpose of MVP-8 is to record the imported result artifacts from the completed remote A800-SXM4-40GB FineWeb-Edu `300M` `10-step` bounded training smoke.

This run should be interpreted as a training systems smoke.
It does not support model-quality claims.

## 2. Imported Result Package
Imported source bundle:
- `mvp8_a800_300m_10step_results.tar.gz`

Imported controlled directory:
- `experiments/a100/fineweb_edu_50mb_300m_10step_execute/results_imported/`

Imported small artifacts:
- `summary.json`
- `summary.md`
- `metrics.jsonl`
- `run_config.json`
- `run_metadata.json`
- `preflight_summary.json`
- `execution_readiness_summary.json`

No checkpoint files were imported or committed in this step.

## 3. Run Identity
Observed run facts:
- machine class: `A800-SXM4-40GB`
- corpus: `FineWeb-Edu 50MB public corpus`
- tokenizer: `educode_bpe_mixed_domain_8k`
- parameter_count: `319329280`
- runtime_device: `cuda`
- runtime_dtype: `bf16`
- max_steps: `10`
- run_id: `20260523_211309_a100_fineweb_edu_50mb_300m_10step_smoke`

## 4. Result Summary
Observed summary values:
- first_train_loss: `9.181210`
- final_train_loss: `2.769437`
- final_val_loss: `9.134018`
- loss_all_finite: `true`
- grad_all_finite: `true`
- checkpoint_reload_match: `true`
- metrics_rows: `10`
- validation_rows: `2`
- tokens_seen: `163840`
- approximate_tokens_per_sec: `43245.612399`

## 5. Imported Validation
Validation script:
- `scripts/validate_a800_imported_training_results.py`

Imported-validation result:
- `status = success`
- `metrics_rows = 10`
- `validation_rows_in_metrics = 2`
- `final_step_present = true`
- `checkpoint_reload_match = true`

Imported validation summary:
- `experiments/a100/fineweb_edu_50mb_300m_10step_execute/results_imported/import_validation_summary.json`

## 6. Known Caveats
Recorded caveats:
- `core_model_feature_parity=false` because the config declares `rope` while the current core model path still uses `learned_position_embedding`
- `validation_metrics.jsonl` was not written separately; validation rows are embedded inside `metrics.jsonl`

These caveats do not invalidate the imported training smoke result.

## 7. Interpretation
This imported run confirms that the bounded public-corpus training path completed:
- data loading
- tokenizer loading
- model construction
- forward/loss
- backward
- optimizer steps
- periodic validation
- checkpoint save/reload verification
- metrics/summary writing

This is a training systems smoke only.
It is not a final architecture validation and does not support model-quality conclusions.

## 8. Artifact Policy
This step does not commit:
- checkpoints
- raw data
- processed/splits large local artifacts
- the tar.gz bundle itself

## 9. Next Step
Recommended next step:
- compare this 10-step smoke against the imported 100-step bounded run to judge short-run stability rather than model quality
