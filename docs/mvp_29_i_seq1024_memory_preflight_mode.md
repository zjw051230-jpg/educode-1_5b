# MVP-29.I Seq1024 SDPA Memory Preflight Mode

## Scope

This step adds a bounded context length `1024` SDPA memory preflight config, Modal runner mode, readiness validation, artifact-validation support, and a local validator. It does not run Modal, does not request GPU, does not start training, and does not produce a real A100 result.

## Why This Is Needed

MVP-28 produced a real A100 SDPA seq512 systems baseline. MVP-29.P concluded that the next useful scaling-axis test is context length `512 -> 1024`, but only through a short memory preflight first.

The goal is to verify whether the current 300M-class model, SDPA attention path, streaming 5GB FineWeb-Edu input, and Modal A100-40GB path can handle seq1024 before spending on longer training.

## Why Not Direct Seq1024 3000-step

Do not run seq1024 3000-step directly:

- context length changes attention memory and throughput behavior
- attention memory can grow roughly with sequence length squared
- seq512 evidence does not prove seq1024 memory safety
- longer training would spend money before proving the new shape fits
- loss from a short preflight is only a sanity signal, not quality evidence

## New Config

```text
configs/a100/fineweb_edu_5gb_300m_10step_public16k_seq1024_sdpa_memory_preflight.json
```

Key parameters:

| Field | Value |
| --- | --- |
| context length | `1024` |
| max steps | `10` |
| batch size | `4` |
| grad accum | `4` |
| tokens per optimizer step | `16384` |
| attention backend | `sdpa` |
| data loading | `streaming` |
| train sampling | `shuffle_buffer`, seed `1337`, buffer `1024` |
| validation sampling | `shuffle_buffer`, seed `7331`, buffer `64`, max blocks/doc `8` |
| result package | `/vol/results/mvp29_a100_5gb_10step_seq1024_sdpa_memory_preflight_results.tar.gz` |

## Why Batch Size 4

The seq512 SDPA baseline used `batch_size=8`, `context_length=512`, and `grad_accum=4`, giving:

```text
8 * 512 * 4 = 16384 tokens per optimizer step
```

This seq1024 preflight uses:

```text
4 * 1024 * 4 = 16384 tokens per optimizer step
```

That keeps the optimizer-step token budget stable while testing the longer context. It is the conservative first probe. If this passes with comfortable memory headroom, a later batch-size-8 throughput probe can be planned separately.

## Why Keep Grad Accum 4

Keeping `grad_accum=4` avoids changing two knobs at once. The first seq1024 check should isolate context length and memory behavior as much as possible.

## Why Continue SDPA

The runtime model currently supports PyTorch SDPA only. `src/educode/tiny_model.py` rejects non-`sdpa` attention backends. Naive attention and FlashAttention remain separate implementation or feasibility tasks.

## Relation To Seq512 Baseline

MVP-28.A baseline:

| Metric | Seq512 SDPA value |
| --- | --- |
| summary tokens/sec | `44100.712407` |
| mean per-step tokens/sec | `46732.188322` |
| average step time | `0.371513s` |
| peak allocated memory | `2.645120 GiB` |
| peak reserved memory | `8.416016 GiB` |
| MFU | unavailable / `null` |

The seq1024 run should be interpreted against this baseline as a memory and throughput preflight, not as quality training.

## New Modal Mode

```text
preflight_5gb_10step_seq1024_sdpa_memory
```

Next-run command, only after a separate cost gate:

```text
modal run scripts/modal_a100_streaming_runner.py --mode preflight_5gb_10step_seq1024_sdpa_memory
```

## Readiness And Artifact Gates

Readiness now distinguishes:

- `training_execution`
- `bounded_sdpa_profile`
- `bounded_seq1024_sdpa_memory_preflight`

The seq1024 memory gate allows only the explicit 10-step config shape:

- `max_steps=10`
- `context_length=1024`
- `batch_size=4`
- `grad_accum=4`
- `attention_backend=sdpa`
- profiling/memory flags enabled
- expected result package name fixed

The post-run artifact validator also has a separate bounded seq1024 memory preflight path. It expects 10 metrics rows, validation rows derived from eval cadence, finite losses, SDPA, seq1024, batch size 4, and GPU memory fields if available. MFU may remain null as a caveat.

## Cost Boundary

This implementation step costs `$0`.

The next real run should be cheaper than the 50-step SDPA profiling run because it runs only 10 steps, though Modal startup, clone, unpacking, and packaging overhead still matter. GPU billing stops after `App completed`; Modal Volume storage costs continue.

## Success Criteria For The Future Run

- Modal app completed
- A100-40GB requested
- no OOM
- finite train loss
- finite validation loss if evaluation runs
- memory fields recorded
- metrics rows equal `10`
- result package generated
- artifact validation blocker count `0`
- no checkpoint or raw tarball committed to git

## Stop Conditions

Stop and report instead of continuing if:

- CUDA OOM occurs
- loss becomes non-finite
- readiness rejects the config
- post-run artifact validation reports blockers
- the run targets 3000/5000/10000 steps
- checkpoint or raw tarball behavior becomes unexpected

## Status

MVP-29.I is preparation only. The real A100 seq1024 memory preflight remains pending a separate explicit run approval.
