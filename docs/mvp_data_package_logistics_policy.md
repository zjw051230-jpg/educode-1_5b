# MVP Data Package Logistics Policy

## Purpose

Keep public-corpus preparation CPU/local-side and keep GPU rental sessions focused on bounded training execution. GPU hosts should receive prepared split packages instead of fetching Hugging Face datasets during paid training windows.

## Package Sources

| corpus slice | local package | intended remote extract dir | status |
|---|---|---|---|
| FineWeb-Edu `sample-10BT` 2GB | `C:/Users/01/fineweb_edu_2gb_prepared_splits.tar.gz` | `data/public_corpus/fineweb_edu_sample10bt_2gb/` | prepared |
| FineWeb-Edu `sample-10BT` 5GB | `C:/Users/01/fineweb_edu_5gb_prepared_splits.tar.gz` | `data/public_corpus/fineweb_edu_sample10bt_5gb/` | prepared; SHA-256 `19a933ec5afc379d58751461ff56e8e89be4d3fbfc05e10df789c6541f8bcd5d` |

## Required Package Members

Prepared split packages should contain only small metadata and train/val splits:

- `manifest.json`
- `validation_summary.json`
- `intake_summary.json`
- `intake_validation_summary.json`
- `splits/<basename>.train.jsonl`
- `splits/<basename>.val.jsonl`

They must not contain:

- `raw.jsonl`
- `processed/`
- checkpoints
- model weights
- tokenizer artifacts
- result tarballs
- absolute paths
- parent-directory traversal entries

## GPU Host Rules

1. Upload the prepared package before starting the training command phase.
2. Verify the package SHA-256 against the committed `prepared_package_manifest.json`.
3. Extract into the matching `data/public_corpus/fineweb_edu_sample10bt_<size>/` directory.
4. Verify `intake_validation_summary.json` counts and train/val paths.
5. Run memory inspection, dry-run, and readiness checks on the GPU host before training.
6. Do not fetch Hugging Face data on the GPU host for prepared slices.
7. Copy back only small result packages and validation summaries unless a later step explicitly approves checkpoint transfer.

## Commit Boundary

Allowed in Git:

- data configs
- small manifests and validation summaries
- prepared package manifests
- readiness summaries
- result import plans
- documentation

Not allowed in Git:

- `raw.jsonl`
- `processed/`
- `splits/`
- prepared `.tar.gz` packages
- checkpoints
- model weights
- result `.tar.gz` packages

## Failure Handling

If local fetch, validation, intake, or packaging fails, record the slice as partial/prepared-plan-only. Do not create a fake package manifest, do not run downstream readiness as if splits exist, and do not claim GPU readiness for that corpus size.
