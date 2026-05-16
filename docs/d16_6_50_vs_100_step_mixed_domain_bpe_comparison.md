# D16.6 50-Step vs 100-Step Mixed/Domain BPE Comparison

## 1. Purpose
The purpose of D16.6 is to compare the accepted bounded 50-step and bounded 100-step mixed/domain BPE small-training runs using the already recorded run artifacts only.

This step does not run new training, does not modify the training scripts, and does not change the tokenizer, model, optimizer, or dataset pipeline.

## 2. Compared Runs
Compared runs:
- 50-step run:
  - run_id: `20260517_000844_windows_cuda_50_step_mixed_domain_bpe_training`
  - report: `docs/d16_1_50_step_mixed_domain_bpe_training.md`
  - accepted by: `docs/d16_2_50_step_mixed_domain_bpe_training_review.md`
  - checkpoint: `experiments/windows_cuda/20260517_000844_windows_cuda_50_step_mixed_domain_bpe_training/checkpoint_final.pt`
- 100-step run:
  - run_id: `20260517_004516_windows_cuda_100_step_mixed_domain_bpe_training`
  - report: `docs/d16_4_100_step_mixed_domain_bpe_training.md`
  - accepted by: `docs/d16_5_100_step_mixed_domain_bpe_training_review.md`
  - checkpoint: `experiments/windows_cuda/20260517_004516_windows_cuda_100_step_mixed_domain_bpe_training/checkpoint_final.pt`

Both runs used:
- local Windows GPU
- `mixed_domain_external` corpus train/val split files only
- `tokenizers/educode_bpe_mixed_domain_8k/tokenizer.json`
- tokenizer type `bpe`
- observed vocab size `8192`
- the same mixed/domain BPE smoke config family
- the same tiny decoder-only model path
- checkpoint save/reload validation

## 3. Metrics Table

| Metric | 50-step | 100-step |
|---|---:|---:|
| run_id | `20260517_000844_windows_cuda_50_step_mixed_domain_bpe_training` | `20260517_004516_windows_cuda_100_step_mixed_domain_bpe_training` |
| max_steps | 50 | 100 |
| first_train_loss | 9.161793 | 9.161793 |
| final_train_loss | 4.809736 | 3.796839 |
| train_loss_drop | 4.352057 | 5.364954 |
| final_val_loss | 7.669892 | 7.833482 |
| checkpoint_reload_match | True | True |

## 4. Source Category Preservation
Recorded source-category counts in both runs:
- train: `{"external_general_text": 11, "synthetic_examples": 41}`
- val: `{"external_general_text": 1, "synthetic_examples": 4}`

Comparison result:
- both runs preserved the same mixed-corpus provenance counts
- `synthetic_examples` remained the majority source in both train and val
- `external_general_text` remained supplement only
- both runs kept the backbone/supplement distinction intact

## 5. Interpretation
Observed comparison:
- the 100-step run achieved a lower final train loss than the 50-step run
- the 100-step run also produced a larger train-loss drop, which shows that the longer bounded run pushed optimization further on the training path
- the 100-step run ended with a higher final validation loss than the 50-step run, so validation did not improve alongside the extra steps
- this indicates that the current `mixed_domain_external` corpus remains small enough that continuing to add steps is more likely to bias results toward overfitting than to produce a stronger validation signal
- both runs recorded `checkpoint_reload_match = True`, which confirms that the mixed/domain BPE training pipeline, checkpoint reload path, and structured logging path are functioning correctly
- both runs also preserved source-category recording, which confirms that the mixed-corpus provenance chain remained intact through training
- these results do not justify any model-quality or generalization claim

## 6. Acceptance Decision
Decision:
- the comparison is accepted as a useful bounded-run analysis of the current mixed/domain BPE training path

Acceptance basis:
- both the 50-step and 100-step runs were already individually reviewed and accepted
- both runs showed clearly decreasing train loss
- both runs recorded finite validation loss
- both runs recorded `checkpoint_reload_match = True`
- the comparison reveals that the longer run improved train loss while worsening the final validation endpoint on the current small mixed corpus
- this is enough to inform the next project decision without requiring any new training

## 7. Limitations
Current limitations:
- both runs use the same small controlled mixed corpus only
- the validation split is still very small
- higher final validation loss in the 100-step run is a useful overfitting signal, but it is not a robust scientific estimate of generalization
- these runs validate bounded engineering behavior, not formal model quality
- no conclusion here should be extended to full pretraining, larger hardware, or broader datasets

## 8. Next Step
Recommended next step:
- A2 A100 mixed/domain training plan
- or more corpus expansion before any further local step-stacking

Reasoning:
- the next bottleneck is corpus breadth and validation quality, not the ability to keep increasing bounded local training steps
- the comparison indicates that more local steps on the current small mixed corpus are less valuable than better scale planning or better corpus breadth first
