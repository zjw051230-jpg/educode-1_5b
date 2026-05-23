# MVP-11.1 FineWeb-Edu 500MB Fetch and Intake Checklist

## 1. Scope

MVP-11.1 will fetch and intake the bounded 500MB FineWeb-Edu public corpus slice after MVP-11 readiness is committed.

This checklist is a command draft only. MVP-11 does not execute these commands.

## 2. Preconditions

Before running any fetch command:

```text
.venv/Scripts/python.exe scripts/check_fineweb_edu_500mb_expansion_readiness.py
```

Required result:

```text
ready_for_500mb_fetch=true
blockers=0
```

Also confirm there is enough local disk space for raw, processed, and split artifacts.

## 3. Fetch

```text
.venv/Scripts/python.exe scripts/fetch_fineweb_edu_slice.py --config configs/data/fineweb_edu_sample10bt_500mb.json --retries 2 --timeout-seconds 180
```

Expected local output:

```text
data/public_corpus/fineweb_edu_sample10bt_500mb/raw.jsonl
data/public_corpus/fineweb_edu_sample10bt_500mb/manifest.json
```

Do not commit `raw.jsonl`.

## 4. Validate Raw Slice

```text
.venv/Scripts/python.exe scripts/validate_fineweb_edu_slice.py --config configs/data/fineweb_edu_sample10bt_500mb.json
```

Expected small committed output:

```text
data/public_corpus/fineweb_edu_sample10bt_500mb/validation_summary.json
```

Stop if JSONL validation fails, empty text count is high, or duplicate rate is unexpectedly high.

## 5. Intake

```text
.venv/Scripts/python.exe scripts/intake_fineweb_edu_slice.py --config configs/data/fineweb_edu_sample10bt_500mb.json
```

Expected local outputs:

```text
data/public_corpus/fineweb_edu_sample10bt_500mb/processed/fineweb_edu_500mb.processed.jsonl
data/public_corpus/fineweb_edu_sample10bt_500mb/splits/fineweb_edu_500mb.train.jsonl
data/public_corpus/fineweb_edu_sample10bt_500mb/splits/fineweb_edu_500mb.val.jsonl
data/public_corpus/fineweb_edu_sample10bt_500mb/intake_summary.json
```

Do not commit `processed/` or `splits/`.

## 6. Validate Intake

```text
.venv/Scripts/python.exe scripts/validate_fineweb_edu_intake.py --config configs/data/fineweb_edu_sample10bt_500mb.json
```

Expected small committed output:

```text
data/public_corpus/fineweb_edu_sample10bt_500mb/intake_validation_summary.json
```

Stop if train/val overlap, duplicate `doc_id` values, or processed/split count mismatches are reported.

## 7. Git Status Check

```text
git status --short -- data/public_corpus/fineweb_edu_sample10bt_500mb/
```

Allowed trackable files after MVP-11.1:

```text
data/public_corpus/fineweb_edu_sample10bt_500mb/manifest.json
data/public_corpus/fineweb_edu_sample10bt_500mb/validation_summary.json
data/public_corpus/fineweb_edu_sample10bt_500mb/intake_summary.json
data/public_corpus/fineweb_edu_sample10bt_500mb/intake_validation_summary.json
```

Do not submit:

```text
data/public_corpus/fineweb_edu_sample10bt_500mb/raw.jsonl
data/public_corpus/fineweb_edu_sample10bt_500mb/processed/
data/public_corpus/fineweb_edu_sample10bt_500mb/splits/
```

## 8. Commit Policy

Only commit:

- small manifests;
- validation summaries;
- intake summaries;
- docs.

Do not commit raw corpus files, processed corpus files, split corpus files, checkpoints, or model artifacts.
