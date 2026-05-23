# MVP-3 FineWeb-Edu Fetch Troubleshooting

## 1. Original Dry-run Failure
The original MVP-3 dry-run attempted to read a small number of streaming records from `HuggingFaceFW/fineweb-edu` with config `sample-10BT`.

That dry-run failed before any bounded `50MB` fetch was attempted.

## 2. Error Summary
Observed failure signals included:
- `SSL: UNEXPECTED_EOF_WHILE_READING`
- `RuntimeError: Cannot send a request, as the client has been closed.`

This indicates that the failure was not caused by a missing `datasets` dependency.
It occurred while the Hugging Face streaming path was trying to read remote parquet metadata or records.

## 3. Why No 50MB Fetch Was Attempted
The `50MB` bounded fetch was intentionally not attempted after the original dry-run failed because:
- the dry-run is the safety gate for remote connectivity and script behavior
- a failed dry-run means the remote streaming path is not yet reliable enough for a controlled fetch
- this step should not hard-pull public data when the first remote read path is already unstable

## 4. Script Hardening Changes
MVP-3.R hardens the dry-run path by adding:
- bounded `--max-records`
- configurable `--timeout-seconds`
- bounded `--retries`
- configurable `--retry-sleep-seconds`
- optional `--preview-output` JSON for a tiny dry-run summary
- clearer exception reporting for SSL, client-closed, timeout, and Hugging Face connection failures
- cleanup behavior that avoids leaving partial fetch artifacts behind

## 5. Retry Policy
The hardened dry-run uses limited retry logic only:
- no infinite retry loop
- each retry prints attempt number and exception type
- retry behavior is intended for transient network instability, not for hiding persistent failures

## 6. HF_TOKEN Note
If a Hugging Face token is later provided, it should only be read from an environment variable such as `HF_TOKEN`.
The script does not write token values to files and must not print token values to the console.

This MVP-3.R step does not provide or record any token.

## 7. Windows Symlink Warning
The Hugging Face cache symlink warning on Windows is non-blocking.
It may affect cache efficiency and disk usage, but it is not the root cause of the original streaming failure.

## 8. Next Options
Available next options are:
- retry the dry-run later
- provide `HF_TOKEN` if rate or connection issues persist
- run the bounded fetch on A100/Linux instead of the current Windows network path
- choose an alternative public corpus if FineWeb-Edu remains unreliable in this environment
