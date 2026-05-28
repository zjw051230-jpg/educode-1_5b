# MVP-25.B Validation Coverage Fix

## Scope

MVP-25.B fixes validation measurement coverage for future streaming runs. This step only changes local code, configs, validation script, and documentation. It does not run Modal, does not enter GPU hosts, does not run training, and does not make model-quality claims.

## MVP-25.A finding

MVP-25.A closed the train-side prefix-only issue for the 5GB 1000-step Modal run:

- `train_sampling_policy=shuffle_buffer`
- `sampling_policy=shuffle_buffer`
- `shuffle_seed=1337`
- `shuffle_buffer_size=1024`
- `bounded_prefix_batches_only=false`

However, validation still used:

- `val_sampling_policy=sequential_prefix`
- `val_data_probe.docs_used=1`
- `val_data_probe.records_seen=1`
- `validation_rows=10`

That meant the run had valid artifact health evidence, but weak validation-loss representativeness. The validation loss was produced from a narrow sequential-prefix slice and could not reliably drive a longer-run decision.

## Root cause

The streaming validation path is built in `scripts/run_a100_300m_fineweb_edu_10step_training.py` through `build_split_sampling_settings(config, split_name="val")` and `create_streaming_batch_iterator(...)`.

Before this fix, validation settings always returned:

```python
{
    "sampling_policy": "sequential_prefix",
    "shuffle_seed": None,
    "shuffle_buffer_size": 1,
}
```

The streaming iterator then read `validation_metrics.jsonl` batches by repeatedly calling `next(val_batch_iter)` at each eval interval. `scripts/streaming_lm_batch_iterator.py` tokenized the validation JSONL from the beginning and yielded overlapping next-token blocks from the first available text. Because the first validation document was long enough to provide all `10` validation batches, the iterator never needed to read a second validation document.

The narrow coverage was therefore caused by iterator strategy, not by the number of validation metric rows. Ten validation rows existed, but all could come from one long document.

## Fix

The fix adds validation-specific sampling settings while preserving the existing train sampling behavior.

### Code changes

`build_split_sampling_settings(config, split_name="train")` still uses the existing top-level train `sampling` config, so train-side `shuffle_buffer` behavior is unchanged.

`build_split_sampling_settings(config, split_name="val")` now reads an optional `validation_sampling` block. The 5GB 1000-step and 3000-step configs now declare:

```json
"validation_sampling": {
  "policy": "shuffle_buffer",
  "shuffle_seed": 7331,
  "shuffle_buffer_size": 64,
  "max_blocks_per_document": 8
}
```

`create_streaming_batch_iterator(...)` now accepts `max_blocks_per_document`. When set, `iter_token_blocks(...)` limits how many overlapping token blocks one document may contribute before moving to the next sampled document. This prevents a single long validation document from filling all eval batches.

### Metadata added

Future run summaries now record validation coverage fields:

- `val_sampling_policy`
- `val_shuffle_seed`
- `val_shuffle_buffer_size`
- `validation_max_blocks_per_document`
- `validation_unique_doc_count`
- `validation_batches_evaluated`
- `validation_tokens_evaluated`
- `validation_prefix_only_risk`

The validation data probe also includes:

- `unique_doc_count`
- `max_blocks_per_document`

## Why validation is more trustworthy after this fix

The old validation path measured repeated batches from the beginning of the validation stream. If the first document was long, all validation batches could come from that document.

The new path combines deterministic validation-side shuffle-buffer sampling with a per-document block cap. This improves measurement coverage because:

1. validation documents are sampled with a fixed seed, so results are reproducible;
2. the validation iterator is not forced to stay at the JSONL prefix;
3. one long document cannot dominate all eval batches;
4. summaries explicitly report how many unique validation documents contributed;
5. summaries explicitly mark whether prefix-only risk remains.

This makes validation loss a better measurement-health signal for future runs, but it still does not prove model-quality improvement. It only fixes the measurement path so future comparisons are less biased by a single validation document.

## Local validation

Validator:

```text
scripts/validate_mvp25_b_validation_coverage_fix.py
```

The validator uses a local synthetic JSONL fixture and a fake tokenizer. It does not run Modal, GPU, or training. It verifies that validation-side sampling covers multiple documents and reports the new metadata.

Expected result:

```json
{
  "validation_status": "passed",
  "validation_unique_doc_count": 6,
  "validation_batches_evaluated": 3,
  "validation_tokens_evaluated": 24,
  "val_sampling_policy": "shuffle_buffer",
  "val_shuffle_seed": 7331,
  "val_shuffle_buffer_size": 4,
  "validation_prefix_only_risk": false,
  "blocker_count": 0
}
```

## Follow-up recommendation

Do not jump directly to 5GB 3000-step training until a validation preflight has been run against the prepared 5GB validation split with the new `validation_sampling` config.

Recommended order:

1. Run a local or Modal validation preflight that only checks coverage metadata and confirms `validation_unique_doc_count > 1` with `validation_prefix_only_risk=false`.
2. If the preflight passes, request explicit cost approval for 5GB 3000-step training.
3. Keep 5GB 10000-step deferred until a 5GB 3000-step run shows healthy artifacts and credible validation coverage.
