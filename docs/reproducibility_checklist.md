# Reproducibility Checklist

Use this checklist before presenting a run or profiling result.

## Evidence Boundaries

- [ ] Identify whether the evidence is quality training, systems profiling, or memory preflight.
- [ ] State that short profiling losses are sanity signals only.
- [ ] Avoid unsupported claims about production model quality.
- [ ] Avoid speedup claims unless a matching baseline exists.

## Artifact Hygiene

- [ ] Raw datasets are not committed.
- [ ] Prepared data is not committed.
- [ ] Root-level result tarballs are not committed.
- [ ] Checkpoints are not committed.
- [ ] Imported result files are small files such as `summary.json`, `metrics.jsonl`, and `validation_metrics.jsonl`.

## Environment

- [ ] Capture repo commit and branch.
- [ ] Capture config path.
- [ ] Capture Python and package versions with `scripts/capture_environment_summary.py`.
- [ ] Record whether Modal, GPU, or training was run.

## Local Branch Guardrail

- Modal/GPU/training run: no for this branch.
- User cost confirmation needed: no for this branch.
- Tarball/checkpoint/raw data commit: no for this branch.
