# D11 Domain BPE Small Training Plan

## 1. Purpose
The purpose of D11 is to define the first bounded small-training plan for the domain BPE path built on the refreshed 45-file synthetic expanded corpus.

This step is planning only.
It does not implement or run training.

## 2. Current Baseline
Current observed baseline:
- processed docs = `45`
- train docs = `41`
- val docs = `4`
- domain BPE vocab size = `3988`
- D10 loss = `8.434178`
- D10 forward/loss smoke passed

These values define the starting point for the first domain-BPE bounded local training step.

## 3. Training Scope
Recommended first bounded run:
- local GPU first
- domain synthetic corpus only
- tokenizer: `tokenizers/educode_bpe_domain_8k/`
- vocab_size = `3988`
- tiny dense decoder-only model
- max_steps = `50`
- eval_interval = `10`
- train loss + val loss
- final checkpoint
- checkpoint reload check
- metrics + summary

The goal is to validate the repeated local training path for the domain BPE artifact without changing corpus scope, hardware class, or model family.

## 4. Success Criteria
- train loss finite
- val loss finite
- checkpoint reload match
- metrics rows = `50`
- validation rows = `5`

Meeting these criteria would confirm that the domain-BPE local training path is bounded, reproducible, and structurally sound.

## 5. Guardrails
This step must preserve the following guardrails:
- not full pretraining
- not A100 by default
- not 1.5B
- no model quality claim
- no external data

These guardrails keep the next training step interpretable as local pipeline validation rather than a broader capability claim.

## 6. Planned Follow-up Step
A follow-up D11.1 step can create a bounded 50-step domain BPE training run that:
- loads the domain BPE smoke config or a closely aligned bounded training config
- uses the processed `synthetic_expanded` train/val splits only
- evaluates every `10` steps
- saves a final checkpoint under ignored experiment outputs
- reloads the checkpoint and verifies parameter/state consistency
- writes metrics and a markdown summary

## 7. What D11 Does Not Do
D11 does not:
- implement the training script
- run training
- train a tokenizer
- modify model code
- download data
- enter A100 by default

## 8. Next Step
Recommended next step:
- D11.1 50-step domain BPE small training run
