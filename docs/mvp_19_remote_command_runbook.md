# MVP-19 Remote Command Runbook

This runbook gives command templates for a future MVP-19 A800/A100 streaming 3000-step run.

Do not run these commands during MVP-19.P. MVP-19.P is documentation-only.

## Local Upload Template

Upload the prepared split package from the local machine to the GPU host. Use placeholders for SSH details; do not hardcode a previous port.

```bash
scp -P <PORT> \
  fineweb_edu_500mb_prepared_splits.tar.gz \
  <USER>@<HOST>:~/educode_runtime/fineweb_edu_500mb_prepared_splits.tar.gz
```

## Remote Setup and Readiness Commands

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

test -s ~/educode_runtime/fineweb_edu_500mb_prepared_splits.tar.gz

tar -xzf ~/educode_runtime/fineweb_edu_500mb_prepared_splits.tar.gz -C ~/educode-1_5b

test -s data/public_corpus/fineweb_edu_sample10bt_500mb/splits/fineweb_edu_500mb.train.jsonl
test -s data/public_corpus/fineweb_edu_sample10bt_500mb/splits/fineweb_edu_500mb.val.jsonl

python scripts/inspect_training_batch_memory_plan.py \
  --config configs/a100/fineweb_edu_500mb_300m_3000step_public16k_execute.json

python scripts/run_a100_300m_fineweb_edu_10step_training.py \
  --config configs/a100/fineweb_edu_500mb_300m_3000step_public16k_execute.json \
  --dry-run

python scripts/check_a100_execution_readiness.py \
  --config configs/a100/fineweb_edu_500mb_300m_3000step_public16k_execute.json
```

Expected readiness output includes:

```text
data_loading_mode=streaming
ready_for_a800_execution=True
blockers=0
```

Stop if readiness has blockers.

## Remote Training Command

Run only after explicit approval.

```bash
cd ~/educode-1_5b

python scripts/run_a100_300m_fineweb_edu_10step_training.py \
  --config configs/a100/fineweb_edu_500mb_300m_3000step_public16k_execute.json
```

## Remote Post-run Validation and Packaging

```bash
cd ~/educode-1_5b

python scripts/validate_a800_public16k_run_artifacts.py \
  --output-dir experiments/a100/fineweb_edu_500mb_300m_3000step_public16k_execute

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

ls -lh ~/educode_runtime/mvp19_a800_3000step_public16k_streaming_results.tar.gz
```

The package must not include checkpoint files, raw corpus files, processed corpus files, train/validation split files, or prepared split packages.

## Local Download Template

Download only the small result package to the local project root. Do not commit the result tarball.

```bash
scp -P <PORT> \
  <USER>@<HOST>:~/educode_runtime/mvp19_a800_3000step_public16k_streaming_results.tar.gz \
  D:/模型/educode-1_5b/mvp19_a800_3000step_public16k_streaming_results.tar.gz
```

## Local Next Step After Download

After the result package exists locally, start MVP-19.R import and validation using:

```text
docs/mvp_19r_import_streaming_3000step_results_plan.md
```

Keep the tarball local-only unless a later step explicitly authorizes a different artifact policy.
