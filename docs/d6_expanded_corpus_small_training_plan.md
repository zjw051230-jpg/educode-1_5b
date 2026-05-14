# D6 Expanded Corpus Small Training Plan

## 1. Purpose
Plan the first bounded small training run on the expanded synthetic corpus and the expanded BPE tokenizer.

## 2. Current Baseline
Current observed baseline:
- expanded synthetic corpus files = `15`
- processed docs = `15`
- train docs = `13`
- val docs = `2`
- expanded BPE observed vocab = `1846`
- D5 forward/loss smoke passed
- D5 loss = `7.641596`
- A100 smoke milestone already validated the scaling path up to 2.15B, but current D6 should remain local and bounded unless explicitly approved

## 3. Training Scope
Recommended first bounded run:
- local GPU first
- expanded synthetic corpus only
- tokenizer: `tokenizers/educode_bpe_expanded_8k/`
- vocab_size = `1846`
- tiny dense decoder-only model
- max_steps = `50`
- eval_interval = `10`
- train loss + val loss
- final checkpoint
- checkpoint reload check
- summary + metrics
- no A100 unless separately approved

## 4. Success Criteria
- train loss finite
- val loss finite
- checkpoint reload works
- metrics rows = `50`
- validation rows = `5`
- no claim of model quality
- no external data involved

## 5. Guardrails
This step must preserve the following guardrails:
- not full pretraining
- not A100 by default
- not 1.5B
- not external corpus
- not production tokenizer
- do not compare results as meaningful model quality

## 6. Planned Script
A follow-up D6.1 step can create:
- `scripts/run_50_step_expanded_bpe_training.py`

That script should:
- load `configs/windows/bpe_expanded_8k_smoke.json`
- load the expanded tokenizer
- load synthetic_expanded train/val JSONL
- train for `50` steps
- eval every `10` steps
- save the final checkpoint under ignored `experiments/`
- reload the checkpoint
- write `metrics.jsonl` and `summary`

## 7. What D6 Does Not Do
D6 does not:
- implement the training script
- run training
- enter A100
- download data
- train a tokenizer

## 8. Next Step
D6.1: 50-step expanded BPE small training run
