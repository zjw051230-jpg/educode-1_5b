# D11.6 50-step vs 100-step Domain BPE Comparison

## 1. Summary
The purpose of D11.6 is to compare the accepted bounded 50-step and bounded 100-step domain-BPE small-training runs using the already recorded run artifacts only.

This step does not run new training, does not modify the training scripts, and does not change the tokenizer, model, optimizer, or dataset pipeline.

High-level result:
- the 100-step run achieved a clearly lower final train loss than the 50-step run
- the validation endpoint did not improve alongside the extra training steps
- checkpoint reload was stable in both runs
- the comparison supports the claim that the local domain-BPE training chain is reproducible as a bounded engineering workflow
- the next bottleneck before D12 is corpus breadth and validation quality, not the ability to add more bounded local steps

## 2. Compared Runs
Compared runs:
- 50-step run:
  - run_id: `20260515_034606_windows_cuda_50_step_domain_bpe_training`
  - report: `docs/d11_1_50_step_domain_bpe_training.md`
  - accepted by: `docs/d11_2_50_step_domain_bpe_training_review.md`
  - config: `experiments/windows_cuda/20260515_034606_windows_cuda_50_step_domain_bpe_training/run_config.json`
  - checkpoint: `experiments/windows_cuda/20260515_034606_windows_cuda_50_step_domain_bpe_training/checkpoint_final.pt`
- 100-step run:
  - run_id: `20260516_171326_windows_cuda_100_step_domain_bpe_training`
  - report: `docs/d11_4_100_step_domain_bpe_training.md`
  - accepted by: `docs/d11_5_100_step_domain_bpe_training_review.md`
  - config: `experiments/windows_cuda/20260516_171326_windows_cuda_100_step_domain_bpe_training/run_config.json`
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
- no generation artifacts; generation was not part of these bounded runs

## 3. Metrics Table

| Metric | 50-step | 100-step |
|---|---:|---:|
| run_name / run_id | `20260515_034606_windows_cuda_50_step_domain_bpe_training` | `20260516_171326_windows_cuda_100_step_domain_bpe_training` |
| training steps | 50 | 100 |
| tokenizer type | `bpe` | `bpe` |
| corpus / dataset notes | domain synthetic corpus only; `41` train docs / `4` val docs | domain synthetic corpus only; `41` train docs / `4` val docs |
| first_train_loss | 8.485050 | 8.406959 |
| final_train_loss | 4.463557 | 3.124400 |
| train_loss_delta (final - first) | -4.021493 | -5.282559 |
| final_val_loss | 7.506592 | 7.694381 |
| checkpoint_reload_match | True | True |
| sample generation availability | None recorded | None recorded |
| acceptance status | Accepted by D11.2 | Accepted by D11.5 |

## 4. Observations
Observed comparison:
- the 100-step run produced a more pronounced train loss reduction than the 50-step run
- the final train loss improved from `4.463557` at 50 steps to `3.124400` at 100 steps
- the train loss delta also deepened from `-4.021493` to `-5.282559`, which shows that the longer bounded run continued to optimize the training path
- the final validation loss did not improve with the extra steps; it increased from `7.506592` to `7.694381`
- this indicates a train/validation gap on the current tiny synthetic validation split, even though validation remained finite throughout both runs
- the 100-step run still reached a lower minimum validation loss than its own final endpoint, which suggests the validation signal is noisy and too small to support strong model-quality conclusions
- both runs recorded `checkpoint_reload_match = True`, which confirms checkpoint save/load stability across both bounded budgets
- both runs wrote the expected bounded-run artifacts (`metrics.jsonl`, `summary.md`, `checkpoint_final.pt`, `run_metadata.json`, `run_config.json`)

## 5. Acceptance Judgment
Decision:
- the comparison is accepted as a useful bounded-run analysis of the current domain-BPE training path

Acceptance basis:
- both the 50-step and 100-step runs were already individually reviewed and accepted
- both runs recorded finite train/validation losses
- both runs recorded `checkpoint_reload_match = True`
- the 100-step run improved training optimization more than the 50-step run
- the comparison shows that longer bounded local training is reproducible, but does not produce a stronger final validation endpoint on the current tiny synthetic validation split
- this is enough to support an engineering conclusion without requiring any new training

## 6. Resume-ready Evidence
This comparison is strong resume-ready evidence for the claim that the project implements a small LLM experimentation platform from scratch, because it shows:
- a modular training stack that connects config, tokenizer, dataset intake, batching, model forward, loss, optimizer step, checkpointing, validation, and structured logging
- repeated bounded local runs on the same domain-BPE path with comparable artifact structure
- successful checkpoint reload verification across multiple bounded budgets
- the ability to analyze run artifacts after execution rather than relying only on terminal output
- disciplined interpretation of metrics, including distinguishing engineering validation from model-quality claims

What it does not prove:
- meaningful generalization quality
- formal large-scale pretraining
- external-data performance
- 1.5B-scale readiness

## 7. Next Step Recommendation
Recommended next step:
- move to D12 planning rather than extending the current local bounded step budget further

Most important gap to address before D12 execution:
- improve corpus breadth and validation quality first

Reasoning:
- the current results already show that the local training chain is reproducible and checkpoint-stable
- the main unresolved weakness is not whether the system can run longer, but whether the current domain synthetic corpus and tiny validation split provide a meaningful signal
- before any broader training claim, the project should either define an external/general text supplement plan or create another approved corpus-expansion batch with a stronger validation split
