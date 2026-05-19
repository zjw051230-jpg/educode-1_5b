# D18 Batch 04 Worker Aggregation Summary

## 1. Purpose
This summary records the worker-level aggregation view for batch_04 and highlights where the authoritative validator counts matched the worker-reported delivery summaries.

## 2. Expected vs Observed Worker Counts
| worker_id | worker_directory | manifest_rows | markdown | python | progress_files | validation_result | quality_result |
|---|---|---:|---:|---:|---:|---|---|
| `CC-1` | `cc1_ml_foundations` | 1000 | 700 | 300 | 10 | passed | 1000 pass / 0 notes |
| `CC-2` | `cc2_python_data_systems` | 1000 | 700 | 300 | 10 | passed | 0 pass / 1000 notes |
| `CC-3` | `cc3_transformer_architecture` | 1000 | 700 | 300 | 10 | passed | 0 pass / 1000 notes |
| `CC-4` | `cc4_training_runtime_systems` | 1000 | 700 | 300 | 10 | passed | 1000 pass / 0 notes |
| `CC-5` | `cc5_bilingual_qa` | 1000 | 850 | 150 | 10 | passed | 150 pass / 850 notes |
| `CC-6` | `cc6_code_snippets` | 1000 | 300 | 700 | 10 | passed | 700 pass / 300 notes |

Batch-level totals:
- manifest rows: `6000`
- markdown files: `3950`
- python files: `2050`
- validation failures: `0`
- quality rejects: `0`

## 3. Manifest Normalization Notes
The six worker deliveries were internally consistent in intent, but not identical in manifest schema.

Observed manifest styles:
- `CC-1` and `CC-2`: `filename` + `subdirectory`
- `CC-3`: `proposed_filename` + `subcategory`
- `CC-4`: full repo-relative `path` plus `md` / `py` file-type tags
- `CC-5`: full repo-relative `filename` plus `subdir`
- `CC-6`: `relative_path` + `subcategory`

The D18 validator normalized these shapes before checking counts, file paths, metadata, and worker scope.

## 4. Progress-File Naming Differences
Worker progress logs also used different naming conventions:
- `CC-1` / `CC-2`: `progress_0100.md` style
- `CC-3` / `CC-4` / `CC-5`: `progress_checkpoint_0100.md` style
- `CC-6`: `progress_checkpoint_01_0100.md` style

Important interpretation:
- D18 did not assume one checkpoint filename pattern
- D18 treated the authoritative requirement as `10` progress files per worker, regardless of the worker-local naming style

## 5. Quality Concentration by Worker
The automated quality notes were not evenly distributed.

Cleaner-control workers:
- `CC-1`: all `1000` files recorded as `quality_pass`
- `CC-4`: all `1000` files recorded as `quality_pass`

Higher-note workers:
- `CC-2`: all `1000` files recorded as `needs_edit`
- `CC-3`: all `1000` files recorded as `needs_edit`
- `CC-5`: the `850` markdown files carried the note concentration, while `150` python files passed cleanly
- `CC-6`: the `300` markdown files carried the note concentration, while `700` python files passed cleanly

Dominant note themes:
- repeated internal lines
- templated opening families
- dense boilerplate in markdown review-note scaffolds

## 6. Interpretation
Authoritative D18 result:
- all six workers delivered complete `1000`-file batches
- all worker summaries matched validator-observed counts
- no worker under-delivered
- no worker escaped the draft-only governance rules

Operational follow-up result:
- `CC-1` and `CC-4` are useful baseline/control groups for human review
- `CC-2`, `CC-3`, `CC-5` markdown, and `CC-6` markdown should receive the first manual template-reduction review pass
