# A2 A100 Mixed/Domain Training Plan

## 1. Purpose
The purpose of A2 is to plan the next A100 mixed/domain training path after the accepted local mixed/domain bounded runs and the D16.6 comparison.

This step is planning only.
It does not enter an A100 machine, does not rent GPU time, does not run training, and does not change model code.

A2 is not direct long training.
It is the plan for the next controlled A100 mixed/domain run ladder.

## 2. Current Baseline
Current accepted mixed/domain baseline:
- mixed/domain tokenizer vocab size = `8192`
- mixed corpus total docs = `57`
- train docs = `52`
- val docs = `5`
- synthetic docs = `45`
- external docs = `12`
- 50-step final_train_loss = `4.809736`
- 50-step final_val_loss = `7.669892`
- 100-step final_train_loss = `3.796839`
- 100-step final_val_loss = `7.833482`
- checkpoint reload passed in both runs
- overfitting signal exists on the current small mixed corpus

This means the local mixed/domain pipeline, checkpoint path, and provenance recording path have been validated, but the current small corpus is not a good justification for more local step-stacking.

## 3. Why A100 Planning Now
A100 planning is the correct next move because:
- the local mixed/domain pipeline has already been validated through bounded 50-step and 100-step runs
- the mixed/domain tokenizer path has reached the full observed vocab size `8192`
- the mixed corpus train/val chain has already been built and validated
- source-category provenance has been preserved across processing and training
- continuing to increase local step count is not appropriate on the current small mixed corpus
- the next useful question is whether mixed/domain configs, throughput, memory behavior, and checkpoint behavior stay healthy on A100 hardware

This planning step is for controlled A100 scale validation only.
It is not a claim about model quality, generalization, or formal pretraining readiness.

## 4. Recommended A100 Run Ladder
The recommended future A100 run ladder is staged and intentionally narrow.
Each stage should only be attempted if the previous one passes.

### A2.1 300M mixed/domain forward/loss smoke
Scope:
- no backward
- no checkpoint
- verify config, tokenizer, model, and loss
- use the `mixed_domain_external` train split

Goal:
- confirm that the A100 mixed/domain config loads correctly
- confirm that tokenizer and vocab-size alignment still hold
- confirm that forward/loss are finite on the A100 path
- record memory and basic step timing

### A2.2 300M mixed/domain 10-step training smoke
Scope:
- backward + optimizer
- no long training
- checkpoint optional or final-only
- record memory and step time

Goal:
- verify finite backward/optimizer behavior on A100
- confirm that a short mixed/domain training loop runs cleanly
- record step-time and memory behavior before any longer bounded run

### A2.3 300M mixed/domain 100-step bounded run
Scope:
- only if A2.2 passes
- eval every `10` steps
- checkpoint reload
- compare train/val loss

Goal:
- validate a controlled bounded A100 mixed/domain run with the same review discipline already used locally
- confirm checkpoint reload and structured metrics behavior on the A100 path
- check whether train/val behavior is still dominated by the small-corpus overfitting signal

### A2.4 2.15B mixed/domain short profile
Scope:
- short run only
- `seq_len = 256` or `512` depending memory
- no long run on the current tiny corpus
- no model quality claim

Goal:
- validate memory envelope and short-run systems behavior at the larger mixed/domain profile size
- confirm that the project can profile the larger target path without turning the current tiny mixed corpus into a misleading pseudo-pretraining milestone

## 5. Proposed First A100 Config
Recommended first config target:
- config path:
  `configs/a100/educode_300m_mixed_domain_draft.json`
- tokenizer:
  `tokenizers/educode_bpe_mixed_domain_8k/tokenizer.json`
- vocab_size = `8192`
- corpus:
  - `data/real_corpus/splits/mixed_domain_external.train.jsonl`
  - `data/real_corpus/splits/mixed_domain_external.val.jsonl`
- model target:
  about `300M` to `400M` parameters
- context_length:
  `512`
- batch_size:
  conservative first, for example `4`
- eval_interval:
  `10` for short runs
- max_steps:
  `10` for first training smoke, `100` for bounded run after approval

This first A100 config should remain focused on controlled validation.
It should not be treated as approval for a long training run.

## 6. Success Criteria
Success criteria for the future A100 mixed/domain line:
- config validates
- tokenizer loads
- vocab-size alignment passes
- source-category counts are recorded
- forward/loss are finite
- backward is finite for the training smoke
- checkpoint reload passes when a checkpoint is saved
- memory and step time are recorded
- no generation or model-quality claim is made

## 7. Guardrails
Guardrails for A2:
- A2 is not full pretraining
- A2 is not production model training
- A2 is not proof of model quality
- the current mixed corpus remains small
- `external_general_text` remains supplement only
- do not run 2.15B long training yet
- do not commit checkpoints
- do not upload secrets, tokens, or raw logs

## 8. A100 Artifact Policy
Artifact policy for the future A100 mixed/domain line:
- commit scripts, configs, and docs only
- keep checkpoints in ignored `experiments/`
- transfer only summary and metrics artifacts if needed
- do not commit `.pt`, `.pth`, or `.safetensors`
- write an A100 run summary after execution

## 9. Next Step
Recommended next step:
- A2.1 create the A100 300M mixed/domain config draft and validation script
