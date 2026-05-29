# MVP-29.P Context Length 1024 Memory Preflight Plan

## Scope

This step plans a context length `512 -> 1024` memory preflight. It does not run Modal, does not request GPU, does not start training, does not create a seq1024 runner mode, and does not produce new runtime results.

## Why MVP-29 Does Context Length 1024

MVP-28 established an A100 SDPA systems baseline at context length `512`. The next useful systems question is whether the current 300M-class model, streaming data path, SDPA attention implementation, and Modal A100-40GB execution path can handle longer sequence length before spending on longer training.

This is more useful than immediately adding more training steps because context length changes the memory and throughput profile of the system. It also improves the project narrative from "ran longer" to "measured and gated a real LLM systems scaling axis."

## Current Seq512 Baseline

Source artifact:

```text
experiments/a100/fineweb_edu_5gb_300m_50step_public16k_sdpa_profile/results_imported_modal_streaming/
```

| Field | Value |
| --- | --- |
| GPU | A100-40GB |
| attention backend | `sdpa` |
| context length | `512` |
| batch size | `8` |
| gradient accumulation | `4` |
| tokens per optimizer step | `16384` |
| max steps | `50` |
| summary tokens/sec | `44100.712407` |
| mean per-step tokens/sec | `46732.188322` |
| average step time | `0.371513s` |
| peak allocated memory | `2.645120 GiB` |
| peak reserved memory | `8.416016 GiB` |
| MFU | unavailable / `null` |

## Expected Impact Of 512 -> 1024

Doubling context length changes several surfaces at once:

- Per microbatch tokens double if batch size stays fixed.
- Attention score memory scales approximately with sequence length squared, so the attention component may grow by about `4x` at the same batch size.
- Activation and logits-related terms also grow with token count, so step time is expected to rise.
- Tokens/sec may drop because each step has more attention work per token.
- Validation tokens per validation batch change with `batch_size * context_length`.

If `batch_size=8` is kept, tokens per optimizer step become:

```text
8 * 1024 * 4 = 32768
```

That doubles the optimizer-step token budget compared with the seq512 baseline. It may fit on A100-40GB, given the seq512 peak reserved memory was only `8.416016 GiB`, but it is not the conservative first probe.

## Memory Risk

The seq512 profile has comfortable A100-40GB headroom, but reserved memory does not prove seq1024 safety. Attention memory can grow sharply with sequence length, and PyTorch SDPA kernel selection may change by shape, dtype, and CUDA runtime.

Recommended first probe:

```text
context_length = 1024
batch_size = 4
gradient_accumulation_steps = 4
max_steps = 10
attention_backend = sdpa
```

This keeps tokens per optimizer step unchanged:

```text
4 * 1024 * 4 = 16384
```

It reduces the first seq1024 memory risk while still exercising the longer context path. The attention component is still expected to be roughly `2x` versus the seq512 batch-8 baseline because sequence length doubles while batch size halves.

## Throughput Risk

Throughput should be expected to fall versus the seq512 SDPA baseline. Step time should increase because each token attends over a longer context. A 10-step memory preflight should focus on whether the run fits, whether losses remain finite, and whether throughput/memory fields are recorded.

Do not interpret 5-10 step losses as model quality.

## Recommended Preflight Design

MVP-29.I should add, but not automatically run, a bounded seq1024 memory preflight config and Modal mode.

Recommended shape:

| Field | Recommendation |
| --- | --- |
| mode | `preflight_5gb_10step_seq1024_sdpa_memory` or similar |
| context length | `1024` |
| max steps | `10` |
| batch size | `4` |
| gradient accumulation | `4` |
| attention backend | `sdpa` |
| data loading | `streaming` |
| train sampling | `shuffle_buffer` |
| validation sampling | `shuffle_buffer` |
| eval cadence | one validation sanity check, if supported |
| checkpoint | prefer disabled for true memory preflight; if current training script requires a final checkpoint, do not import or commit it |
| result package | small JSON/JSONL/Markdown only |

The preflight should record:

- tokens/sec
- step time
- peak allocated memory
- peak reserved memory
- finite train loss
- finite validation loss if validation runs
- artifact validation blocker count

## Batch Size Decision

Recommended first batch size: `4`.

Reasoning:

- It keeps optimizer-step tokens equal to the seq512 baseline when `grad_accum=4`.
- It reduces OOM risk while still testing seq1024 attention and activation behavior.
- It creates a clean memory comparison before trying `batch_size=8`.

`batch_size=8` can be a later throughput probe if the batch-4 memory preflight passes with comfortable headroom.

## Grad Accum Decision

Keep `gradient_accumulation_steps=4` for the first preflight. This preserves the existing optimizer-step structure and avoids changing two knobs at once.

## Attention Backend

Continue using SDPA. The runtime model currently supports only `sdpa` in `src/educode/tiny_model.py`. Naive attention and FlashAttention should remain separate implementation/audit tasks, not part of the first seq1024 memory preflight.

## Cost Boundary

This planning step costs `$0`.

The next A100 memory preflight should be far cheaper than the 50-step SDPA profile because it should run only `5-10` steps. Actual Modal cost may still include startup, clone, package extraction, and result packaging overhead. GPU billing stops after `App completed`; Modal Volume storage cost continues.

## Success Criteria

A future seq1024 memory preflight succeeds if:

- Modal app completes.
- A100-40GB is the requested GPU.
- The run uses `context_length=1024`.
- The run uses SDPA.
- No OOM occurs.
- Metrics rows match the bounded step count.
- Loss values are finite.
- GPU memory fields are recorded.
- The result package contains only small imported artifacts.
- No checkpoint or tarball is committed to git.

## Stop Conditions

Stop and report instead of continuing if:

- CUDA OOM occurs.
- readiness checks reject the config.
- post-run artifact validation fails.
- losses become non-finite.
- the mode accidentally targets 3000/5000/10000 steps.
- the result package tries to include checkpoint weights.

## Why Not Direct Seq1024 3000-step

Do not run seq1024 3000-step directly:

- seq1024 changes the memory regime and throughput profile.
- The current validated quality-training result is still seq512.
- The current SDPA baseline is a 50-step profile, not a seq1024 proof.
- A 3000-step seq1024 run would multiply cost before proving memory safety.
- A short preflight gives better engineering evidence and clearer failure boundaries.

## Recommendation

Proceed to:

```text
MVP-29.I add seq1024 10-step SDPA memory preflight config/mode
```

Do not run the mode until a separate cost gate explicitly approves Modal A100 execution.
