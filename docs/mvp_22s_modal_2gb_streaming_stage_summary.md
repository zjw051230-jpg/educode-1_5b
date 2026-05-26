# MVP-22.S Modal 2GB Streaming Stage Summary

## 1. Purpose

Summarize the Modal A100 backend results for the 2GB prepared-corpus public16k streaming training stage, covering the imported 1000-step and 3000-step runs.

This stage summary is a systems-readiness and cost-decision document. It does not make model-quality claims.

## 2. Runs Reviewed

| milestone | run | report | imported summary |
|---|---|---|---|
| MVP-21.R | Modal A100 2GB 1000-step | `docs/mvp_21_modal_a100_2gb_1000step_streaming_run.md` | `experiments/a100/fineweb_edu_2gb_300m_1000step_public16k_execute/results_imported_modal_streaming/summary.json` |
| MVP-22.R | Modal A100 2GB 3000-step | `docs/mvp_22_modal_a100_2gb_3000step_streaming_run.md` | `experiments/a100/fineweb_edu_2gb_300m_3000step_public16k_execute/results_imported_modal_streaming/summary.json` |

Both runs completed on Modal and were imported locally as small result artifacts.

## 3. Common Setup

| field | value |
|---|---|
| backend | Modal |
| GPU | `NVIDIA A100-SXM4-40GB` |
| requested GPU | `A100-40GB` |
| Modal Volume | `educode-data` |
| prepared package | `/vol/prepared/fineweb_edu_2gb_prepared_splits.tar.gz` |
| GPU-worker Hugging Face fetch | no |
| data_loading_mode | `streaming` |
| batch_size | `8` |
| gradient_accumulation_steps | `4` |
| sequence_length | `512` |
| tokenizer_vocab_size | `16384` |
| parameter_count | `336106496` |
| runtime_device | `cuda` |
| runtime_dtype | `bf16` |

The prepared corpus package was uploaded before training. Modal GPU workers consumed the prepared train/val splits from Volume and did not fetch Hugging Face data during the paid GPU job.

## 4. Result Table

| field | 1000-step | 3000-step |
|---|---:|---:|
| max_steps | `1000` | `3000` |
| run_id | `20260526_162737_fineweb_edu_2gb_300m_1000step_public16k_execute` | `20260526_165916_fineweb_edu_2gb_300m_3000step_public16k_execute` |
| first_train_loss | `9.864925` | `9.864925` |
| final_train_loss | `3.008913` | `3.156151` |
| final_val_loss | `9.012106` | `9.043165` |
| metrics_rows | `1000` | `3000` |
| validation_rows | `10` | `10` |
| tokens_seen | `16384000` | `49152000` |
| checkpoint_reload_match | `true` | `true` |
| post_run_artifact_validation | `passed` | `passed` |
| elapsed_seconds | `346.31222` | `1043.828751` |
| approximate_tokens_per_sec | `47309.910177` | `47088.183726` |

## 5. Interpretation

Both runs prove that the Modal backend, prepared-data package logistics, and streaming training path are working for the 2GB public16k route.

The 3000-step run increased `tokens_seen` from `16384000` to `49152000`, exactly 3x the 1000-step run. The runtime scaled approximately linearly: `346.31222` seconds for 1000 steps and `1043.828751` seconds for 3000 steps. Throughput stayed close, moving from about `47309.91` tokens/sec to `47088.18` tokens/sec.

Checkpoint reload and post-run artifact validation passed for both runs. The imported local validators also passed with blocker count `0` for both result packages.

This should not be interpreted as a model-quality result. The final validation loss did not clearly improve: `9.012106` at 1000 steps versus `9.043165` at 3000 steps. The difference is small and should be treated cautiously, but it does not support blindly extending 2GB step count as the default next action.

Two caveats remain important:

- `scheduler_config_present_but_not_applied` is still present in the training summary.
- `bounded_prefix_batches_only` remains true, so these are bounded-prefix systems runs rather than broad corpus-quality experiments.

## 6. Artifact Policy

- Checkpoints were produced remotely for reload validation, but were not downloaded and were not committed.
- `raw.jsonl`, `processed/`, and `splits/` were not committed.
- Result transfer tarballs were not committed.
- Imported small artifacts were committed under controlled `results_imported_modal_streaming/` directories.
- Modal Volume can retain the prepared package and result packages, but retained Volume data continues to incur low storage cost until deleted.

## 7. Conclusion

Modal can be used as a backup or primary A100 execution backend for prepared-data streaming runs. The 2GB 1000-step and 3000-step results establish the remote execution chain for this project.

The next step should not blindly extend 2GB step count. The next decision should weigh:

1. 2GB 5000-step as an optional stability extension.
2. 5GB 1000-step as a more meaningful data-scale step.
3. Scheduler and sampling cleanup before additional quality-oriented claims.

Recommended direction: do local scheduler/sampling cleanup planning or implementation first, then use Modal for 5GB 1000-step preflight and training only after explicit cost approval.
