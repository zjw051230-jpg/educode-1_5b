# D16.1 50-Step Mixed/Domain BPE Training

## 1. Purpose
The purpose of D16.1 is to run the first bounded 50-step local small-training experiment on the approved mixed/domain BPE path built from the `mixed_domain_external` corpus.

This run is a local bounded validation step only.
It is not formal large-scale pretraining.

## 2. Run Overview
- run_id: `20260517_000844_windows_cuda_50_step_mixed_domain_bpe_training`
- device: `cuda`
- hardware target: `windows_cuda`
- max_steps: `50`
- eval_interval: `10`
- train docs: `52`
- val docs: `5`
- train source_category counts: `{"external_general_text": 11, "synthetic_examples": 41}`
- val source_category counts: `{"external_general_text": 1, "synthetic_examples": 4}`
- tokenizer vocab size: `8192`

## 3. Observed Result
Key results:
- first_train_loss: `9.161793`
- final_train_loss: `4.809736`
- final_val_loss: `7.669892`
- loss_all_finite: `true`
- val_loss_all_finite: `true`
- checkpoint reload match: `true`
- metrics rows: `50`
- validation rows: `5`

Artifact directory:
- `experiments/windows_cuda/20260517_000844_windows_cuda_50_step_mixed_domain_bpe_training/`

Generated run artifacts include:
- `run_config.json`
- `run_metadata.json`
- `metrics.jsonl`
- `summary.md`
- `summary.json`
- `checkpoint_final.pt`

## 4. Interpretation
This run confirms that the mixed/domain BPE path can complete a strictly bounded 50-step local training loop with periodic validation, visible mixed-corpus provenance counts, and a successful checkpoint reload sanity check.

The result should be interpreted as bounded small training on the approved mixed/domain corpus.
It is not formal large-scale pretraining and does not support broad model-quality claims.

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
- D16.2 review the bounded 50-step mixed/domain BPE training artifacts before any longer or non-local run
