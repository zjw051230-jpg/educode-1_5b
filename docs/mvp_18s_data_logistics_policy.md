# MVP-18.S Data Logistics Policy

## Purpose

This policy records how public-corpus data should move through future A800/A100 runs after MVP-18.

The goal is to keep GPU sessions focused on bounded execution, not large data fetching or corpus preparation.

## Policy

Do not fetch 500MB+ Hugging Face or public-corpus slices inside the GPU training container.

For future public16k GPU runs:

1. Prepare raw fetches, cleaned processed files, and train/validation splits locally or on a CPU/data host.
2. Validate provenance and training approval before packaging.
3. Transfer only prepared split packages to the GPU host.
4. Run the GPU script against prepared local split files.
5. Download only small result artifact packages for review.
6. Do not download checkpoints unless explicitly approved for a separate purpose.
7. Do not commit checkpoints, `raw.jsonl`, processed data, split files, or result tarballs.

## Current 500MB Package

The current 500MB FineWeb-Edu public corpus path should remain the baseline for MVP-19.

The prepared split package used for transfer is about `207MB`, which is small enough to move to a GPU host deliberately while still avoiding live corpus fetching inside the GPU container.

This package represents prepared train/validation split artifacts, not repository content to commit.

## Future 2GB and 10GB Corpus Work

For future 2GB or 10GB public corpus experiments, use a local machine or CPU/data host for:

- public-corpus fetching;
- raw source staging;
- cleaning and metadata validation;
- train/validation split creation;
- tokenizer or data compatibility checks;
- packaging and checksum recording.

The GPU host should receive prepared split packages only after these steps pass.

This avoids spending GPU rental time on network-bound data preparation and reduces the risk of failed runs caused by live dataset access, bandwidth variability, or host storage surprises.

## Artifact Download Boundary

After a GPU run, download a small result artifact package containing review files such as:

- `summary.json`;
- `summary.md`;
- `metrics.jsonl`;
- `validation_metrics.jsonl`;
- `run_config.json`;
- `run_metadata.json`;
- post-run artifact validation summary.

Do not download the checkpoint by default. MVP-18's remote checkpoint was about `1.9G` and was intentionally not downloaded or committed.

## Commit Boundary

Allowed for commit:

- documentation;
- validation scripts;
- small imported review artifacts;
- summary JSON files explicitly reviewed for size and contents.

Not allowed for commit unless separately approved:

- checkpoint files;
- result tarballs;
- `raw.jsonl`;
- processed corpus directories;
- split files;
- large data packages.

## Operational Conclusion

Future GPU sessions should start with prepared data already on the GPU host and should end by returning only small review artifacts. This keeps A800/A100 time focused on training-systems validation and keeps large data/checkpoint artifacts out of git.
