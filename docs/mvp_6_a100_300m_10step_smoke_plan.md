# MVP-6 A100 300M 10-step Smoke Plan

## 1. Purpose
The purpose of MVP-6 is to prepare the A100-side planning package for a future FineWeb-Edu `50MB` short training smoke using the existing mixed-domain `8k` tokenizer, without entering an A100 machine and without running training in this step.

MVP-6 creates a config draft, a preflight script, a transfer checklist, and a result-handoff plan only.

## 2. Why 300M First
A `300M`-class smoke is the next reasonable scale step because:
- it is substantially closer to the intended A100 workflow than the local tiny-model smoke path
- it remains small enough for a bounded `10-step` chain validation
- it allows training-path checks such as environment readiness, bf16 suitability, data loading, tokenizer compatibility, logging, and checkpoint policy to be validated before any larger run is attempted

This is a short training-chain validation target, not a model-quality target.

## 3. Input Corpus
Planned input corpus artifacts:
- `data/public_corpus/fineweb_edu_sample10bt_50mb/splits/fineweb_edu_50mb.train.jsonl`
- `data/public_corpus/fineweb_edu_sample10bt_50mb/splits/fineweb_edu_50mb.val.jsonl`

These remain local artifacts in MVP-6 and are not committed in this step.

## 4. Tokenizer Choice
Tokenizer reused for the planned smoke:
- `tokenizers/educode_bpe_mixed_domain_8k/tokenizer.json`

Reason:
- MVP-5 already validated the FineWeb-Edu public-corpus smoke path against the mixed-domain tokenizer with finite loss
- MVP-6 keeps the shortest path to an A100 smoke without detouring into tokenizer retraining

## 5. Config Path
Config draft created:
- `configs/a100/fineweb_edu_50mb_300m_10step_smoke.json`

Key draft properties:
- `model_size_label=300m`
- `sequence_length=512`
- `batch_size=8`
- `gradient_accumulation_steps=4`
- `max_steps=10`
- `eval_interval=5`
- `checkpoint_interval=10`
- `expected_gpu=A100`
- `precision=bf16_if_available_else_fp16`
- `output_dir=experiments/a100/fineweb_edu_50mb_300m_10step_smoke`

## 6. Expected A100 Environment
Expected future execution environment:
- single `A100` GPU
- CUDA visible via `nvidia-smi`
- `torch.cuda.is_available()` returns `True`
- bf16 support checked and recorded
- repo synced to the intended commit
- tokenizer artifact and public corpus split files available on the target machine

## 7. Preflight Command
Preflight script created:
- `scripts/preflight_a100_fineweb_edu_smoke.py`

Future preflight command:

```text
python scripts/preflight_a100_fineweb_edu_smoke.py --config configs/a100/fineweb_edu_50mb_300m_10step_smoke.json
```

This script is not executed as an A100 result in MVP-6.

## 8. Training Command Placeholder
Future training command placeholder:

```text
python scripts/run_a100_300m_fineweb_edu_10step_training.py --config configs/a100/fineweb_edu_50mb_300m_10step_smoke.json
```

That script is only a placeholder reference in MVP-6 and is not created in this step.

## 9. Expected Outputs
Expected future outputs from a real A100 smoke session:
- small run summary JSON
- `metrics.jsonl`
- compact logs
- optional checkpoint artifacts under the configured experiment directory

Checkpoint artifacts must not be committed by default.

## 10. Stop Conditions
Stop the future A100 smoke attempt if any of the following occurs:
- `torch.cuda.is_available()` is `False`
- `nvidia-smi` does not show an `A100`
- tokenizer path is missing
- FineWeb-Edu train/val split files are missing
- tokenizer vocab size does not match `8192`
- config validation fails
- output directory escapes `experiments/a100/`
- unexpected dirty git state exists before the run

## 11. Artifact Policy
Artifact policy for MVP-6 and the planned A100 smoke:
- MVP-6 does not enter A100
- MVP-6 does not run training
- `raw.jsonl` is not committed
- `processed/` and `splits/` remain local artifacts and are not committed in this step
- `experiments/` outputs remain ignored by git
- checkpoints are not committed by default
- summarized results may be copied back later after review

## 12. What MVP-6 Does Not Do
MVP-6 does not:
- enter A100
- run training
- train a tokenizer
- train a model
- claim model quality
- implement the future A100 training loop

The planned `10-step` smoke is only intended to validate the training chain on A100 once that environment is actually used.

## 13. Next Step
Recommended next step:
- prepare MVP-7 to implement or adapt the actual A100 FineWeb-Edu `10-step` training script, or execute the existing preflight on the target A100 machine once access is ready.
