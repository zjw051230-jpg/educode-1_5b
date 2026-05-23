# MVP-8.P A100 Execution Preflight Gate

## 1. Purpose
The purpose of MVP-8.P is to complete the final local preflight gate before a real A100 FineWeb-Edu `300M` `10-step` execution smoke.

This step is limited to config review, execution-config creation, execution-readiness checking, and execution-package definition.
It does not enter A100 and does not run real training.

## 2. Input MVP-7 Results
Inputs carried forward from MVP-7:
- script: `scripts/run_a100_300m_fineweb_edu_10step_training.py`
- smoke config: `configs/a100/fineweb_edu_50mb_300m_10step_smoke.json`
- dry-run summary: `experiments/a100/fineweb_edu_50mb_300m_10step_smoke/dry_run_summary.json`

Observed MVP-7 dry-run facts:
- `exact_parameter_count = 319329280`
- `runtime_dtype = bf16`
- `model_materialized_locally = true`
- `memory_limited_local_dry_run = false`
- `core_model_feature_parity = false`

These results are treated as prerequisites for the MVP-8.P execution gate.

## 3. Config Review
Reviewed smoke config:
- `run_name = fineweb_edu_50mb_300m_10step_smoke`
- `train_path = data/public_corpus/fineweb_edu_sample10bt_50mb/splits/fineweb_edu_50mb.train.jsonl`
- `val_path = data/public_corpus/fineweb_edu_sample10bt_50mb/splits/fineweb_edu_50mb.val.jsonl`
- `tokenizer_path = tokenizers/educode_bpe_mixed_domain_8k/tokenizer.json`
- `tokenizer_vocab_size = 8192`
- `model_size_label = 300m`
- `sequence_length = 512`
- `batch_size = 8`
- `gradient_accumulation_steps = 4`
- `max_steps = 10`
- `eval_interval = 5`
- `checkpoint_interval = 10`
- `precision = bf16_if_available_else_fp16`
- `output_dir = experiments/a100/fineweb_edu_50mb_300m_10step_smoke`
- `no_commit_checkpoints = true`
- `training.no_training = true`

Conclusion from the review:
- the smoke config remains intentionally blocked for execution because `training.no_training=true`
- a separate reviewed execution config is required before the real A100 smoke can be launched

## 4. no_training Switch
MVP-8.P created a dedicated execution config rather than editing the smoke config in place.

Execution gate decision:
- smoke config keeps `training.no_training=true`
- execution config sets `training.no_training=false`

This preserves the dry-run-safe config while giving the future A100 run a distinct reviewed execution entry point.

## 5. Execution Config
Execution config created:
- `configs/a100/fineweb_edu_50mb_300m_10step_execute.json`

Key properties retained:
- `max_steps = 10`
- `eval_interval = 5`
- `checkpoint_interval = 10`
- `no_commit_checkpoints = true`
- `purpose = "A100 10-step execution smoke, not model quality claim"`
- unchanged public-corpus train/val paths
- unchanged tokenizer path

Execution-specific adjustments:
- `run_name = fineweb_edu_50mb_300m_10step_execute`
- `output_dir = experiments/a100/fineweb_edu_50mb_300m_10step_execute`
- `training.no_training = false`
- checkpoint save dir moved under the execution output root

## 6. Readiness Check Result
Readiness gate script created:
- `scripts/check_a100_execution_readiness.py`

Local validation commands run in this step:

```text
.venv/Scripts/python.exe -m py_compile scripts/check_a100_execution_readiness.py
.venv/Scripts/python.exe scripts/check_a100_execution_readiness.py --config configs/a100/fineweb_edu_50mb_300m_10step_execute.json
```

Observed readiness result:
- `status = success`
- `training_no_training = false`
- `max_steps = 10`
- `checkpoint_interval = 10`
- `no_commit_checkpoints = true`
- `ready_for_a100_execution = true`
- `blockers = 0`
- `caveats = 1`

Readiness summary written:
- `experiments/a100/fineweb_edu_50mb_300m_10step_execute/execution_readiness_summary.json`

## 7. Core Model Feature Parity Caveat
MVP-8.P preserves the existing MVP-7 caveat:
- `core_model_feature_parity=false`

Reason:
- the current execution path still uses the existing core model implementation
- the config declares `position_encoding=rope`
- the current core model path still uses learned position embeddings

Interpretation rule:
- this is not a blocker for MVP-8 execution preflight
- it is a caveat that limits interpretation of the future A100 result
- MVP-8 remains a training-systems smoke, not final architecture validation

## 8. Required A100 Files
Required files for the future A100 execution step:
- `configs/a100/fineweb_edu_50mb_300m_10step_execute.json`
- `scripts/run_a100_300m_fineweb_edu_10step_training.py`
- `scripts/check_a100_execution_readiness.py`
- `scripts/preflight_a100_fineweb_edu_smoke.py`
- `tokenizers/educode_bpe_mixed_domain_8k/tokenizer.json`
- `data/public_corpus/fineweb_edu_sample10bt_50mb/splits/fineweb_edu_50mb.train.jsonl`
- `data/public_corpus/fineweb_edu_sample10bt_50mb/splits/fineweb_edu_50mb.val.jsonl`
- `experiments/a100/fineweb_edu_50mb_300m_10step_smoke/dry_run_summary.json`

## 9. Execution Command
Approved future A100 execution command:

```text
python scripts/run_a100_300m_fineweb_edu_10step_training.py --config configs/a100/fineweb_edu_50mb_300m_10step_execute.json
```

This command was not run in MVP-8.P.

## 10. Stop Conditions
Stop the future A100 execution if any of the following occurs:
- `torch.cuda.is_available()` is `False`
- GPU name is not `A100`
- tokenizer path is missing
- FineWeb-Edu train/val split files are missing
- dry-run summary is missing
- `exact_parameter_count` is not `319329280`
- `model_materialized_locally` is not `true`
- `memory_limited_local_dry_run` is not `false`
- `training.no_training` is not `false` in the execution config
- `max_steps` is not `10`
- `checkpoint_interval` is not `10`
- `no_commit_checkpoints` is not `true`
- output dir escapes `experiments/a100/`

## 11. What MVP-8.P Does Not Do
MVP-8.P does not:
- enter A100
- run real training
- train a tokenizer
- modify core model code
- change the public-corpus train/val paths
- claim final architecture validation
- commit checkpoints
- commit `raw.jsonl`
- commit local `processed/` or `splits/` artifacts

## 12. Next Step
Recommended next step:
- run the reviewed execution config on the target A100 machine and fill the execution receipt after the bounded `10-step` smoke completes or fails
