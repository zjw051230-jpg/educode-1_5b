# T7.3 Bounded 100-Step Small Training Plan

## 1. Purpose
The purpose of T7.3 is to define the next bounded small-training increment after the accepted 50-step T7.1/T7.2 result.

This step is planning only.
It does not run training, does not modify the training script, and does not change the model or tokenizer path.

## 2. Current Baseline from T7.1/T7.2
Current accepted baseline:
- reviewed run_id: `20260514_024451_windows_cuda_50_step_small_real_data_training`
- synthetic seed corpus only
- linked BPE tokenizer vocab size: `1174`
- same tiny dense decoder-only model path
- `max_steps = 50`
- `eval_interval = 10`
- train loss decreased from `7.192344` to `4.074500`
- final val loss: `7.380465`
- `metrics.jsonl` rows: `50`
- validation rows: `5`
- checkpoint reload match: `True`
- T7.1 accepted in T7.2 review

## 3. Why 100-Step Is the Next Safe Increment
A bounded 100-step run is the next safe increment because it changes only one main variable relative to the accepted baseline: training length.

This keeps the following fixed:
- same synthetic-seed-only corpus path
- same BPE tokenizer artifact
- same tiny dense model path
- same local Windows GPU path
- same evaluation cadence
- same artifact expectations

That makes the follow-up run easier to compare against T7.1 without introducing new ambiguity from multiple simultaneous changes.

## 4. Training Scope
The future bounded 100-step run should use:
- synthetic seed corpus only
- BPE vocab size `1174`
- same tiny dense model
- `max_steps = 100`
- `eval_interval = 10`
- final checkpoint save
- final generation sample
- structured metrics logging plus summary output

Expected artifact set:
- `run_metadata.json`
- `run_config.json`
- `metrics.jsonl`
- `generation_samples.jsonl`
- `summary.md`
- `checkpoint_final.pt`
- checkpoint manifest output

## 5. Success Criteria
Success criteria for the bounded 100-step stage:
- train loss is finite
- val loss is finite
- no CUDA OOM occurs
- checkpoint reload match is `True`
- `metrics.jsonl` rows = `100`
- validation rows = `10`

## 6. Guardrails
Guardrails for this stage:
- not A100/B200
- not 1.5B
- not real external corpus
- no quality claim

Additional interpretation guardrails:
- the corpus remains synthetic and tiny
- the validation split remains too small for strong generalization claims
- any generation output remains a pipeline sanity check, not a model-quality result

## 7. Next Step
Recommended next step:
- T7.4 bounded 100-step small training run
