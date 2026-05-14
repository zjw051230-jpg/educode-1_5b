# D6.3 100-Step Expanded BPE Training Plan

## 1. Purpose
The purpose of D6.3 is to define the next bounded local training increment for the expanded synthetic corpus path after the accepted D6.1 50-step run and the D6.2 review.

This step is planning only.
It does not run training, does not retrain the tokenizer, and does not change model or training code.

## 2. Current Baseline from D6.1 / D6.2
Current accepted baseline:
- reviewed run_id: `20260515_014657_windows_cuda_50_step_expanded_bpe_training`
- corpus scope: expanded synthetic corpus only
- tokenizer: `tokenizers/educode_bpe_expanded_8k/`
- observed tokenizer vocab size: `1846`
- train docs: `13`
- val docs: `2`
- max_steps completed: `50`
- eval_interval used: `10`
- first_train_loss: `7.633180`
- final_train_loss: `4.182922`
- final_val_loss: `7.184383`
- metrics rows: `50`
- validation rows: `5`
- checkpoint reload match: `True`
- D6.1 status after D6.2 review: accepted

## 3. Why 100-Step Is the Next Safe Increment
A bounded `100`-step run is the next safe increment because it extends the same already-accepted local training path without changing any major variable.

What stays fixed:
- same local GPU path
- same expanded synthetic corpus split files
- same expanded BPE tokenizer artifact
- same tiny decoder-only model path
- same periodic validation cadence
- same checkpoint and summary expectations

What changes:
- only the bounded step budget increases from `50` to `100`

This keeps the next stage reviewable while giving a slightly longer optimization window and more repeated validation points than D6.1.

## 4. Training Scope
Recommended D6.4 run scope:
- local GPU
- expanded synthetic corpus only
- expanded BPE tokenizer only
- vocab_size = `1846`
- max_steps = `100`
- eval_interval = `10`
- train_loss + val_loss
- final checkpoint
- checkpoint reload
- metrics + summary

This scope should remain aligned with the existing bounded expanded-BPE training path and should not broaden into a new hardware, tokenizer, data, or model milestone.

## 5. Success Criteria
D6.4 should be treated as successful only if all of the following hold:
- train loss finite
- val loss finite
- checkpoint reload match
- metrics rows = `100`
- validation rows = `10`

Additional expected checks:
- required run artifacts are written under ignored `experiments/`
- no external data is introduced
- no model quality claim is made from the bounded run metrics

## 6. Guardrails
The next step must preserve the following guardrails:
- not full pretraining
- not A100 by default
- not 1.5B
- no model quality claim

Additional practical guardrails:
- no tokenizer retraining in this step
- no corpus expansion in this step
- no model-code changes in this step
- no long-run or non-local scope jump without a separate approved milestone

## 7. Next Step
Recommended next step:
- D6.4 100-step expanded BPE training run
