# MVP-10 Post-A800 Review and Next-Scale Decision

## 1. Purpose
The purpose of MVP-10 is to review the imported A800 `10-step` and `100-step` results and decide whether the next approved step should prioritize public-corpus expansion, public-tokenizer work, a longer `300M` bounded run, or a larger-model smoke.

This step is decision-only.
It does not run training, rent GPUs, download new data, train a tokenizer, or modify model code.

## 2. What MVP-8 / MVP-9 Proved
The imported MVP-8 and MVP-9 results prove the following bounded engineering facts:
- the public corpus fetch and intake path works for the reviewed FineWeb-Edu `50MB` slice
- the mixed-domain `8k` tokenizer can drive the current public-corpus smoke path
- the `319329280`-parameter model can materialize and run on `A800-SXM4-40GB`
- forward, loss, backward, and optimizer step all work on the reviewed path
- checkpoint save and reload verification works
- metrics and summary artifacts are produced
- A800 `40GB` is sufficient for this `319M` short-run path

Together, MVP-8 and MVP-9 establish that the bounded public-corpus training loop is operational as a training-systems path.

## 3. What They Did Not Prove
The imported results do not prove:
- model quality
- generalization
- final architecture validity
- tokenizer optimality
- that a `50MB` corpus is sufficient
- long-run stability
- that `1B` or `2B` configs can run directly without additional review

These runs are training systems smoke / bounded-run evidence only.
They should not be interpreted as pretraining success.

## 4. Metrics Summary

| Metric | MVP-8 | MVP-9 |
|---|---:|---:|
| max_steps | 10 | 100 |
| parameter_count | 319329280 | 319329280 |
| first_train_loss | 9.181210 | 9.181210 |
| final_train_loss | 2.769437 | 2.413716 |
| final_val_loss | 9.134018 | 8.900962 |
| metrics_rows | 10 | 100 |
| validation_rows | 2 | 5 |
| tokens_seen | 163840 | 1638400 |
| elapsed_seconds | 3.788592 | 33.971051 |
| tokens_per_sec | 43245.612399 | 48229.299267 |
| checkpoint_reload_match | true | true |

## 5. Caveats
The current imported-result line still carries important caveats:
- `core_model_feature_parity=false`
- position encoding mismatch: declared `rope`, implemented `learned_position_embedding`
- `validation_metrics.jsonl` is missing as a separate artifact and validation rows are embedded in `metrics.jsonl`
- MVP-9 `checkpoint_path` has a logging/path mismatch and points into the `10step_execute` directory
- `scheduler_config_present_but_not_applied=true`
- `bounded_prefix_batches_only=true`
- the `50MB` public corpus is tiny and should be treated as a smoke-scale dataset

These caveats do not invalidate MVP-8 or MVP-9 as bounded training-systems evidence, but they do constrain what the project should claim next.

## 6. Decision Options
### A. Direct `300M` `1000-step` run on the same `50MB` corpus
Pros:
- fastest next GPU experiment
- tests longer-run stability on the exact reviewed path

Cons:
- likely overfits the tiny corpus
- does not improve data quality or tokenizer quality
- extends a known smoke-scale setup instead of strengthening the pretraining substrate

Decision:
- not the first recommendation

### B. Expand public corpus to `500MB`
Pros:
- improves data scale materially while staying bounded
- still manageable for reviewed intake and smoke workflows
- strengthens the substrate for both longer `300M` runs and later tokenizer work

Cons:
- requires additional fetch and intake time
- requires another bounded data review step

Decision:
- recommended next data step

### C. Train a public `16k` tokenizer
Pros:
- better matches the FineWeb-Edu / public-English path than the current mixed-domain tokenizer
- improves future public-corpus pretraining alignment
- reduces reliance on a tokenizer trained for a different corpus mixture

Cons:
- adds an extra step before the next GPU training stage
- should ideally follow a larger public slice so the tokenizer is not still tuned on too-small a corpus

Decision:
- recommended after `500MB` expansion, or at minimum after a larger reviewed public slice such as `100MB` or `500MB`

### D. `1B` `10-step` smoke
Pros:
- tests larger-model materialization and memory behavior
- gives useful scaling signal beyond the current `319M` path

Cons:
- should come after the architecture/config caveats are reviewed
- would otherwise compound uncertainty from declared-vs-implemented feature mismatch
- does not solve the data and tokenizer limitations first

Decision:
- secondary recommendation after public-corpus expansion plus tokenizer decision

## 7. Recommended Next Route
Recommended route:
- MVP-11: FineWeb-Edu `500MB` public corpus fetch/intake plan
- MVP-12: public-corpus `16k` tokenizer training plan
- MVP-13: `300M` `1000-step` bounded run on the larger public corpus
- MVP-14: `1B` `10-step` smoke after config/model caveat review

Not recommended as the immediate next step:
- direct `1000-step` run on the current `50MB` corpus
- any `1B` run before config/model caveat review
- H200/B200 escalation
- long training

The main reason is sequencing: the next constraint is no longer whether the current `319M` loop can run, but whether the data substrate, tokenizer alignment, and config/logging claims are strong enough to justify broader scaling.

## 8. What MVP-10 Does Not Do
MVP-10 does not:
- run training
- use a GPU
- download new data
- train a tokenizer
- change model code

## 9. Next Step
Recommended next step:
- MVP-11 FineWeb-Edu `500MB` public corpus expansion plan
