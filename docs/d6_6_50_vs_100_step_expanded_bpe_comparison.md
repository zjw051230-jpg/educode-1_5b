# D6.6 50-Step vs 100-Step Expanded BPE Comparison

## 1. Purpose
The purpose of D6.6 is to compare the accepted bounded 50-step and bounded 100-step expanded-BPE small-training runs using the already recorded run artifacts only.

This step does not run new training, does not modify the training scripts, and does not change the model.

## 2. Compared Runs
Compared runs:
- 50-step run:
  - run_id: `20260515_014657_windows_cuda_50_step_expanded_bpe_training`
  - report: `docs/d6_1_50_step_expanded_bpe_training.md`
  - accepted by: `docs/d6_2_50_step_expanded_bpe_training_review.md`
- 100-step run:
  - run_id: `20260515_023640_windows_cuda_100_step_expanded_bpe_training`
  - report: `docs/d6_4_100_step_expanded_bpe_training.md`
  - accepted by: `docs/d6_5_100_step_expanded_bpe_training_review.md`

Both runs used:
- local Windows GPU
- expanded synthetic corpus train/val split files
- expanded BPE tokenizer path
- tiny decoder-only model path
- checkpoint save/reload validation

## 3. Metrics Table

| Metric | 50-step | 100-step |
|---|---:|---:|
| run_id | `20260515_014657_windows_cuda_50_step_expanded_bpe_training` | `20260515_023640_windows_cuda_100_step_expanded_bpe_training` |
| max_steps | 50 | 100 |
| first_train_loss | 7.633180 | 7.689178 |
| final_train_loss | 4.182922 | 3.109032 |
| train_loss_drop | 3.450258 | 4.580146 |
| final_val_loss | 7.184383 | 7.552639 |
| checkpoint_reload_match | True | True |

## 4. Interpretation
Observed comparison:
- the 100-step run reached a lower final train loss than the 50-step run
- the 100-step run also produced a higher final validation loss than the 50-step run
- this suggests that, on the current tiny expanded synthetic corpus, adding more steps pushes optimization further on the train path without producing a stronger validation signal
- the current expanded synthetic corpus and validation split remain small enough that continuing to add steps is more likely to bias results toward overfitting than toward meaningful quality improvement
- both runs still successfully validate that the expanded-BPE local training pipeline, checkpoint path, and structured logging path are functioning correctly

This comparison does not justify any claim about model quality or generalization ability.

## 5. Acceptance Decision
Decision:
- the comparison is accepted as a useful bounded-run analysis of the current expanded-BPE training path

Acceptance basis:
- both the 50-step and 100-step runs were already individually reviewed and accepted
- both runs recorded `checkpoint_reload_match = True`
- both runs showed clearly decreasing train loss
- the comparison reveals that the longer run improved train loss while weakening the validation endpoint on the current tiny synthetic validation set
- this is enough to inform the next project decision without requiring any new training

## 6. Limitations
Current limitations:
- both runs use the same small expanded synthetic corpus only
- the validation split is still extremely small
- higher final validation loss in the 100-step run is a useful warning sign, but it is not a robust scientific estimate of generalization
- these runs validate bounded engineering behavior, not formal model quality
- no conclusion here should be extended to full pretraining, larger hardware, or broader datasets

## 7. Next Step
Recommended next step:
- D7 corpus expansion batch 2

Reasoning:
- the next bottleneck is corpus scale, not the ability to keep increasing bounded local training steps
- the comparison indicates that more training steps on the current tiny expanded synthetic corpus are less valuable than increasing corpus breadth first
