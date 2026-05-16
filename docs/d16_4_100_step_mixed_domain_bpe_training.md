# D16.4 100-Step Mixed/Domain BPE Training

## 1. Purpose
The purpose of D16.4 is to run the next bounded 100-step local small-training experiment on the approved mixed/domain BPE path after the accepted D16.1 50-step run and the D16.3 plan.

This run is a local bounded validation step only.
It is not formal large-scale pretraining.

## 2. Run Overview
- run_id: `20260517_004516_windows_cuda_100_step_mixed_domain_bpe_training`
- device: `cuda`
- hardware target: `windows_cuda`
- max_steps: `100`
- eval_interval: `10`
- train docs: `52`
- val docs: `5`
- train source_category counts: `{"external_general_text": 11, "synthetic_examples": 41}`
- val source_category counts: `{"external_general_text": 1, "synthetic_examples": 4}`
- tokenizer vocab size: `8192`

## 3. Observed Result
Key results:
- first_train_loss: `9.161793`
- final_train_loss: `3.796839`
- final_val_loss: `7.833482`
- loss_all_finite: `true`
- val_loss_all_finite: `true`
- checkpoint reload match: `true`
- metrics rows: `100`
- validation rows: `10`

Artifact directory:
- `experiments/windows_cuda/20260517_004516_windows_cuda_100_step_mixed_domain_bpe_training/`

Generated run artifacts include:
- `run_config.json`
- `run_metadata.json`
- `metrics.jsonl`
- `summary.md`
- `summary.json`
- `checkpoint_final.pt`

## 4. Interpretation
This run confirms that the mixed/domain BPE path can complete a strictly bounded 100-step local training loop with periodic validation, visible mixed-corpus provenance counts, and a successful checkpoint reload sanity check while keeping `external_general_text` supplement only.

Relative to the accepted D16.1 50-step baseline, train loss decreased further from `4.809736` to `3.796839` while final val loss increased from `7.669892` to `7.833482`.
This should be treated as the expected small-corpus overfitting signal described in D16.3, not as a broad model-quality result.

The result should be interpreted as bounded small training on the approved mixed/domain corpus.
It is not formal large-scale pretraining and does not support broad model-quality or generalization claims.

## 5. What It Does Not Claim
This step does not claim:
- meaningful downstream model quality
- external-data generalization
- production readiness
- large-scale pretraining completion
- A100 or 1.5B-scale validation
- generation-quality results

## 6. Next Step
Recommended next step:
- D16.5 review the bounded 100-step mixed/domain BPE training artifacts before any longer or non-local run
