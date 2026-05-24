# MVP-17 Streaming Batch Iterator Plan

## Goal

MVP-17 should replace run-sized host-side batch materialization with a streaming batch iterator for the A100/A800 public16k training script.

The goal is to restore reasonable batch settings without requiring Python to hold millions of overlapping sample lists in host RAM.

## Current Suspected Issue

The current path builds batches through:

```text
extract_bounded_batches -> make_next_token_samples -> batch_samples
```

This path collects token IDs into a large list, creates every overlapping next-token sample, batches all available samples, and only then slices the required number of batches.

For the original public16k `1000-step` config, MVP-16 inspection estimated roughly `129 GiB` of Python precompute pressure, even though the actual input and label tensor payload for the requested batches is around `250 MiB`.

## Proposed API

Add focused iterator utilities, likely outside the model core:

```python
def iter_jsonl_texts(path: Path) -> Iterator[str]:
    ...
```

Responsibilities:

- stream JSONL lines;
- validate `source_category`, `license`, and `allowed_for_training` at the data boundary;
- yield text strings one at a time;
- avoid retaining previous records.

```python
def iter_token_blocks(
    text_iter: Iterator[str],
    tokenizer: Tokenizer,
    sequence_length: int,
    eos_token_id: int | None,
) -> Iterator[tuple[list[int], list[int]]]:
    ...
```

Responsibilities:

- tokenize incoming text incrementally;
- append EOS when configured;
- keep a small rolling token buffer;
- yield one `x`/`y` block at a time;
- avoid creating all sliding-window samples.

```python
def iter_batches(
    token_block_iter: Iterator[tuple[list[int], list[int]]],
    batch_size: int,
) -> Iterator[tuple[list[list[int]], list[list[int]]]]:
    ...
```

Responsibilities:

- collect only `batch_size` blocks;
- yield one batch;
- clear local batch storage after yield.

```python
def cycle_batches(
    batch_factory: Callable[[], Iterator[Batch]],
    max_batches: int,
) -> Iterator[Batch]:
    ...
```

Responsibilities:

- provide deterministic cycling or restart behavior when bounded data is shorter than requested;
- cap total yielded batches;
- avoid retaining full epoch batches.

## Memory Behavior

The MVP-17 implementation should guarantee:

- no full batch list for the entire run;
- no full tokenized corpus in memory;
- no full list of overlapping sliding-window samples;
- no full validation batch list unless the cache is explicitly small;
- only a small rolling token buffer plus the current microbatch.

The intended steady-state host memory should scale with:

```text
O(batch_size * sequence_length + rolling_token_buffer)
```

not:

```text
O(max_steps * gradient_accumulation_steps * batch_size * sequence_length)
```

and definitely not with every overlapping token offset in the run-sized prefix.

## Test Plan

Use test-driven implementation for the iterator utilities.

Required tests:

1. Tiny JSONL unit test:
   - create a temporary JSONL with a few valid records;
   - confirm `iter_jsonl_texts` yields only approved text.
2. Shape test:
   - use a tiny tokenizer or controlled token sequence;
   - confirm each batch has `batch_size` rows and `sequence_length` tokens per row.
3. Reproducibility test:
   - with a fixed seed and deterministic input order, confirm the first N batches match across repeated iterator construction.
4. One-batch loss comparison:
   - compare one batch from the current path and streaming path on a tiny fixture where equivalent ordering is expected.
5. Memory behavior test:
   - ensure iterator functions return iterators and do not expose a full list of batches.

## Integration Plan

Preserve the existing script interface:

```text
.venv/Scripts/python.exe scripts/run_a100_300m_fineweb_edu_10step_training.py --config <config>
```

Add a config flag:

```json
"data_loading_mode": "streaming"
```

Recommended integration sequence:

1. Implement streaming iterator utilities and tests.
2. Add dry-run support that reports streaming memory plan fields.
3. Add script branch for `data_loading_mode = streaming`.
4. Keep the current list-based path as the default until streaming tests pass.
5. Switch the A800 public16k configs to streaming only after a local smoke confirms batch formation and one-batch loss.
6. Run a short GPU execution before another `3000-step` larger-batch run.

## Risks

| risk | mitigation |
|---|---|
| data order changes | define deterministic iterator order and test first batches |
| reproducibility differences | seed any shuffle/cycle behavior and record mode in summary |
| throughput regression | measure tokens/sec separately from memory correctness |
| gradient accumulation interaction | test microbatch counting and tokens_seen accounting |
| validation drift | make validation iterator deterministic or use a small explicit validation cache |
| accidental model-quality claims | keep reports framed as systems validation until data/sampling quality improves |

## Success Criteria

MVP-17 should be considered ready only when:

- unit tests pass;
- local data/model/loss smoke passes with streaming mode;
- memory inspection shows no run-sized batch list;
- summary artifacts record the active `data_loading_mode`;
- the first GPU retry uses a short bounded run before larger-step execution.

## Implementation Result

MVP-17 implemented the streaming iterator path, switched the public16k 1000/3000-step configs to `data_loading_mode = "streaming"`, and validated the path locally with unit tests, streaming memory inspection, data/model/loss smoke, and dry-runs.

The next execution-facing document is `docs/mvp_18_a800_streaming_1000step_execution_plan.md`.
