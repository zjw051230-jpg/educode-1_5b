# MVP-29 Seq1024 SDPA Memory Preflight Execution Receipt

## Receipt

| Field | Value |
| --- | --- |
| Modal app | completed |
| GPU | A100-40GB |
| mode | `preflight_5gb_10step_seq1024_sdpa_memory` |
| result package | `/vol/results/mvp29_a100_5gb_10step_seq1024_sdpa_memory_preflight_results.tar.gz` |
| final train loss | `2.392136` |
| final validation loss | `9.044042` |
| OOM | `false` |
| post-run blockers | `0` |
| cost estimate | approximately `$0.03-$0.15`; actual Modal billing should be checked separately |

## Import Boundary

No additional Modal run was executed during import. The import step only downloaded the result package from Modal Volume, inspected the tarball member list, extracted small JSON/JSONL/Markdown artifacts, and validated the imported files locally.

Checkpoint files and the raw result tarball are not committed to git. Modal Volume storage cost continues independently of this repository.
