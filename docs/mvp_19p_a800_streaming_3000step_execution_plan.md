# MVP-19.P A800 Streaming 3000-step Execution Plan

## 1. Purpose

MVP-19.P prepares the next A800/A100 3000-step streaming run. The goal of the future execution is to verify whether the MVP-17 streaming path remains stable over a longer bounded training-systems run after MVP-18 restored `batch_size=8` / `gradient_accumulation_steps=4` for 1000 steps.

This plan does not run training, enter A100/A800, download data, train tokenizer/model artifacts, modify training main logic, or commit checkpoints, `raw.jsonl`, processed data, split files, or result tarballs.

## 2. Prerequisites

Required software/project state:

- latest commit on the execution machine: `0a1cb75` or later;
- MVP-18 streaming 1000-step success already reviewed;
- config path: `configs/a100/fineweb_edu_500mb_300m_3000step_public16k_execute.json`;
- streaming code from `c2a46e5+` present;
- local prepared splits package available before GPU rental:

```text
fineweb_edu_500mb_prepared_splits.tar.gz
```

Required GPU instance:

- 1 x A800/A100 40GB-class GPU;
- container/host RAM `>=48GiB` preferred;
- disk `>=50GB` available for source checkout, prepared splits, logs, result artifacts, and one remote checkpoint.

## 3. Do Not Fetch on GPU Host

Do not fetch FineWeb-Edu or any 500MB+ Hugging Face/public-corpus slice on the GPU host.

The GPU machine should receive the prepared local split package only. The GPU session should perform training, validation, and artifact packaging, not public-corpus download or preprocessing.

## 4. Remote Setup Commands

The remote setup should establish hardware visibility, memory availability, repository state, dependencies, and prepared data before any training command.

```bash
set -euo pipefail

nvidia-smi

python - <<'PY'
from pathlib import Path
candidates = [
    Path('/sys/fs/cgroup/memory.max'),
    Path('/sys/fs/cgroup/memory/memory.limit_in_bytes'),
]
for path in candidates:
    if path.exists():
        value = path.read_text(encoding='utf-8').strip()
        print(f'{path}: {value}')
PY

mkdir -p ~/educode_runtime
cd ~

if [ ! -d educode-1_5b ]; then
  git clone <REPO_URL> educode-1_5b
fi

cd ~/educode-1_5b
git fetch --all --tags
git checkout main
git pull --ff-only
git log --oneline -n 5
git rev-parse --short HEAD

python -m pip install --upgrade pip
python -m pip install torch tokenizers

# The prepared split package should already have been uploaded to ~/educode_runtime/.
test -s ~/educode_runtime/fineweb_edu_500mb_prepared_splits.tar.gz

tar -xzf ~/educode_runtime/fineweb_edu_500mb_prepared_splits.tar.gz -C ~/educode-1_5b

test -s data/public_corpus/fineweb_edu_sample10bt_500mb/splits/fineweb_edu_500mb.train.jsonl
test -s data/public_corpus/fineweb_edu_sample10bt_500mb/splits/fineweb_edu_500mb.val.jsonl
```

If the uploaded package layout differs, stop and inspect the archive before moving files. Do not run training until the train/val split paths match the config.

## 5. Readiness Commands

Run the local memory-plan inspection, dry-run, and readiness gate before the 3000-step execution.

```bash
cd ~/educode-1_5b

python scripts/inspect_training_batch_memory_plan.py \
  --config configs/a100/fineweb_edu_500mb_300m_3000step_public16k_execute.json

python scripts/run_a100_300m_fineweb_edu_10step_training.py \
  --config configs/a100/fineweb_edu_500mb_300m_3000step_public16k_execute.json \
  --dry-run

python scripts/check_a100_execution_readiness.py \
  --config configs/a100/fineweb_edu_500mb_300m_3000step_public16k_execute.json
```

Expected readiness indicators:

```text
data_loading_mode=streaming
ready_for_a800_execution=True
blockers=0
```

Stop if readiness reports blockers or if the dry-run/config output does not point to the 3000-step output directory.

## 6. Training Command

Run this command only after explicit approval and after the readiness commands pass.

```bash
cd ~/educode-1_5b

python scripts/run_a100_300m_fineweb_edu_10step_training.py \
  --config configs/a100/fineweb_edu_500mb_300m_3000step_public16k_execute.json
```

This is a bounded training-systems execution. It is not a model-quality claim.

## 7. Post-run Validation

After training completes, validate the run artifacts on the GPU host.

```bash
cd ~/educode-1_5b

python scripts/validate_a800_public16k_run_artifacts.py \
  --output-dir experiments/a100/fineweb_edu_500mb_300m_3000step_public16k_execute
```

Expected result:

```text
success=true
metrics_rows=3000
validation_rows=10
checkpoint_reload_match=true
post_run_artifact_validation passed
```

The validator writes `post_run_artifact_validation_summary.json` into the run output directory. Treat any blocker as a stop condition.

## 8. Copyback Policy

Only package and download the small review files:

- `summary.json`;
- `summary.md`;
- `metrics.jsonl`;
- `validation_metrics.jsonl`;
- `run_config.json`;
- `run_metadata.json`;
- `post_run_artifact_validation_summary.json`.

Do not download:

- checkpoint files;
- raw corpus files;
- processed corpus files;
- train/validation split files;
- prepared split packages.

Suggested remote package command:

```bash
cd ~/educode-1_5b

mkdir -p ~/educode_runtime/mvp19_copyback

tar -czf ~/educode_runtime/mvp19_a800_3000step_public16k_streaming_results.tar.gz \
  -C experiments/a100/fineweb_edu_500mb_300m_3000step_public16k_execute \
  summary.json \
  summary.md \
  metrics.jsonl \
  validation_metrics.jsonl \
  run_config.json \
  run_metadata.json \
  post_run_artifact_validation_summary.json
```

## 9. Stop Conditions

Stop and preserve logs for review if any of these occur:

- cgroup/container RAM is less than `32GiB`;
- readiness blockers are greater than `0`;
- the dry-run points to the wrong output directory or stale run name;
- GPU or host OOM occurs;
- any loss or gradient value becomes non-finite;
- `checkpoint_reload_match=false`;
- post-run artifact validation fails;
- expected metrics or validation row counts are missing;
- the output directory contains unexpected checkpoint path behavior.

## 10. Expected Runtime

MVP-18 1000-step elapsed time was `343.899789` seconds. A linear 3000-step estimate is about `1031.699367` seconds, or about `17.2` minutes.

Reserve `30-40` minutes total for GPU execution, validation, packaging, and buffer time.
