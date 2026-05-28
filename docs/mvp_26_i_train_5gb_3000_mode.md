# MVP-26.I 5GB 3000-step Modal Runner Mode

## Scope

This step implements and locally validates the `train_5gb_3000` Modal runner mode. It does not run Modal, does not request GPU, does not start training, does not run backward, does not call `optimizer.step()`, and does not create checkpoints or result tarballs.

## Why this step is needed

MVP-26.P confirmed that the 5GB 3000-step config is ready for a bounded next-scale decision after MVP-25.C removed the validation-coverage blocker. The remaining execution gate was that `scripts/modal_a100_streaming_runner.py` did not yet expose a `train_5gb_3000` mode.

This step closes that wiring gap only. It does not approve or execute the actual training run.

## Added runner mode

`train_5gb_3000` is registered in `MODE_SPECS` with:

| Field | Value |
| --- | --- |
| config | `configs/a100/fineweb_edu_5gb_300m_3000step_public16k_execute.json` |
| prepared package | `/vol/prepared/fineweb_edu_5gb_prepared_splits.tar.gz` |
| train split | `data/public_corpus/fineweb_edu_sample10bt_5gb/splits/fineweb_edu_5gb.train.jsonl` |
| validation split | `data/public_corpus/fineweb_edu_sample10bt_5gb/splits/fineweb_edu_5gb.val.jsonl` |
| result dir | `/vol/results/modal_train_5gb_3000` |
| result package | `/vol/results/mvp26_a100_5gb_3000step_public16k_streaming_results.tar.gz` |
| training mode | `train=True` |
| Modal GPU path | `A100-40GB`, same as existing non-CPU runner modes |

The runner required-commit guard is updated to include the pushed MVP-26.P planning commit `89ab3f6`.

## Difference from train_5gb_1000

| Item | `train_5gb_1000` | `train_5gb_3000` |
| --- | --- | --- |
| config | `fineweb_edu_5gb_300m_1000step_public16k_execute.json` | `fineweb_edu_5gb_300m_3000step_public16k_execute.json` |
| max steps | `1000` | `3000` |
| result dir | `/vol/results/modal_train_5gb_1000` | `/vol/results/modal_train_5gb_3000` |
| result package | `mvp24_a100_5gb_1000step_public16k_streaming_results.tar.gz` | `mvp26_a100_5gb_3000step_public16k_streaming_results.tar.gz` |
| expected train tokens | `16,384,000` | `49,152,000` |
| validation sampling | old executed run used weaker validation coverage | config uses MVP-25.C `shuffle_buffer` validation settings |

## Validation coverage wiring

The 3000-step config keeps the MVP-25.C validation settings:

| Field | Value |
| --- | --- |
| `validation_sampling.policy` | `shuffle_buffer` |
| `validation_sampling.shuffle_seed` | `7331` |
| `validation_sampling.shuffle_buffer_size` | `64` |
| `validation_sampling.max_blocks_per_document` | `8` |

The training script already records the validation coverage metadata in summaries:

- `validation_unique_doc_count`
- `validation_batches_evaluated`
- `validation_tokens_evaluated`
- `validation_prefix_only_risk`

## Local validation

The lightweight validator is:

```powershell
.\.venv\Scripts\python.exe scripts\validate_mvp26_i_train_5gb_3000_mode.py
```

It does not import Modal, does not run Modal, and does not train. It checks the runner registry and config mapping, confirms `max_steps=3000`, confirms expected train tokens are `49,152,000`, verifies the result package name, and verifies validation sampling remains `shuffle_buffer`.

Expected output includes:

```json
{
  "validation_status": "passed",
  "blocker_count": 0,
  "mode_name": "train_5gb_3000",
  "config_path": "configs/a100/fineweb_edu_5gb_300m_3000step_public16k_execute.json",
  "max_steps": 3000,
  "expected_tokens_seen": 49152000,
  "expected_result_package": "/vol/results/mvp26_a100_5gb_3000step_public16k_streaming_results.tar.gz",
  "validation_sampling_policy": "shuffle_buffer"
}
```

## Cost boundary

This step has no Modal runtime cost and no GPU cost because it only changes local runner wiring and runs local static/lightweight validation.

The next step is the real training cost gate. That step must explicitly approve Modal A100-40GB usage and should not be bundled into this implementation commit.

## Next-step command, not run in this step

The command for a future approved training run is:

```powershell
modal run scripts/modal_a100_streaming_runner.py --mode train_5gb_3000
```

Do not execute it until the next training gate explicitly authorizes Modal, GPU, and training cost.
