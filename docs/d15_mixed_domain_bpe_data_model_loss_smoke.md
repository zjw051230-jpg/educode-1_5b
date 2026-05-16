# D15 Mixed/Domain BPE Data/Model/Loss Smoke

## 1. Purpose
The purpose of D15 is to verify the shortest forward-only integration path across the approved `mixed_domain_external` processed corpus, the mixed/domain BPE tokenizer artifact, the tiny decoder-only model forward pass, and the next-token loss function.

This step is a smoke validation only.
It does not train a model, run backward, update parameters, or save checkpoints.

## 2. Files Added
- `configs/windows/bpe_mixed_domain_8k_smoke.json`
- `scripts/inspect_mixed_domain_bpe_data_model_loss_smoke.py`
- `docs/d15_mixed_domain_bpe_data_model_loss_smoke.md`

## 3. Corpus Used
Processed corpus:
- `data/real_corpus/processed/mixed_domain_external.processed.jsonl`

Selection rule:
- use records with `split = train` only

Observed corpus usage:
- train docs: `52`
- train source counts: `{"external_general_text": 11, "synthetic_examples": 41}`
- total token count after BPE encoding: `42044`
- sequence length used: `128`
- batch size used: `4`

Source-category guard result:
- expected train source categories were present: `synthetic_examples` and `external_general_text`
- `external_general_text` remained smaller than `synthetic_examples` in the train split

The `external_general_text` portion remained supplement only inside the approved mixed corpus.

## 4. Tokenizer Used
Smoke config:
- `configs/windows/bpe_mixed_domain_8k_smoke.json`

Tokenizer artifact:
- `tokenizers/educode_bpe_mixed_domain_8k/tokenizer.json`

Observed tokenizer properties:
- tokenizer type: `BPE`
- tokenizer vocab size: `8192`
- model vocab size: `8192`

## 5. Observed Result
Observed smoke output:
- seed: `42`
- input_ids shape: `(4, 128)`
- logits shape: `(4, 128, 8192)`
- loss value: `9.161793`
- loss finite: `true`
- device: `cuda`

Result:
- `success: mixed/domain BPE processed-data model/loss smoke passed`

This confirms that the approved mixed corpus, the mixed/domain tokenizer artifact, and the tiny forward/loss path remain shape-compatible and numerically valid in a no-grad smoke setting.

## 6. Comparison with Previous BPE Smokes
Previous domain BPE smoke:
- D10 tokenizer vocab: `3988`

Current mixed/domain BPE smoke:
- D15 tokenizer vocab: `8192`
- D15 train docs: `52`
- D15 train source categories: `synthetic_examples` plus `external_general_text`

Interpretation:
- the mixed/domain smoke validates the forward/loss path against a larger observed vocabulary than the earlier domain-only smoke
- the mixed corpus broadened tokenizer and data coverage while keeping `external_general_text` supplement only
- this remains a wiring and numerical-stability check, not a model-quality claim

## 7. What It Does Not Do
This step does not:
- download data
- copy external corpora
- train a tokenizer
- train a model
- run backward
- perform an optimizer step
- save a checkpoint
- generate text
- modify model code
- perform `git push`

## 8. Current Limitations
- this remains a smoke test on a small approved mixed corpus
- finite loss does not imply useful model quality or downstream convergence
- the mixed corpus still uses `external_general_text` as a small supplement only, not a general-language backbone
- this step validates forward/loss compatibility only, not repeated training behavior

## 9. Next Step
Recommended next step:
- prepare a bounded mixed/domain BPE small-training plan while keeping `external_general_text` supplement only
