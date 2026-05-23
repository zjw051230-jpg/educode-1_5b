# MVP-8 A800 Execution Receipt

## 1. Completion
- completed: `yes`

## 2. Machine Information
- machine / cloud provider: `A800-SXM4-40GB remote training session`
- GPU name: `A800-SXM4-40GB`
- CUDA available: `true`

## 3. Config and Command
- config path: `configs/a100/fineweb_edu_50mb_300m_10step_execute.json`
- training command: `python scripts/run_a100_300m_fineweb_edu_10step_training.py --config configs/a100/fineweb_edu_50mb_300m_10step_execute.json`
- max_steps: `10`
- parameter_count: `319329280`

## 4. Training Result
- first_train_loss: `9.181210`
- final_train_loss: `2.769437`
- final_val_loss: `9.134018`
- loss_finite: `true`
- metrics_rows: `10`
- validation_rows: `2`

## 5. Checkpoint / Output
- checkpoint_path: `experiments/a100/fineweb_edu_50mb_300m_10step_execute/checkpoints/checkpoint_step_0010.pt`
- checkpoint_reload_match: `true`
- output_dir: `experiments/a100/fineweb_edu_50mb_300m_10step_execute`
- copied back files:
  - `summary.json`
  - `summary.md`
  - `metrics.jsonl`
  - `run_config.json`
  - `run_metadata.json`
  - `preflight_summary.json`
  - `execution_readiness_summary.json`
- submitted checkpoint: `no`

## 6. Failure / Stability Notes
- OOM observed: `no`
- non-finite loss observed: `no`
- other blockers or caveats:
  - `core_model_feature_parity=false` due to rope vs learned_position_embedding mismatch
  - validation rows were embedded in `metrics.jsonl`

## 7. Next Step Recommendation
- next step: compare this completed 10-step smoke against the imported 100-step bounded run as a stronger short-range stability check
