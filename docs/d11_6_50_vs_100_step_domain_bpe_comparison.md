# D11.6 50-step vs 100-step Domain BPE Comparison

## 1. Purpose
The purpose of D11.6 is to compare the accepted bounded 50-step and bounded 100-step domain-BPE small-training runs using the already recorded run artifacts only.

This step does not run new training, does not modify the training scripts, and does not change the tokenizer, model, optimizer, or dataset pipeline.

## 2. Compared Runs
Compared runs:
- 50-step run:
  - run_id: `20260515_034606_windows_cuda_50_step_domain_bpe_training`
  - report: `docs/d11_1_50_step_domain_bpe_training.md`
  - accepted by: `docs/d11_2_50_step_domain_bpe_training_review.md`
  - checkpoint: `experiments/windows_cuda/20260515_034606_windows_cuda_50_step_domain_bpe_training/checkpoint_final.pt`
- 100-step run:
  - run_id: `20260516_171326_windows_cuda_100_step_domain_bpe_training`
  - report: `docs/d11_4_100_step_domain_bpe_training.md`
  - accepted by: `docs/d11_5_100_step_domain_bpe_training_review.md`
  - checkpoint: `experiments/windows_cuda/20260516_171326_windows_cuda_100_step_domain_bpe_training/checkpoint_final.pt`

Both runs used:
- local Windows GPU
- domain synthetic corpus train/val split files only
- `tokenizers/educode_bpe_domain_8k/tokenizer.json`
- tokenizer type `bpe`
- observed vocab size `3988`
- the same domain BPE smoke config family
- the same tiny decoder-only model path
- checkpoint save/reload validation

## 3. Metrics Table

| Metric | 50-step | 100-step |
|---|---:|---:|
| run_id | `20260515_034606_windows_cuda_50_step_domain_bpe_training` | `20260516_171326_windows_cuda_100_step_domain_bpe_training` |
| max_steps | 50 | 100 |
| first_train_loss | 8.485050 | 8.406959 |
| final_train_loss | 4.463557 | 3.124400 |
| train_loss_drop | 4.021493 | 5.282559 |
| final_val_loss | 7.506592 | 7.694381 |
| checkpoint_reload_match | True | True |

## 4. Interpretation
Observed comparison:
- the 100-step run achieved a lower final train loss than the 50-step run
- the 100-step run also produced a larger train-loss drop, which shows that the longer bounded run pushed optimization further on the training path
- the 100-step run ended with a higher final validation loss than the 50-step run, so validation did not improve alongside the extra steps
- this indicates a train/validation gap on the current small domain synthetic validation split
- the current domain synthetic corpus remains small enough that continuing to add steps is more likely to bias results toward overfitting than to produce a stronger validation signal
- both runs recorded `checkpoint_reload_match = True`, which confirms that the domain-BPE training pipeline, checkpoint path, and structured logging path are functioning correctly
- these results support the claim that the project has a working from-scratch small LLM experimentation platform, but they do not justify any model-quality or generalization claim

## 5. Acceptance Decision
Decision:
- the comparison is accepted as a useful bounded-run analysis of the current domain-BPE training path

Acceptance basis:
- both the 50-step and 100-step runs were already individually reviewed and accepted
- both runs showed clearly decreasing train loss
- both runs recorded finite validation loss
- both runs recorded `checkpoint_reload_match = True`
- the comparison reveals that the longer run improved train loss while weakening the final validation endpoint on the current small synthetic validation split
- this is enough to inform the next project decision without requiring any new training

## 6. Limitations
Current limitations:
- both runs use the same small domain synthetic corpus only
- the validation split is still very small
- higher final validation loss in the 100-step run is a useful warning sign, but it is not a robust scientific estimate of generalization
- these runs validate bounded engineering behavior, not formal model quality
- no conclusion here should be extended to full pretraining, larger hardware, or broader datasets

## 7. Next Step
Recommended next step:
- D12 external/general text supplement plan or D12 corpus expansion batch 3

Reasoning:
- the next bottleneck is corpus breadth and validation quality, not the ability to keep increasing bounded local training steps
- the comparison indicates that more training steps on the current small domain synthetic corpus are less valuable than improving corpus breadth and validation quality first
