# MVP-22.S Modal 2GB 1000-Step vs 3000-Step Comparison

## Side-by-Side Table

| field | 1000-step | 3000-step | interpretation |
|---|---:|---:|---|
| config | `fineweb_edu_2gb_300m_1000step_public16k_execute` | `fineweb_edu_2gb_300m_3000step_public16k_execute` | same 2GB prepared corpus route |
| backend/GPU | Modal / `NVIDIA A100-SXM4-40GB` | Modal / `NVIDIA A100-SXM4-40GB` | same backend class |
| data_loading_mode | `streaming` | `streaming` | same host-RAM-safe path |
| batch_size | `8` | `8` | unchanged |
| gradient_accumulation_steps | `4` | `4` | unchanged |
| max_steps | `1000` | `3000` | 3x more optimizer steps |
| first_train_loss | `9.864925` | `9.864925` | same initial setup signal |
| final_train_loss | `3.008913` | `3.156151` | both finite; not a monotonic quality claim |
| final_val_loss | `9.012106` | `9.043165` | no clear validation improvement |
| metrics_rows | `1000` | `3000` | expected row counts passed |
| validation_rows | `10` | `10` | eval cadence differs but both produced 10 validation rows |
| tokens_seen | `16384000` | `49152000` | exactly 3x tokens_seen |
| elapsed_seconds | `346.31222` | `1043.828751` | approximately linear with step count |
| approximate_tokens_per_sec | `47309.910177` | `47088.183726` | throughput stayed stable |
| checkpoint_reload_match | `true` | `true` | checkpoint reload path passed both times |
| post_run_artifact_validation | `passed` | `passed` | result artifact checks passed both times |

## Loss Curve Interpretation Based on Final Metrics

Both runs show finite train loss, finite validation loss, and finite gradients. That is good training-systems evidence.

The 3000-step run does not show a clear final-validation-loss improvement over the 1000-step run: `9.043165` versus `9.012106`. This should not be overinterpreted as regression either, because the validation sample is bounded and this stage is not designed as a model-quality benchmark. The right conclusion is narrower: longer 2GB training remained stable, but did not produce a compelling validation-loss reason to keep extending the same 2GB setup by default.

## Throughput Comparison

The 1000-step run processed `16384000` tokens in `346.31222` seconds, about `47309.910177` tokens/sec. The 3000-step run processed `49152000` tokens in `1043.828751` seconds, about `47088.183726` tokens/sec.

Throughput stayed close across the two runs, which supports Modal A100-40GB as a predictable backend for this streaming configuration.

## What Increased Step Count Proved

Increasing from 1000 to 3000 steps proved:

- the Modal backend can sustain a longer bounded run;
- the streaming iterator can feed `12000` train microbatches plus validation batches without host-RAM precompute;
- metrics logging scales to 3000 rows;
- checkpoint reload still passes at the 3000-step checkpoint;
- post-run and import validation remain clean.

## What It Did Not Prove

Increasing step count did not prove:

- model quality;
- generalization;
- downstream task performance;
- that 2GB 5000-step is the best next use of GPU budget;
- that scheduler behavior is correct, because scheduler config remains present but not applied;
- that bounded-prefix sampling is sufficient for quality-oriented claims.

## Decision Implication

The 3000-step result is enough to validate the longer Modal 2GB systems path. The next default should be either scheduler/sampling cleanup or 5GB 1000-step preflight, not automatically 2GB 5000-step.
