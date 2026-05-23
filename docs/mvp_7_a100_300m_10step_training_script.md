# MVP-7 A100 FineWeb-Edu 300M 10-step Training Script

## 1. Purpose
The purpose of MVP-7 is to implement the future A100 FineWeb-Edu `300M` `10-step` smoke script while keeping this step local, bounded, and dry-run-first.

This step does not run real training.
It implements the script, validates the dry-run path, and records the current compatibility boundary between the A100 smoke config and the existing core model implementation.

## 2. Script Created
Script created:
- `scripts/run_a100_300m_fineweb_edu_10step_training.py`

Supported CLI:

```text
.venv/Scripts/python.exe scripts/run_a100_300m_fineweb_edu_10step_training.py --config configs/a100/fineweb_edu_50mb_300m_10step_smoke.json --dry-run
```

The same script also contains the future non-dry-run path, but that path remains blocked by the current config-level `training.no_training=true` safety gate in this step.

## 3. Reused Building Blocks
MVP-7 reuses the existing script-layer training pipeline rather than modifying core model code:
- `educode.config_loader.load_json_config`
- `educode.config_validator.validate_config`
- `educode.sequence_dataset.make_next_token_samples`
- `educode.sequence_dataset.batch_samples`
- `educode.losses.next_token_cross_entropy`
- `educode.checkpoint.save_checkpoint`
- `educode.checkpoint.load_checkpoint`
- `educode.checkpoint.compare_model_parameters`
- `educode.run_logging.write_metrics_record`
- `educode.run_logging.build_summary_markdown`
- `educode.run_setup.make_run_id`
- `educode.run_setup.snapshot_config`
- `educode.run_setup.write_run_metadata`

This keeps MVP-7 inside the existing repo contract and avoids core-model churn.

## 4. Dry-run Responsibilities
The new `--dry-run` path now verifies:
- config validation
- tokenizer-path existence and vocab-size match
- FineWeb-Edu train/val split existence
- bounded train/val JSONL probing using the existing mixed-domain `8k` tokenizer
- exact parameter counting for the configured `300M`-class model
- attempted local model materialization
- explicit recording of `memory_limited_local_dry_run` if local materialization fails for memory reasons
- explicit recording of declared-config features versus currently implemented core-model features

The dry-run does not:
- run forward
- run backward
- build an optimizer
- save a checkpoint
- run training
- enter A100

## 5. Dry-run Observed Result
Observed local dry-run result:
- `runtime_device=cuda`
- `runtime_dtype=bf16`
- `tokenizer_vocab_size=8192`
- `exact_parameter_count=319329280`
- `model_materialized_locally=true`
- `memory_limited_local_dry_run=false`
- `core_model_feature_parity=false`

Dry-run artifact written:
- `experiments/a100/fineweb_edu_50mb_300m_10step_smoke/dry_run_summary.json`

This confirms that the current repo can validate the A100 smoke config, tokenizer, bounded public-corpus batch formation, and 300M-class parameter scale locally without entering a real A100 session.

## 6. Important Compatibility Note
MVP-7 intentionally does not modify `src/educode/tiny_model.py`.

That means the script currently executes against the existing core model implementation, which is effectively:
- RMSNorm
- SwiGLU
- SDPA attention
- learned position embeddings
- untied embeddings

The current A100 draft config still declares fields such as:
- `position_encoding=rope`
- `norm_type=rmsnorm`
- `ffn_type=swiglu`

Because the core model still uses learned position embeddings rather than RoPE, the dry-run truthfully records `core_model_feature_parity=false` instead of pretending the config has already been fully implemented at the core-model layer.

## 7. Training-path Boundary
The script contains a future non-dry-run path for the actual `10-step` smoke, including:
- bounded prefix-batch loading from the FineWeb-Edu train/val JSONL splits
- gradient accumulation
- periodic validation
- metrics logging
- checkpoint save/load sanity check
- summary JSON / markdown output

However, MVP-7 keeps the current config blocked for execution via:
- `training.no_training=true`

That gate prevents accidental local non-dry-run execution in this step.

## 8. What MVP-7 Does Not Do
MVP-7 does not:
- enter A100
- run real training
- train a tokenizer
- retrain or replace the mixed-domain `8k` tokenizer
- modify core model code
- claim RoPE support has been validated
- claim model quality
- commit checkpoints
- commit `processed/` or `splits/` local artifacts

## 9. Next Step
Recommended next step:
- use MVP-8 to prepare the approved A100-side execution procedure, including a reviewed execution config or explicit config toggle for `training.no_training=false` only at the real execution stage
