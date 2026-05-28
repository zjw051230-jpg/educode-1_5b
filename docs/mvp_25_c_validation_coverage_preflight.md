# MVP-25.C Real 5GB Validation Coverage Preflight

## Scope

MVP-25.C verifies the MVP-25.B validation coverage fix against the real prepared 5GB validation split in Modal Volume. This preflight only checks validation sampling coverage. It must not train a model, run backward, call `optimizer.step()`, save a training checkpoint, submit tarballs, or run any 5GB 3000-step or 10000-step training job.

## Why this preflight is needed

MVP-25.B proved the validation coverage fix with a local synthetic JSONL fixture. That was enough to validate iterator behavior, but it did not prove that the real prepared 5GB validation split and Modal Volume packaging expose multi-document validation coverage under the production config.

MVP-25.C closes that measurement-health gap by reading the real 5GB validation split from:

```text
/vol/prepared/fineweb_edu_5gb_prepared_splits.tar.gz
```

The preflight uses only the validation split and required metadata files. The training split is not required for this mode.

## First execution attempt and fix

The first real Modal CPU preflight attempt reached the CPU-only function but failed before validation batches were read. The failure happened while extracting required members from the prepared tarball:

```text
FileNotFoundError: missing required package members
```

Root cause: the runner assumed every prepared package member was rooted under:

```text
data/public_corpus/fineweb_edu_sample10bt_5gb/
```

The local copy recorded by the data logistics policy uses rootless package members instead:

```text
manifest.json
validation_summary.json
intake_validation_summary.json
splits/fineweb_edu_5gb.val.jsonl
```

The runner now discovers the actual tar members for the validation-only preflight instead of assuming one fixed root. It deterministically maps each expected repo path to the shortest matching tar member, extracts only the required files into the repo layout expected by the config, and records the actual member mapping in the Modal receipt as `package_member_discovery`.

Status remains pending rerun. This fix does not claim that the real 5GB validation coverage preflight passed.

## Modal mode

The new mode is:

```text
preflight_5gb_validation_coverage
```

Expected command:

```powershell
modal run scripts/modal_a100_streaming_runner.py --mode preflight_5gb_validation_coverage
```

This mode dispatches to the CPU-only Modal function, not the GPU-decorated A100 function.

Expected cost before execution:

- GPU 费用 = 0
- Only very low Modal CPU runtime and Modal Volume read cost are expected.
- The job selectively extracts the validation split and small metadata files instead of extracting the whole package.

## Validation sampling config

The preflight uses the existing 5GB validation sampling config:

```json
{
  "policy": "shuffle_buffer",
  "shuffle_seed": 7331,
  "shuffle_buffer_size": 64,
  "max_blocks_per_document": 8
}
```

This combines deterministic validation-side shuffle-buffer sampling with a per-document token-block cap. The goal is to make it impossible for one long validation document to fill every validation batch.

## Preflight boundaries

The preflight must report these execution boundaries:

- `used_gpu=false`
- `ran_training=false`
- `ran_backward=false`
- `ran_optimizer_step=false`
- `saved_checkpoint=false`

The implementation reads validation batches from `create_streaming_batch_iterator(...)`, but it does not instantiate the model or run a training loop.

## Required output fields

The Modal result must include:

- `preflight_status`
- `val_sampling_policy`
- `val_shuffle_seed`
- `val_shuffle_buffer_size`
- `validation_max_blocks_per_document`
- `validation_unique_doc_count`
- `validation_batches_evaluated`
- `validation_tokens_evaluated`
- `validation_prefix_only_risk`
- `blocker_count`
- `blockers`

Local copies are written to:

```text
experiments/a100/fineweb_edu_5gb_300m_1000step_public16k_execute/results_imported_modal_validation_coverage_preflight/modal_preflight_receipt.json
experiments/a100/fineweb_edu_5gb_300m_1000step_public16k_execute/results_imported_modal_validation_coverage_preflight/validation_coverage_preflight_summary.json
```

## Passing standard

MVP-25.C passes only if the local validator confirms:

- `preflight_status="passed"`
- `val_sampling_policy="shuffle_buffer"`
- `val_shuffle_seed=7331`
- `val_shuffle_buffer_size=64`
- `validation_max_blocks_per_document=8`
- `validation_unique_doc_count > 1`
- `validation_batches_evaluated > 0`
- `validation_tokens_evaluated > 0`
- `validation_prefix_only_risk=false`
- `blocker_count=0`
- `blockers=[]`
- no GPU, training, backward pass, optimizer step, or checkpoint was used

Validator:

```powershell
.\.venv\Scripts\python.exe -m py_compile scripts/validate_mvp25_c_validation_preflight_result.py
.\.venv\Scripts\python.exe scripts/validate_mvp25_c_validation_preflight_result.py
```

## Current result

Status: pending Modal execution.

This document intentionally does not claim a real 5GB validation coverage result yet. The Modal command and expected cost must be reported before execution. After the Modal run, update this section with the validator output and the next-training recommendation.

## Decision rule for next training

If MVP-25.C passes, the MVP-25.A validation-coverage blocker is removed for a bounded 5GB 3000-step training request. That still does not approve training by itself: the 5GB 3000-step run remains a separate cost-bearing Modal GPU action and requires explicit approval.

If MVP-25.C fails, do not run 5GB 3000-step or 10000-step training. Fix the validation coverage path or prepared artifact issue first.
