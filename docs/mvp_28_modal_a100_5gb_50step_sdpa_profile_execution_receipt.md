# MVP-28 Modal A100 SDPA Profile Execution Receipt

## Receipt

| Field | Value |
| --- | --- |
| Status | Modal app completed |
| GPU | A100-40GB |
| Mode | `profile_5gb_50step_sdpa` |
| Ran training/profiling | `true` |
| Attention backend | `sdpa` |
| Max steps | `50` |
| Result package | `/vol/results/mvp28_a100_5gb_50step_sdpa_profile_results.tar.gz` |
| Final train loss | `4.328258` |
| Final validation loss | `8.897261` |
| Artifact validation blockers | `0` |

## Cost Boundary

Estimated cost remains in the expected `$0.05-$0.20` range, subject to Modal billing. GPU billing stops after `App completed`; Modal Volume storage cost continues.

## Import Boundary

No additional Modal run was executed during import. The import step downloaded the result package from Modal Volume and extracted only the small result files.

Checkpoint and tarball policy:

- checkpoint was produced remotely for reload validation
- checkpoint is not committed to git
- raw result tarball is left untracked
- prepared data is not committed

## Result Location

```text
experiments/a100/fineweb_edu_5gb_300m_50step_public16k_sdpa_profile/results_imported_modal_streaming/
```
