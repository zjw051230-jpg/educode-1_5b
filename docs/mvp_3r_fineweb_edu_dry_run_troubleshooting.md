# MVP-3.R FineWeb-Edu Dry-run Troubleshooting

## 1. Purpose
The purpose of MVP-3.R is to harden the FineWeb-Edu dry-run path, retry the dry-run in a bounded way, and record the result without attempting the full `50MB` fetch.

## 2. Dry-run Command
Enhanced dry-run command used:

```text
.venv/Scripts/python.exe scripts/fetch_fineweb_edu_slice.py --config configs/data/fineweb_edu_sample10bt_50mb.json --dry-run --max-records 3 --retries 2 --timeout-seconds 60 --preview-output data/public_corpus/fineweb_edu_sample10bt_50mb/dry_run_preview.json
```

## 3. Dry-run Result
The enhanced dry-run completed successfully.
Observed result:
- `record_count=3`
- `size_mb=0.009165`
- no bounded `50MB` fetch was attempted in this step

## 4. Preview Output
A small preview file was generated:
- `data/public_corpus/fineweb_edu_sample10bt_50mb/dry_run_preview.json`

The preview is intentionally tiny and does not include a large raw corpus artifact.

## 5. Raw Output Check
`data/public_corpus/fineweb_edu_sample10bt_50mb/raw.jsonl` does not exist after the dry-run.
This confirms that the hardened dry-run did not create a fetch output file.

## 6. Error Summary
The original MVP-3 dry-run failed with remote streaming errors.
After script hardening, the enhanced dry-run succeeded without requiring `HF_TOKEN` and without performing the `50MB` fetch.

## 7. Next Recommended Action
Recommended next action:
- decide whether to proceed to a later controlled `50MB` fetch step
- if future instability returns, retry later, provide `HF_TOKEN`, move the fetch to A100/Linux, or switch public corpus
