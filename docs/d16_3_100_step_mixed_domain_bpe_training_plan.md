# D16.3 100-Step Mixed/Domain BPE Training Plan

## 1. Purpose
The purpose of D16.3 is to define the next bounded local training increment for the mixed/domain BPE path after the accepted D16.1 50-step run and the D16.2 review.

This step is planning only.
It does not run training, does not retrain the tokenizer, and does not change model or training code.

## 2. Current Baseline from D16.1 / D16.2
Current accepted baseline:
- reviewed run_id: `20260517_000844_windows_cuda_50_step_mixed_domain_bpe_training`
- corpus scope: `mixed_domain_external` only
- tokenizer: `tokenizers/educode_bpe_mixed_domain_8k/`
- vocab_size: `8192`
- train docs: `52`
- val docs: `5`
- max_steps completed: `50`
- eval_interval used: `10`
- first_train_loss: `9.161793`
- final_train_loss: `4.809736`
- final_val_loss: `7.669892`
- metrics rows: `50`
- validation rows: `5`
- checkpoint reload match: `True`
- train source_category counts: `{"external_general_text": 11, "synthetic_examples": 41}`
- val source_category counts: `{"external_general_text": 1, "synthetic_examples": 4}`
- D16.1 status after D16.2 review: accepted

## 3. Why 100-Step Is the Next Bounded Local Increment
A bounded `100`-step run is the next safe local increment because it extends the same already-accepted training path without changing any major variable.

What stays fixed:
- same local GPU path
- same `mixed_domain_external` split files
- same mixed/domain BPE tokenizer artifact
- same tiny decoder-only model path
- same periodic validation cadence
- same checkpoint and summary expectations
- same source-category reporting requirement

What changes:
- only the bounded step budget increases from `50` to `100`

This keeps the next stage reviewable while providing a longer optimization window and more repeated validation points than D16.1.

## 4. Training Scope
Recommended D16.4 run scope:
- local GPU
- `mixed_domain_external` corpus only
- mixed/domain BPE tokenizer only
- vocab_size = `8192`
- max_steps = `100`
- eval_interval = `10`
- train_loss + val_loss
- source_category counts recorded
- final checkpoint
- checkpoint reload
- metrics + summary

This scope should remain aligned with the existing bounded mixed-domain training path and should not broaden into a new hardware, tokenizer, data, or model milestone.

## 5. Success Criteria
D16.4 should be treated as successful only if all of the following hold:
- train loss finite
- val loss finite
- checkpoint reload match
- metrics rows = `100`
- validation rows = `10`
- source_category counts preserved

Additional expected checks:
- required run artifacts are written under ignored `experiments/`
- `external_general_text` remains supplement only in reporting and interpretation
- no model quality claim is made from the bounded run metrics

## 6. Guardrails
The next step must preserve the following guardrails:
- not full pretraining
- not A100 by default
- not 1.5B
- no model quality claim
- `external_general_text` remains supplement only

Additional practical guardrails:
- no tokenizer retraining in this step
- no data expansion in this step
- no model-code changes in this step
- no long-run or non-local scope jump without a separate approved milestone

## 7. Expected Interpretation
Expected review interpretation:
- if train loss continues to decrease while val loss rises, treat that as an overfitting signal on the current small mixed corpus
- do not continue increasing step count automatically without more approved data or a separately justified planning step
- finite losses and a passing checkpoint reload confirm bounded pipeline behavior, not broad capability or generalization

## 8. Next Step
Recommended next step:
- D16.4 100-step mixed/domain BPE training run
