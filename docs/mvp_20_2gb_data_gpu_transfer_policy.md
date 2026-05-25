# MVP-20 2GB Data GPU Transfer Policy

## Purpose

Use the locally prepared FineWeb-Edu 2GB split package for future GPU sessions so A800/A100 containers do not fetch Hugging Face data during paid rental time.

## Local Source Package

```text
C:/Users/01/fineweb_edu_2gb_prepared_splits.tar.gz
```

Expected package members:

- `manifest.json`
- `validation_summary.json`
- `intake_summary.json`
- `intake_validation_summary.json`
- `splits/fineweb_edu_2gb.train.jsonl`
- `splits/fineweb_edu_2gb.val.jsonl`

The package must not contain:

- `raw.jsonl`
- `processed/`
- checkpoints
- model weights
- tokenizer artifacts
- result tarballs
- absolute paths
- parent-directory traversal entries

## Upload Rule

Upload the prepared package to the GPU host before entering the training command phase. Do not run Hugging Face dataset fetch commands on the GPU host for this 2GB slice.

Example shape, with provider-specific values filled in at rental time:

```text
scp -P <PORT> C:/Users/01/fineweb_edu_2gb_prepared_splits.tar.gz <USER>@<HOST>:/workspace/fineweb_edu_2gb_prepared_splits.tar.gz
```

## Remote Unpack Rule

Unpack into the project root or a staging directory that preserves these repo-relative paths:

```text
data/public_corpus/fineweb_edu_sample10bt_2gb/manifest.json
data/public_corpus/fineweb_edu_sample10bt_2gb/validation_summary.json
data/public_corpus/fineweb_edu_sample10bt_2gb/intake_summary.json
data/public_corpus/fineweb_edu_sample10bt_2gb/intake_validation_summary.json
data/public_corpus/fineweb_edu_sample10bt_2gb/splits/fineweb_edu_2gb.train.jsonl
data/public_corpus/fineweb_edu_sample10bt_2gb/splits/fineweb_edu_2gb.val.jsonl
```

If unpacking directly from this package, create the `data/public_corpus/fineweb_edu_sample10bt_2gb/` directory first and extract package members under it.

## Verification Before Training

Before any GPU training command, verify:

- package SHA-256 equals `1c02cdf74e5a883ac1fcbee2cb9ebcf5917b8de145aaf4bdc59b1da6c120d51a`;
- train split exists at `data/public_corpus/fineweb_edu_sample10bt_2gb/splits/fineweb_edu_2gb.train.jsonl`;
- val split exists at `data/public_corpus/fineweb_edu_sample10bt_2gb/splits/fineweb_edu_2gb.val.jsonl`;
- `intake_validation_summary.json` reports `processed_count=449367`, `train_count=426857`, and `val_count=22510`;
- no training command downloads FineWeb-Edu from Hugging Face on the GPU host.

## Copyback Rule

After a future GPU run, copy back only small result artifacts and validation summaries unless explicitly approved otherwise. Do not copy checkpoints or large generated artifacts back into Git.
