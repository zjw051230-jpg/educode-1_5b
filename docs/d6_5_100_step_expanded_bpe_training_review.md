# D6.5 100-Step Expanded BPE Training Review

## 1. Purpose
The purpose of D6.5 is to review the completed bounded 100-step expanded-BPE small-training run from D6.4 using only the existing run artifacts.

This step does not run new training, does not modify the training script, and does not change the model.

## 2. Reviewed Run
Reviewed run:
- run_id: `20260515_023640_windows_cuda_100_step_expanded_bpe_training`
- run_dir: `D:/模型/educode-1_5b/experiments/windows_cuda/20260515_023640_windows_cuda_100_step_expanded_bpe_training`
- hardware: `Windows RTX 2080 Ti`
- config: `configs/windows/bpe_expanded_8k_smoke.json`
- stage: `windows_cuda`
- artifact files confirmed:
  - `run_metadata.json`
  - `run_config.json`
  - `metrics.jsonl`
  - `summary.md`
  - `checkpoint_final.pt`

## 3. Metrics Summary
Observed metrics from `metrics.jsonl` and the recorded run summary:
- metrics rows: `100`
- validation rows: `10`
- first_train_loss: `7.689178`
- final_train_loss: `3.109032`
- min_train_loss: `3.045063`
- max_train_loss: `7.689178`
- mean_train_loss: `4.336923`
- final_val_loss: `7.552639`
- min_val_loss: `7.076225`
- max_val_loss: `7.552639`
- mean_val_loss: `7.291576`
- train_loss_all_finite: `True`
- val_loss_all_finite: `True`
- checkpoint_reload_match: `True`

Interpretation:
- train loss decreased clearly across the bounded run
- validation loss remained finite at every scheduled evaluation point
- validation loss did not meaningfully improve and trended upward across later checkpoints, which is likely due to the tiny synthetic validation split rather than a useful quality signal
- these metrics confirm bounded local training-path behavior only and should not be treated as model-quality evidence

## 4. Checkpoint Result
Checkpoint review result:
- `checkpoint_final.pt` exists
- the run summary records `checkpoint_reload_match: True`
- the reviewed artifact set includes the expected final checkpoint and summary outputs

Interpretation:
- the bounded 100-step run produced a restorable final checkpoint artifact
- the documented reload sanity check passed for the reviewed run

## 5. Acceptance Decision
Decision:
- D6.4 is accepted as bounded 100-step expanded BPE small training run

Acceptance basis:
- required run artifacts exist
- `metrics.jsonl` contains the expected `100` rows
- validation rows equal `10`
- train loss decreased from `7.689178` to `3.109032`
- train and validation losses remained finite
- checkpoint reload passed
- the run stayed within the D6.3 guardrails for bounded local expanded-BPE training

## 6. Limitations
Current limitations:
- this is still not full pretraining
- the current corpus remains small synthetic educational data
- the validation split contains only `2` documents
- validation loss stayed finite but did not meaningfully improve and should not be interpreted as generalization
- the observed tokenizer vocab is `1846`, still below the nominal `8192` target path
- no claim should be made about model quality, downstream usefulness, or scale-readiness from this bounded run alone

## 7. Next Step
Recommended next step:
- D6.6 compare 50-step vs 100-step expanded BPE runs
- then D7 corpus expansion batch 2
