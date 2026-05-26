# MVP-22.S Modal Cost and Storage Note

## Current Runtime State

The Modal GPU jobs for the 2GB 1000-step and 2GB 3000-step runs have completed. They should not continue to incur GPU runtime cost after completion.

Do not deploy a persistent Modal app for this stage. Do not configure keep-warm behavior or minimum containers.

## Current Modal Volume Contents To Account For

The Modal Volume `educode-data` is expected to retain at least:

```text
/prepared/fineweb_edu_2gb_prepared_splits.tar.gz
/results/mvp21_a100_2gb_1000step_public16k_streaming_results.tar.gz
/results/mvp22_a100_2gb_3000step_public16k_streaming_results.tar.gz
```

The prepared package is the important reusable data artifact. Result packages are small review/import artifacts.

## Storage Cost Estimate

The local 2GB prepared package is approximately `847MB`. The result packages are small relative to the prepared package.

Keeping only the 2GB prepared package plus the two result packages is roughly in the `$0.08/month` storage-cost range, assuming Modal Volume storage pricing around `$0.09/GiB/month` and no large checkpoints retained.

This is an estimate for planning, not a billing receipt.

## 5GB Package Impact

If the 5GB prepared package is uploaded later, Volume storage cost will increase. The local 5GB package is about `2.1GB`, so storing it adds roughly:

```text
2.1 GiB × $0.09/GiB/month ≈ $0.19/month
```

The 5GB upload should happen only when there is a clear plan to run the 5GB preflight or training path.

## Cost Safety Rules

- Do not deploy a persistent Modal app.
- Do not use keep-warm containers.
- Do not set minimum containers.
- Run one explicit Modal job at a time.
- Run preflight before training.
- Stop on readiness blockers.
- Do not download or commit checkpoints by default.
- Do not fetch Hugging Face data from GPU workers for prepared-corpus runs.

## Next Cost Gate

Before the next Modal training job, explicitly confirm:

1. intended mode;
2. expected input package already in Volume;
3. whether the job is preflight-only or training;
4. estimated runtime cost range;
5. whether checkpoints should remain remote-only;
6. whether result tarballs should be downloaded after completion.

The default next cost decision should compare local scheduler/sampling cleanup, 5GB 1000-step preflight, and optional 2GB 5000-step stability extension.
