# MVP-26 Modal A100 5GB 3000-step Execution Receipt

## Receipt

| Field | Value |
| --- | --- |
| Modal app completed | `true` |
| Mode | `train_5gb_3000` |
| GPU | `A100-40GB` |
| ran_training | `true` |
| produced_checkpoint | `true` |
| training_status | `success` |
| repo_commit | `f703e07` |
| result package | `/vol/results/mvp26_a100_5gb_3000step_public16k_streaming_results.tar.gz` |
| final_train_loss | `3.029707` |
| final_validation_loss | `8.341638` |
| post-run blocker_count | `0` |

## Cost Boundary

This was a real Modal A100-40GB training run and therefore produced GPU cost. The measured training elapsed time was `1024.568388` seconds, consistent with the pre-run `$0.65-$0.90` estimate. GPU billing should stop after the Modal app completed. Modal Volume storage cost can continue while Volume data remains stored.

## Artifact Boundary

The run produced a remote checkpoint, but the checkpoint was not downloaded, imported, staged, or committed.

The raw result package was downloaded for import and copied to the project root as an untracked tarball:

```text
mvp26_a100_5gb_3000step_public16k_streaming_results.tar.gz
```

It must remain untracked. Only the small extracted result files under `results_imported_modal_streaming/` are eligible for version control.

## Import Step Boundary

During this import step:

- no additional Modal app was run
- no GPU was requested
- no training was started
- no checkpoint was committed
- no raw result tarball was committed
- no prepared data was committed
