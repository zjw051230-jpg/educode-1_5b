# MVP-30 Modal A100 Seq1024 SDPA Profiling Execution Receipt

## Receipt

| Field | Value |
| --- | --- |
| Modal app | completed |
| GPU | A100-40GB |
| mode | `profile_5gb_50step_seq1024_sdpa` |
| result package | `/vol/results/mvp30_a100_5gb_50step_seq1024_sdpa_profile_results.tar.gz` |
| final train loss | `1.450320` |
| final validation loss | `9.930368` |
| OOM | `false` |
| post-run blockers | `0` |
| cost estimate | approximately `$0.05-$0.20`; actual Modal billing should be checked separately |

## Import Boundary

No additional Modal run was executed during import. The import step only downloaded the result package from Modal Volume, inspected the tarball member list, extracted small JSON/JSONL/Markdown artifacts, and validated the imported files locally.

Checkpoint files and the raw result tarball are not committed to git. Modal Volume storage cost continues independently of this repository.
