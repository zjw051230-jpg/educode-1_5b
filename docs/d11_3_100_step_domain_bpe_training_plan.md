# D11.3 100-Step Domain BPE Training Plan

## 1. Purpose
The purpose of D11.3 is to define the next bounded local training increment for the domain BPE path after the accepted D11.1 50-step run and the D11.2 review.

This step is planning only.
It does not run training, does not retrain the tokenizer, and does not change model or training code.

## 2. Current Baseline from D11.1 / D11.2
Current accepted baseline:
- reviewed run_id: `20260515_034606_windows_cuda_50_step_domain_bpe_training`
- corpus scope: domain synthetic corpus only
- tokenizer: `tokenizers/educode_bpe_domain_8k/`
- observed tokenizer vocab size: `3988`
- train docs: `41`
- val docs: `4`
- max_steps completed: `50`
- eval_interval used: `10`
- first_train_loss: `8.485050`
- final_train_loss: `4.463557`
- final_val_loss: `7.506592`
- metrics rows: `50`
- validation rows: `5`
- checkpoint reload match: `True`
- D11.1 status after D11.2 review: accepted

## 3. Why 100-Step Is the Next Safe Increment
A bounded `100`-step run is the next safe increment because it extends the same already-accepted local training path without changing any major variable.

What stays fixed:
- same local GPU path
- same domain synthetic corpus split files
- same domain BPE tokenizer artifact
- same tiny decoder-only model path
- same periodic validation cadence
- same checkpoint and summary expectations

What changes:
- only the bounded step budget increases from `50` to `100`

This keeps the next stage reviewable while providing a longer optimization window and more repeated validation points than D11.1.

## 4. Training Scope
Recommended D11.4 run scope:
- local GPU
- domain synthetic corpus only
- domain BPE tokenizer only
- vocab_size = `3988`
- max_steps = `100`
- eval_interval = `10`
- train_loss + val_loss
- final checkpoint
- checkpoint reload
- metrics + summary

This scope should remain aligned with the existing bounded domain-BPE training path and should not broaden into a new hardware, tokenizer, data, or model milestone.

## 5. Success Criteria
D11.4 should be treated as successful only if all of the following hold:
- train loss finite
- val loss finite
- checkpoint reload match
- metrics rows = `100`
- validation rows = `10`

## 6. Guardrails
The next step must preserve the following guardrails:
- not full pretraining
- not A100 by default
- not 1.5B
- no model quality claim
- no external data

## 7. Next Step
Recommended next step:
- D11.4 100-step domain BPE training run
