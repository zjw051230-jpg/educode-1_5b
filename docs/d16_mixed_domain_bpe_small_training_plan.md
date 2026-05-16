# D16 Mixed/Domain BPE Small Training Plan

## 1. Purpose
The purpose of D16 is to plan the first bounded small-training step on the approved `mixed_domain_external` corpus together with the mixed/domain BPE tokenizer artifact.

This step is planning only.
It does not implement or run training.

## 2. Current Baseline
Current observed baseline:
- mixed total docs = `57`
- train docs = `52`
- val docs = `5`
- synthetic docs = `45`
- external docs = `12`
- tokenizer vocab size = `8192`
- D15 data/model/loss smoke passed
- D15 loss = `9.161793`
- loss finite = `True`

These values define the starting point for the first bounded local mixed/domain BPE training step.

## 3. Project Backbone Constraint
The bounded mixed/domain training path must preserve the following project-level constraints:
- EduCode-1.5B remains a CS / ML / Python / Transformer training-systems educational domain model pipeline.
- `external_general_text` is supplement only.
- `source_category` must remain visible in reports.
- no broad model quality claim.

These constraints keep the mixed-domain path aligned with the project backbone rather than turning it into a general-language training claim.

## 4. Training Scope
Recommended first bounded run:
- local GPU first
- `mixed_domain_external` corpus only
- tokenizer: `tokenizers/educode_bpe_mixed_domain_8k/`
- vocab_size = `8192`
- tiny dense decoder-only model
- max_steps = `50`
- eval_interval = `10`
- train_loss + val_loss
- final checkpoint
- checkpoint reload check
- metrics + summary
- no A100 unless separately approved

The goal is to validate the repeated local training path for the mixed/domain BPE artifact without changing corpus scope, hardware class, or model family.

## 5. Success Criteria
- train loss finite
- val loss finite
- checkpoint reload match
- metrics rows = `50`
- validation rows = `5`
- `source_category` counts recorded
- no model quality claim

Meeting these criteria would confirm that the mixed/domain BPE local training path is bounded, reproducible, and structurally sound.

## 6. Guardrails
This step must preserve the following guardrails:
- not full pretraining
- not A100 by default
- not 1.5B
- no generation-quality claim
- no external data beyond approved Gutenberg supplement
- external text remains supplement only

These guardrails keep the next training step interpretable as local pipeline validation rather than a broader capability claim.

## 7. Planned Script
A follow-up D16.1 step can create:
- `scripts/run_50_step_mixed_domain_bpe_training.py`

That script should:
- load `configs/windows/bpe_mixed_domain_8k_smoke.json`
- load `tokenizers/educode_bpe_mixed_domain_8k/tokenizer.json`
- load mixed-domain train/val JSONL
- record `source_category` counts
- train for `50` steps
- evaluate every `10` steps
- save a final checkpoint under ignored `experiments/`
- reload the checkpoint
- write `metrics.jsonl` and `summary`

## 8. What D16 Does Not Do
D16 does not:
- implement the training script
- run training
- train a tokenizer
- enter A100
- download data

## 9. Next Step
Recommended next step:
- D16.1 50-step mixed/domain BPE small training run
