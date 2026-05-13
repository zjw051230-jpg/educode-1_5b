# T7.6 50-Step vs 100-Step Comparison

## 1. Purpose
The purpose of T7.6 is to compare the accepted bounded 50-step and bounded 100-step small-training runs before moving on to T8 A100/100M planning.

This step compares only existing reviewed run results.
It does not run new training, does not modify the training scripts, and does not change the model.

## 2. Compared Runs
Compared runs:
- 50-step run:
  - run_id: `20260514_024451_windows_cuda_50_step_small_real_data_training`
  - review: `docs/t7_2_50_step_small_real_data_training_review.md`
- 100-step run:
  - run_id: `20260514_030554_windows_cuda_100_step_small_real_data_training`
  - review: `docs/t7_5_100_step_small_training_review.md`

Both runs used:
- synthetic seed corpus only
- BPE tokenizer vocab size `1174`
- same tiny dense model path
- same local Windows GPU path
- periodic validation and final checkpoint reload checks

## 3. Metrics Table

| metric | 50-step run | 100-step run |
|---|---:|---:|
| run_id | `20260514_024451_windows_cuda_50_step_small_real_data_training` | `20260514_030554_windows_cuda_100_step_small_real_data_training` |
| max_steps | 50 | 100 |
| first_train_loss | 7.192344 | 7.206174 |
| final_train_loss | 4.074500 | 3.113705 |
| train_loss_drop | 3.117844 | 4.092469 |
| final_val_loss | 7.380465 | 8.295060 |
| checkpoint_reload_match | True | True |
| metrics_rows | 50 | 100 |
| validation_rows | 5 | 10 |

## 4. Interpretation
Interpretation:
- the 100-step run reached a lower final train loss than the 50-step run
- the 100-step run also produced a larger train-loss drop overall
- validation loss did not improve; instead, the 100-step run ended with a higher final validation loss than the 50-step run
- this is likely explained by the synthetic corpus being extremely small, the validation split containing only one document, and the model overfitting quickly on the tiny training path
- checkpoint reload, logging, validation, and training pipeline checks all passed in both runs

## 5. Acceptance Decision
Decision:
- the 50-step and 100-step runs are accepted as local small-training pipeline validation
- the 100-step run provides stronger evidence that the bounded local training pipeline remains stable over a longer horizon
- the comparison does not justify any claim about generalization or model quality

## 6. Limitations
Current limitations:
- synthetic seed corpus only
- validation split contains only one document
- not real external corpus
- not A100/B200
- not 1.5B
- validation loss behavior is too unstable to support quality claims
- results should be interpreted as pipeline evidence, not as meaningful language-model evaluation

## 7. Next Step
Recommended next step:
- T8 A100/100M planning
