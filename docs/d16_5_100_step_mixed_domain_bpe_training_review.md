# D16.5 Review 100-Step Mixed/Domain BPE Training Run

## 1. Purpose
The purpose of D16.5 is to review the completed D16.4 bounded 100-step mixed/domain BPE small-training run using the saved run artifacts only.

This step is a review milestone only.
It does not run new training, change the training script, or modify model code.

## 2. Reviewed Run
Reviewed run:
- run_id: `20260517_004516_windows_cuda_100_step_mixed_domain_bpe_training`
- run_dir: `experiments/windows_cuda/20260517_004516_windows_cuda_100_step_mixed_domain_bpe_training/`
- device: `cuda`
- max_steps: `100`
- eval_interval: `10`
- train docs: `52`
- val docs: `5`
- tokenizer vocab size: `8192`

Reviewed artifacts:
- `metrics.jsonl`
- `summary.md`
- `summary.json`
- `checkpoint_final.pt`
- `run_metadata.json`

## 3. Metrics Summary
Observed training metrics:
- metrics rows: `100`
- validation rows: `10`
- first_train_loss: `9.161793`
- final_train_loss: `3.796839`
- min_train_loss: `3.482412`
- max_train_loss: `9.161793`
- mean_train_loss: `5.143302`
- final_val_loss: `7.833482`
- min_val_loss: `7.568005`
- max_val_loss: `8.661902`
- mean_val_loss: `7.916027`
- train_loss_all_finite: `true`
- val_loss_all_finite: `true`

Interpretation:
- train loss decreased clearly across the bounded run
- validation loss remained finite at every scheduled review point
- the run satisfied the expected `100` training records and `10` validation records
- final validation loss is higher than the accepted D16.1 50-step run final validation loss `7.669892`, so the longer bounded run should be treated as an overfitting signal on the current small mixed corpus rather than a reason to keep stacking local steps

## 4. Source Category Check
Recorded source-category counts:
- train: `{"external_general_text": 11, "synthetic_examples": 41}`
- val: `{"external_general_text": 1, "synthetic_examples": 4}`

Review result:
- source-category counts were recorded in the run artifacts
- the counts preserve the backbone/supplement distinction
- `synthetic_examples` remained the majority source in both train and val
- `external_general_text` remained supplement only

## 5. Checkpoint Result
Checkpoint review:
- checkpoint exists: `true`
- checkpoint reload match: `true`

This confirms that the bounded run completed its final checkpoint path and passed the reload sanity check.

## 6. Acceptance Decision
Decision:
- D16.4 accepted as a bounded 100-step mixed/domain BPE small training run

Acceptance basis:
- train loss decreased clearly
- val loss remained finite
- final validation loss is higher than the D16.1 50-step run, which is an overfitting signal on the current small mixed corpus
- checkpoint reload passed
- source-category counts were recorded and preserved the backbone/supplement distinction
- `external_general_text` remained supplement only

## 7. Limitations
This review does not change the project limitations:
- still not full pretraining
- still not A100 or 1.5B-scale work
- still no model quality claim
- still no generalization claim
- the mixed corpus remains small and controlled
- the external text portion remains a supplement only, not a general-language backbone

## 8. Next Step
Recommended next step:
- D16.6 compare the bounded 50-step and 100-step mixed/domain BPE runs
- then A2 planning or more corpus expansion, not more local step-stacking on the current small mixed corpus
