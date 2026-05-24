# MVP-19.Q Prepared Data Package Checklist

## Purpose

This checklist defines the prepared data package policy for the next A800/A100 one-hour streaming queue.

The GPU host must not fetch FineWeb-Edu or any 500MB+ public-corpus slice from Hugging Face. It should receive a prepared split package and run only training, validation, and small artifact packaging.

## Local Prepared Package

Expected local package:

```text
C:/Users/01/fineweb_edu_500mb_prepared_splits.tar.gz
```

This package is a local runtime artifact. Do not commit it.

## Required Package Contents

The package must contain:

- `manifest.json`;
- `validation_summary.json`;
- `intake_summary.json`;
- `intake_validation_summary.json`;
- `fineweb_edu_500mb.train.jsonl`;
- `fineweb_edu_500mb.val.jsonl`.

## Local Inspection Before Upload

Before upload, inspect the archive member list and confirm it contains only expected metadata and split files.

Reject the package if it contains:

- checkpoints;
- model weights;
- unrelated raw corpus files;
- unrelated processed directories;
- absolute paths;
- parent-directory traversal entries.

## Upload Command Template

Use placeholders for the target GPU host. Do not hardcode old ports or hosts.

```bash
scp -P <PORT> C:\Users\01\fineweb_edu_500mb_prepared_splits.tar.gz root@<HOST>:/workspace/
```

## GPU Host Extraction Target

Extract into:

```text
/workspace/educode-1_5b/
```

The extracted files must satisfy the config paths:

```text
data/public_corpus/fineweb_edu_sample10bt_500mb/splits/fineweb_edu_500mb.train.jsonl
data/public_corpus/fineweb_edu_sample10bt_500mb/splits/fineweb_edu_500mb.val.jsonl
```

## GPU Host Policy

On the GPU host:

- do not fetch Hugging Face data;
- do not preprocess the public corpus;
- do not create a new tokenizer;
- do not download or commit checkpoints;
- do not copy raw/processed/split files back to git;
- only package small result artifacts after each run.

## Queue Usage

The same prepared 500MB split package is used for:

1. MVP-19 streaming 3000-step primary run;
2. MVP-20.S streaming 5000-step follow-up only if the 3000-step run succeeds and enough time remains.
