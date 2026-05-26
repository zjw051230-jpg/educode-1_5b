# MVP-26.P Modal Volume Data Policy

## Purpose

Define how EduCode-1.5B prepared corpus packages and small result artifacts move through Modal without exposing credentials, fetching Hugging Face data on GPU jobs, or committing large artifacts.

## Modal Setup Commands

Run locally if Modal is not installed or not authenticated:

```bash
python -m pip install -U modal
modal setup
```

Do not paste Modal tokens into chat, code, docs, or Git.

## Volume Commands

Create the shared Modal Volume:

```bash
modal volume create educode-data
```

Upload the recommended 2GB prepared package first:

```bash
modal volume put educode-data C:\Users\01\fineweb_edu_2gb_prepared_splits.tar.gz /prepared/fineweb_edu_2gb_prepared_splits.tar.gz
```

Optional 5GB standby upload:

```bash
modal volume put educode-data C:\Users\01\fineweb_edu_5gb_prepared_splits.tar.gz /prepared/fineweb_edu_5gb_prepared_splits.tar.gz
```

## Result Download Template

Download only small result packages:

```bash
modal volume get educode-data /results/mvp21_a100_2gb_1000step_public16k_streaming_results.tar.gz C:\Users\01\mvp21_a100_2gb_1000step_public16k_streaming_results.tar.gz
```

For preflight-only results, download the small preflight result directory or specific JSON summaries from:

```text
/results/modal_preflight_2gb_1000/
```

## Volume Layout Policy

| path | purpose | default download policy |
|---|---|---|
| `/prepared/` | local prepared split packages uploaded before GPU execution | upload only; do not import into Git |
| `/results/` | small preflight summaries and small training result packages | download after validation |
| `/checkpoints/` | temporary checkpoints from explicit future training runs | do not download by default |

## Execution Policy

- Prepared packages go under `/prepared/`.
- Result packages go under `/results/`.
- Checkpoints can stay under `/checkpoints/` temporarily but should not be downloaded by default.
- Modal GPU functions must not fetch FineWeb-Edu from Hugging Face.
- Modal GPU functions should unpack prepared packages from `/vol/prepared/`.
- No credentials belong in the repository.

## First Package to Use

Start with:

```text
/prepared/fineweb_edu_2gb_prepared_splits.tar.gz
```

Do not start with 5GB. Use 5GB only after the 2GB route has successful preflight/training evidence.

## Result Package Boundary

Allowed small result package members:

- `summary.json`
- `summary.md`
- `metrics.jsonl`
- `validation_metrics.jsonl`
- `run_config.json`
- `run_metadata.json`
- `post_run_artifact_validation_summary.json`

Not allowed in Git:

- prepared `.tar.gz` packages;
- checkpoints;
- raw corpus files;
- processed corpus files;
- split files;
- credentials or token files.
