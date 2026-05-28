# MVP-28.I SDPA Attention Profiling Mode

## Scope

This step implements the bounded profiling harness for the current SDPA attention baseline. It does not run Modal, does not request GPU, does not start training, does not install FlashAttention, and does not implement a FlashAttention backend.

## Why This Harness Is Needed

MVP-28.P found that the runtime attention path is already PyTorch SDPA in `src/educode/tiny_model.py`, while FlashAttention is not implemented. Before spending on longer training or new backend work, the project needs a small, repeatable profiling mode that can produce comparable throughput and memory artifacts on A100.

The harness separates systems profiling from model-quality training:

- short run length: `50` steps
- fixed current context length: `512`
- existing 300M-class model shape
- existing 5GB prepared streaming package
- explicit backend label: `sdpa`
- result package name includes `50step_sdpa_profile`

## Added Config

Config:

```text
configs/a100/fineweb_edu_5gb_300m_50step_public16k_sdpa_profile.json
```

Key settings:

| Field | Value |
| --- | --- |
| `training.max_steps` | `50` |
| `training.batch_size` | `8` |
| `training.gradient_accumulation_steps` | `4` |
| `training.sequence_length` | `512` |
| `data.data_loading_mode` | `streaming` |
| `sampling.policy` | `shuffle_buffer` |
| `validation_sampling.policy` | `shuffle_buffer` |
| `profiling.attention_backend` | `sdpa` |
| `profiling.record_tokens_per_sec` | `true` |
| `profiling.record_memory` | `true` |
| `profiling.record_mfu` | `true` |

This config is a profiling config, not a quality training config.

## Added Modal Mode

Mode:

```text
profile_5gb_50step_sdpa
```

Expected result package:

```text
/vol/results/mvp28_a100_5gb_50step_sdpa_profile_results.tar.gz
```

The mode uses the same prepared 5GB Modal Volume package as the prior 5GB training modes and writes only the standard small result package. Checkpoints may be created inside the remote output directory because the current training script validates checkpoint reload, but checkpoints and tarballs must not be committed to git.

## Why 50 Steps

Fifty steps is long enough to collect tokens/sec, step-time, memory, and loss-sanity rows, but short enough to keep cost and failure blast radius low. The goal is to validate the profiling path and establish a baseline, not to improve model quality.

## Profiling Metrics

The next run should inspect:

- tokens/sec
- step time
- GPU memory allocated/reserved
- MFU if available; current training metadata may still emit `null`
- train loss sanity
- validation sanity
- result package reproducibility

## Cost Boundary

This implementation step costs `0`: no Modal, no GPU, no training.

The next A100 50-step profiling run should be much cheaper than the 5GB 3000-step training run, but it still requires a separate approval/cost gate before execution.

## MVP-28.RUN First Attempt

The first `profile_5gb_50step_sdpa` Modal attempt did not complete. The app stopped during `scripts/check_a100_execution_readiness.py` before entering the 50-step training/profiling loop.

Failure cause:

- the readiness checker still treated every config as a traditional training execution config
- it only accepted `max_steps` values `1000`, `3000`, and `5000`
- it expected the traditional `*_execute` run name
- it did not recognize `*_sdpa_profile` as a bounded profiling config

No profiling result package was generated, and this document must not be read as evidence that profiling passed.

## MVP-28.FIX-001 Readiness Split

The readiness checker now separates two gate types:

- `training_execution`: unchanged gate for real training configs such as 5GB 3000-step
- `bounded_sdpa_profile`: explicit 50-step profiling gate for `profile_5gb_50step_sdpa`

The profiling gate is only enabled when the config is explicitly marked with `profiling.profile_mode=bounded_sdpa_profile`, `profiling.enabled=true`, `profiling.attention_backend=sdpa`, a `*_sdpa_profile` run name, and profiling status metadata. It does not relax the training execution gate.

The bounded profiling gate still requires:

- `max_steps=50`
- `data_loading_mode=streaming`
- train `sampling.policy=shuffle_buffer`
- `validation_sampling.policy=shuffle_buffer`
- `profiling.record_tokens_per_sec=true`
- `profiling.record_memory=true`
- `profiling.record_mfu=true`
- `profiling.expected_result_package=/vol/results/mvp28_a100_5gb_50step_sdpa_profile_results.tar.gz`

Current status: pending rerun. The correct next run is still:

```text
modal run scripts/modal_a100_streaming_runner.py --mode profile_5gb_50step_sdpa
```

## MVP-28.RUN-RERUN Second Attempt

After MVP-28.FIX-001, the rerun passed readiness and entered the actual A100 50-step SDPA profiling loop. The training/profiling body completed:

- `max_steps=50`
- `final_train_loss=4.271052`
- `final_validation_loss=8.776379`
- training script reported `success=True`

The Modal app still did not complete because the post-run artifact validator stopped the runner before result packaging. The validator still assumed long training artifacts and rejected the bounded profile artifact shape:

- `metrics_rows_actual=50`
- `validation_rows_actual=1`
- post-run validator blockers: `2`

No result package was produced. This is useful execution evidence, but the MVP-28 profiling artifact is still pending successful validation and packaging.

## MVP-28.FIX-002 Artifact Validation Split

The post-run artifact validator now separates:

- `training_execution`: unchanged validation for real training artifacts such as 1000/3000/5000-step runs
- `bounded_sdpa_profile`: explicit validation for the 50-step SDPA profiling artifact

For bounded profiling artifacts, the validator permits:

- `max_steps=50`
- `metrics_rows=50`
- `validation_rows=1`, derived from the config evaluation cadence

It still requires:

- summary success
- finite train loss
- finite validation loss when present
- `attention_backend=sdpa`
- profiling flags for tokens/sec, memory, and MFU enabled in `run_config.json`
- no 10000-step profile

Missing per-row profiling metrics are treated as caveats rather than immediate blockers, so long as the config flags are present and the run artifacts are otherwise consistent.

Current status: pending rerun / pending successful packaging. Do not treat MVP-28 profiling as completed until Modal app completes and the result package is produced.

## Next Command, Not Run In This Step

```text
modal run scripts/modal_a100_streaming_runner.py --mode profile_5gb_50step_sdpa
```

## Success Criteria For The Future Run

- Modal app completes.
- Mode is `profile_5gb_50step_sdpa`.
- `training.max_steps=50`.
- `profiling.attention_backend=sdpa`.
- Metrics include finite loss sanity and timing/throughput fields.
- Memory fields are recorded.
- Result package is written to `/vol/results/`.
- No checkpoint, tarball, raw data, or prepared split is committed.

## Stop Conditions

Stop and report blockers if:

- the mode resolves to a non-profiling config
- the run tries to use a long training config
- CUDA/A100 setup fails before profiling starts
- loss becomes non-finite
- result package is missing required small files
- artifact validation reports blockers

## Local Validation

Static validation script:

```text
scripts/validate_mvp28_i_attention_profile_mode.py
```

It checks the runner mode registry, config path, max steps, SDPA backend, profiling flags, streaming data mode, validation sampling, and expected result package without importing Modal or starting training.
