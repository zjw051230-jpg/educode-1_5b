# MVP-18.S Data Logistics Policy

## Purpose

This note records the data movement policy for public16k A800/A100 runs after MVP-18.

The goal is to keep GPU sessions focused on execution and artifact validation, not on large public-corpus fetching or data preparation.

## Policy Summary

Do not make the GPU container fetch 500MB+ Hugging Face or public-corpus slices during the training session.

Instead:

1. Prepare data locally or on a CPU cloud/data host.
2. Build and validate processed files and train/validation splits before GPU rental.
3. Package the prepared splits as a transfer artifact such as `prepared_splits.tar.gz`.
4. Transfer the prepared splits package to the GPU machine.
5. Run the GPU script against prepared local split files.
6. Download only a small result artifact package after the run.
7. Leave checkpoints remote unless explicitly approved for a separate purpose.

## Current 500MB Package

The current FineWeb-Edu 500MB prepared split package is about `207MB`.

That size is appropriate for deliberate transfer to a GPU host, but it should still remain outside git. It should be treated as a local/GPU runtime artifact, not a repository artifact.

## Future 2GB and 10GB Data Scale

Future 2GB or 10GB public-corpus work should use a local machine or CPU/data host for:

- raw public-corpus fetch;
- provenance and license checks;
- cleaning and metadata validation;
- processed JSONL creation;
- train/validation split creation;
- packaging;
- checksum recording.

The GPU host should receive prepared splits only. It should not be responsible for live Hugging Face fetching, large raw corpus staging, or corpus preprocessing during the rental window.

## Checkpoint and Result Artifact Policy

Do not download checkpoints by default. MVP-18's remote checkpoint was about `1.9G` and was intentionally not downloaded or committed.

Download only the small result package needed for review, such as:

- `summary.json`;
- `summary.md`;
- `metrics.jsonl`;
- `validation_metrics.jsonl`;
- `run_config.json`;
- `run_metadata.json`;
- post-run artifact validation summary.

## Commit Boundary

Allowed for commit:

- documentation;
- validation scripts;
- small reviewed summary artifacts.

Not allowed for commit without separate explicit approval:

- checkpoints;
- result tarballs;
- `raw.jsonl`;
- processed corpus directories;
- split files;
- prepared data packages.

## Operational Conclusion

Future GPU work should start from prepared data packages and end with small review artifacts. This keeps A800/A100 time focused on bounded training-systems validation and prevents raw data, processed data, split files, checkpoints, and result tarballs from entering git.
