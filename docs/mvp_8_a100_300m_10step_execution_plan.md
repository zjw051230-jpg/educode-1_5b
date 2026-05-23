# MVP-8 A100 FineWeb-Edu 300M 10-step Execution Plan

## 1. Purpose
The purpose of MVP-8 is to define the next approved execution procedure for the real A100 FineWeb-Edu `300M` `10-step` smoke after MVP-7 implemented and locally dry-ran the script.

MVP-8 is still planning-only.
It does not enter A100 or run training in this document step.

## 2. Inputs Required
Required inputs for the future execution step:
- `configs/a100/fineweb_edu_50mb_300m_10step_smoke.json`
- `scripts/run_a100_300m_fineweb_edu_10step_training.py`
- `scripts/preflight_a100_fineweb_edu_smoke.py`
- `tokenizers/educode_bpe_mixed_domain_8k/tokenizer.json`
- `data/public_corpus/fineweb_edu_sample10bt_50mb/splits/fineweb_edu_50mb.train.jsonl`
- `data/public_corpus/fineweb_edu_sample10bt_50mb/splits/fineweb_edu_50mb.val.jsonl`

## 3. Important Execution Gate
Before the real A100 smoke is allowed, explicitly review the current config safety field:
- `training.no_training=true`

That field must remain `true` during planning and local dry-run work.
It should only be changed for the actual A100 execution step after the operator is ready to run the smoke intentionally.

## 4. Preflight Order
Recommended future A100-side order:
1. confirm machine identity and CUDA visibility
2. confirm the repo is on the intended commit
3. confirm tokenizer and public-corpus split files exist
4. run the preflight script
5. review `preflight_summary.json`
6. only then enable the real smoke run

Recommended commands:

```text
nvidia-smi
python --version
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available()); print(torch.cuda.device_count()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'no cuda'); print(torch.version.cuda)"
python scripts/preflight_a100_fineweb_edu_smoke.py --config configs/a100/fineweb_edu_50mb_300m_10step_smoke.json
```

## 5. Real Smoke Enablement
Before the real smoke command, review and intentionally flip:
- `training.no_training: true -> false`

Do not reuse an unreviewed edited config.
Prefer either:
- a reviewed A100 execution-only config copy, or
- a deliberate one-line config edit made only on the A100 machine for the approved smoke session

## 6. Future Smoke Command
Expected future command after preflight passes and the config is intentionally unblocked:

```text
python scripts/run_a100_300m_fineweb_edu_10step_training.py --config configs/a100/fineweb_edu_50mb_300m_10step_smoke.json
```

## 7. Expected Outputs
Expected future output directory:
- `experiments/a100/fineweb_edu_50mb_300m_10step_smoke/`

Expected reviewed artifacts:
- `run_config.json`
- `run_metadata.json`
- `metrics.jsonl`
- `summary.json`
- `summary.md`
- `checkpoints_manifest.json`
- checkpoint file under the configured checkpoint directory

## 8. Important Interpretation Boundary
Even after the future A100 smoke runs, the result should still be interpreted as:
- a bounded training-chain validation
- not formal pretraining
- not a quality benchmark
- not proof that all draft config architecture fields are implemented in core model code

In particular, MVP-7 already recorded that the current core model path does not yet have full declared-feature parity with the draft config because learned position embeddings are still used instead of true RoPE.

## 9. Stop Conditions
Stop the future A100 smoke immediately if:
- `torch.cuda.is_available()` is `False`
- GPU name is not an `A100`
- tokenizer path is missing
- train/val split files are missing
- tokenizer vocab size is not `8192`
- config validation fails
- output directory escapes `experiments/a100/`
- `training.no_training` was not intentionally reviewed before execution
- the dry-run/summary contract no longer matches the current script or config

## 10. Copy-back Policy
Copy back only the small reviewed artifacts by default:
- `summary.json`
- `summary.md`
- `metrics.jsonl`
- `run_metadata.json`
- `preflight_summary.json`
- `checkpoints_manifest.json`

Do not copy back large checkpoints unless a later reviewed step explicitly asks for them.

## 11. Next Step
Recommended next step:
- perform the real A100 session only after access is ready and after an explicit reviewed decision on how to flip `training.no_training=false` for that single execution step
