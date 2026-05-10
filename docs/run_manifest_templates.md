# EduCode-1.5B Run Manifest Templates

## 1. Purpose
These templates define a minimal standard for recording every future experiment run in a structured and reusable way.

## 2. Template Files
- `templates/run_manifest/run_metadata.template.json`
- `templates/run_manifest/metrics.template.jsonl`
- `templates/run_manifest/generation_samples.template.jsonl`
- `templates/run_manifest/checkpoints_manifest.template.json`
- `templates/run_manifest/failure_report.template.md`
- `templates/run_manifest/summary.template.md`

## 3. How to Use
For each future run, copy the templates into:

```text
experiments/<stage>/<run_id>/
```

Then rename them to:
- `run_metadata.json`
- `metrics.jsonl`
- `generation_samples.jsonl`
- `checkpoints_manifest.json`
- `failure_report.md`
- `summary.md`

If the run uses a resolved config snapshot, it should also include `run_config.json` in the same run directory.

## 4. What Should Be Committed
- `templates/` can be committed
- `docs/` can be committed
- selected summaries under `experiments/` can be committed later if useful
- large files under `logs/`, `checkpoints/`, and `data/` should not be committed
- model weights should not be committed

## 5. Relation to W5
These templates are the minimal file-level realization of the W5 run logging format.

## 6. What W7 Does Not Do
W7 does not:
- implement a logger
- run experiments
- create real runs
- write training code
- implement tokenizer / model / training
- download data or models

## 7. Next Step
Suggested W8 directions:
- create a read-only config validation script draft
- or create an experiment index document
- still do not implement the training mainline
