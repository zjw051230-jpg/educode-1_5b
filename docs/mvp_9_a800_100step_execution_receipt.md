# MVP-9 A800 100-step Execution Receipt

## 1. Completion
- completed: `yes`

## 2. Machine Information
- machine / cloud provider: `A800-SXM4-40GB remote training session`
- GPU name: `A800-SXM4-40GB`
- CUDA available: `true`

## 3. Config and Command
- config path: `configs/a100/fineweb_edu_50mb_300m_100step_execute.json`
- training command: `python scripts/run_a100_300m_fineweb_edu_10step_training.py --config configs/a100/fineweb_edu_50mb_300m_100step_execute.json`
- max_steps: `100`
- parameter_count: `319329280`

## 4. Training Result
- first_train_loss: `9.181210`
- final_train_loss: `2.413716`
- final_val_loss: `8.900962`
- loss_finite: `true`
- metrics_rows: `100`
- validation_rows: `5`

## 5. Checkpoint / Output
- checkpoint_path: `experiments/a100/fineweb_edu_50mb_300m_10step_execute/checkpoints/checkpoint_step_0100.pt`
- checkpoint_reload_match: `true`
- output_dir: `experiments/a100/fineweb_edu_50mb_300m_100step_execute`
- copied back files:
  - `summary.json`
  - `summary.md`
  - `metrics.jsonl`
  - `run_config.json`
  - `run_metadata.json`
- submitted checkpoint: `no`

## 6. Failure / Stability Notes
- OOM observed: `no`
- non-finite loss observed: `no`
- other blockers or caveats:
  - `core_model_feature_parity=false` due to rope vs learned_position_embedding mismatch
  - validation rows were embedded in `metrics.jsonl`
  - `checkpoint_path` has a logging/path mismatch and still points into the `10step_execute` directory even though the 100-step run succeeded

## 7. Next Step Recommendation
- next step: use this bounded 100-step result as evidence of short-range training stability, not as a model-quality conclusion
