# MVP-21 2GB Remote Command Runbook

This runbook is for a future A800/A100 execution session using the MVP-20 FineWeb-Edu 2GB prepared splits.

Do not run these commands during MVP-21.P. MVP-21.P is local config/readiness preparation only.

## Local Upload Command

```bash
scp -P <PORT> C:\Users\01\fineweb_edu_2gb_prepared_splits.tar.gz root@<HOST>:/workspace/
```

## Remote Setup and Extract

```bash
set -euo pipefail

nvidia-smi

python - <<'PY'
from pathlib import Path
paths = [
    Path('/sys/fs/cgroup/memory.max'),
    Path('/sys/fs/cgroup/memory/memory.limit_in_bytes'),
]
for path in paths:
    if path.exists():
        print(f'{path}: {path.read_text(encoding="utf-8").strip()}')
PY

cd /workspace

test -s /workspace/fineweb_edu_2gb_prepared_splits.tar.gz
sha256sum /workspace/fineweb_edu_2gb_prepared_splits.tar.gz

if [ ! -d educode-1_5b ]; then
  git clone <REPO_URL> educode-1_5b
fi

cd /workspace/educode-1_5b
git fetch --all --tags
git checkout main
git pull --ff-only
git log --oneline -n 5
git rev-parse --short HEAD

python -m pip install --upgrade pip
python -m pip install torch tokenizers

mkdir -p data/public_corpus/fineweb_edu_sample10bt_2gb
tar -xzf /workspace/fineweb_edu_2gb_prepared_splits.tar.gz \
  -C data/public_corpus/fineweb_edu_sample10bt_2gb
```

## Verify Data Files

```bash
test -s data/public_corpus/fineweb_edu_sample10bt_2gb/manifest.json
test -s data/public_corpus/fineweb_edu_sample10bt_2gb/validation_summary.json
test -s data/public_corpus/fineweb_edu_sample10bt_2gb/intake_summary.json
test -s data/public_corpus/fineweb_edu_sample10bt_2gb/intake_validation_summary.json
test -s data/public_corpus/fineweb_edu_sample10bt_2gb/splits/fineweb_edu_2gb.train.jsonl
test -s data/public_corpus/fineweb_edu_sample10bt_2gb/splits/fineweb_edu_2gb.val.jsonl

python - <<'PY'
import json
from pathlib import Path
summary = json.loads(Path('data/public_corpus/fineweb_edu_sample10bt_2gb/intake_validation_summary.json').read_text(encoding='utf-8'))
assert summary['processed_count'] == 449367
assert summary['train_count'] == 426857
assert summary['val_count'] == 22510
print('2GB intake validation counts match MVP-20')
PY
```

## Memory Plan, Dry-run, and Readiness

```bash
python scripts/inspect_training_batch_memory_plan.py \
  --config configs/a100/fineweb_edu_2gb_300m_1000step_public16k_execute.json

python scripts/run_a100_300m_fineweb_edu_10step_training.py \
  --config configs/a100/fineweb_edu_2gb_300m_1000step_public16k_execute.json \
  --dry-run

python scripts/check_a100_execution_readiness.py \
  --config configs/a100/fineweb_edu_2gb_300m_1000step_public16k_execute.json
```

Expected readiness output includes:

```text
data_loading_mode=streaming
ready_for_a800_execution=True
ready_for_a100_execution=True
blockers=0
```

Stop if readiness has blockers.

## 1000-step Training Command

Run only after explicit approval.

```bash
cd /workspace/educode-1_5b

python scripts/run_a100_300m_fineweb_edu_10step_training.py \
  --config configs/a100/fineweb_edu_2gb_300m_1000step_public16k_execute.json
```

## Post-run Validation and Result Packaging

```bash
cd /workspace/educode-1_5b

python scripts/validate_a800_public16k_run_artifacts.py \
  --output-dir experiments/a100/fineweb_edu_2gb_300m_1000step_public16k_execute

tar -czf /workspace/mvp21_a800_2gb_1000step_public16k_streaming_results.tar.gz \
  -C experiments/a100/fineweb_edu_2gb_300m_1000step_public16k_execute \
  summary.json \
  summary.md \
  metrics.jsonl \
  validation_metrics.jsonl \
  run_config.json \
  run_metadata.json \
  post_run_artifact_validation_summary.json

ls -lh /workspace/mvp21_a800_2gb_1000step_public16k_streaming_results.tar.gz
```

The result package must not include checkpoints, raw corpus files, processed corpus files, split files, or the prepared split package.

## Optional 3000-step Follow-up

Run the 3000-step config only after the 1000-step run succeeds with finite losses, checkpoint reload match, and post-run artifact validation.

```bash
python scripts/inspect_training_batch_memory_plan.py \
  --config configs/a100/fineweb_edu_2gb_300m_3000step_public16k_execute.json

python scripts/run_a100_300m_fineweb_edu_10step_training.py \
  --config configs/a100/fineweb_edu_2gb_300m_3000step_public16k_execute.json \
  --dry-run

python scripts/check_a100_execution_readiness.py \
  --config configs/a100/fineweb_edu_2gb_300m_3000step_public16k_execute.json

python scripts/run_a100_300m_fineweb_edu_10step_training.py \
  --config configs/a100/fineweb_edu_2gb_300m_3000step_public16k_execute.json
```

## Optional 5000-step Follow-up

Run the 5000-step config only after the 3000-step run succeeds with finite losses, checkpoint reload match, post-run artifact validation, and enough rental time remaining.

```bash
python scripts/inspect_training_batch_memory_plan.py \
  --config configs/a100/fineweb_edu_2gb_300m_5000step_public16k_execute.json

python scripts/run_a100_300m_fineweb_edu_10step_training.py \
  --config configs/a100/fineweb_edu_2gb_300m_5000step_public16k_execute.json \
  --dry-run

python scripts/check_a100_execution_readiness.py \
  --config configs/a100/fineweb_edu_2gb_300m_5000step_public16k_execute.json

python scripts/run_a100_300m_fineweb_edu_10step_training.py \
  --config configs/a100/fineweb_edu_2gb_300m_5000step_public16k_execute.json
```
