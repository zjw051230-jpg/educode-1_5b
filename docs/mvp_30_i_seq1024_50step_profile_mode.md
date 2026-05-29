# MVP-30.I Seq1024 50-step SDPA Profiling Mode

## Why This Exists

MVP-29 proved that `context_length=1024` is viable on Modal A100-40GB for a short bounded memory preflight at `batch_size=4`, `grad_accum=4`, and `attention_backend=sdpa`.

MVP-30.I extends that shape into a bounded 50-step profiling mode so the project can measure:

- throughput
- step time
- GPU memory
- finite loss sanity
- artifact validation shape

This is still systems profiling, not quality training.

## Difference From MVP-29.I

MVP-29.I was a 10-step memory preflight. It answered:

- does seq1024 OOM at the conservative shape?
- is the memory footprint reasonable?

MVP-30.I goes one level deeper:

- same seq1024 shape
- same `batch_size=4`
- same `grad_accum=4`
- same SDPA backend
- longer bounded run at 50 steps

That longer window is useful for profiling stability, but it is still not long enough to claim training quality.

## Why Not Seq1024 3000-step

Do not jump directly to seq1024 3000-step:

- 10-step and 50-step bounded runs only prove systems viability, not model quality.
- The project should collect profiling evidence first.
- A direct long run would spend more before the systems shape is fully characterized.

## Why Batch Size Stays 4

Keep `batch_size=4` for this mode:

- it preserves the conservative seq1024 shape that already passed no-OOM preflight
- it keeps the run comparable to MVP-29.I
- it avoids introducing a second unknown before the 50-step profile is measured

Seq1024 batch size `8` can be revisited later as a separate memory preflight.

## Why SDPA

Keep `attention_backend=sdpa` because:

- the current production path already uses PyTorch SDPA
- FlashAttention is not part of this step
- the goal is to profile the known backend under longer bounded execution

## Comparison Target

Compare the seq1024 50-step profile against the seq512 50-step SDPA baseline:

- seq512 context length: `512`
- seq512 batch size: `8`
- seq512 avg step time: `0.371513s`
- seq512 peak allocated memory: `2.645120 GiB`
- seq512 peak reserved memory: `8.416016 GiB`

The target is not to claim seq1024 is faster than another backend. The target is to characterize seq1024 SDPA behavior cleanly.

## Cost

This planning step costs `$0`.

The next real Modal A100-40GB run should stay in the low-cost profiling band, but it will still incur startup and packaging overhead.

## Success Criteria

The next real run should succeed if:

- `App completed`
- no OOM
- loss is finite
- `metrics_rows = 50`
- `validation_rows = 1`
- memory and throughput are recorded
- result package is generated
- artifact validation passes

## Stop Conditions

Stop if:

- OOM occurs
- loss becomes non-finite
- artifact validation fails
- checkpoint or tarball handling becomes unexpected

## Next Command

```text
modal run scripts/modal_a100_streaming_runner.py --mode profile_5gb_50step_seq1024_sdpa
```
