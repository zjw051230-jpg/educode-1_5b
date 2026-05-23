# MVP-8 + MVP-9 A800 Training Summary

## 1. Purpose
This document summarizes the imported remote A800-SXM4-40GB results for the FineWeb-Edu `50MB` public-corpus `319M` training-system validation line.

The summary covers:
- MVP-8 `10-step` training smoke
- MVP-9 `100-step` bounded run

## 2. Shared Run Setup
Shared properties across both runs:
- hardware class: `A800-SXM4-40GB`
- corpus: `FineWeb-Edu 50MB public corpus`
- tokenizer: `educode_bpe_mixed_domain_8k`
- parameter_count: `319329280`
- runtime_device: `cuda`
- runtime_dtype: `bf16`
- public-corpus training path only

## 3. MVP-8 vs MVP-9
| Metric | MVP-8 | MVP-9 |
|---|---:|---:|
| max_steps | 10 | 100 |
| first_train_loss | 9.181210 | 9.181210 |
| final_train_loss | 2.769437 | 2.413716 |
| final_val_loss | 9.134018 | 8.900962 |
| loss_all_finite | true | true |
| val_loss_all_finite | true | true |
| grad_all_finite | true | true |
| checkpoint_reload_match | true | true |
| metrics_rows | 10 | 100 |
| validation_rows | 2 | 5 |
| tokens_seen | 163840 | 1638400 |
| approximate_tokens_per_sec | 43245.612399 | 48229.299267 |

## 4. Interpretation
MVP-8 proves the shortest reviewed remote training smoke can complete successfully on the public-corpus path.

MVP-9 extends that result and adds more evidence of short-range stability across repeated optimizer steps, repeated metric writes, repeated validation hooks, and checkpoint reload verification.

Neither run should be interpreted as model-quality evidence.
These are training systems smoke / bounded run results only.

## 5. Caveats
Shared caveat:
- `core_model_feature_parity=false` because the config declares `rope` while the current core model path still uses `learned_position_embedding`

MVP-8 caveat:
- validation rows are embedded in `metrics.jsonl`; no standalone `validation_metrics.jsonl` was written

MVP-9 caveats:
- validation rows are embedded in `metrics.jsonl`; no standalone `validation_metrics.jsonl` was written
- `checkpoint_path` in `summary.json` points into the `10step_execute` directory even though the `100-step` run itself succeeded and `checkpoint_reload_match=true`

## 6. Artifact Policy
This import step commits only:
- imported small result artifacts
- validation summaries
- reports and receipts

This import step does not commit:
- checkpoints
- tar.gz bundles
- raw data
- processed/splits large local artifacts

## 7. Next Step
Recommended next step:
- treat MVP-8 and MVP-9 as evidence that the reviewed FineWeb-Edu public-corpus training loop is operational at the current `319M` scale, then decide whether the next bounded step should target longer reviewed stability or a cleaner architecture-alignment pass before broader claims
