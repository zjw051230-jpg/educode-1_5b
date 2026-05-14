# D10 Domain BPE Data/Model/Loss Smoke

## 1. Purpose
The purpose of D10 is to verify the shortest forward-only integration path across the refreshed 45-file processed corpus, the new domain BPE tokenizer artifact, the tiny model forward pass, and next-token loss computation.

This step is a smoke validation only.
It does not train a model, run backward, update parameters, or save checkpoints.

## 2. Files Added
- `configs/windows/bpe_domain_8k_smoke.json`
- `scripts/inspect_domain_bpe_data_model_loss_smoke.py`
- `docs/d10_domain_bpe_data_model_loss_smoke.md`

## 3. Corpus Used
Processed corpus:
- `data/real_corpus/processed/synthetic_expanded.processed.jsonl`

Selection rule:
- use records with `split = train` only

Observed corpus usage:
- train docs: `41`
- total token count after BPE encoding: `7487`
- sequence length used: `128`
- batch size used: `4`

## 4. Tokenizer Used
Smoke config:
- `configs/windows/bpe_domain_8k_smoke.json`

Tokenizer artifact:
- `tokenizers/educode_bpe_domain_8k/tokenizer.json`

Observed tokenizer properties:
- tokenizer type: `BPE`
- tokenizer vocab size: `3988`
- model vocab size: `3988`

## 5. Observed Result
Observed smoke output:
- input_ids shape: `(4, 128)`
- logits shape: `(4, 128, 3988)`
- loss value: `8.434178`
- loss finite: `true`
- device: `cuda`

Result:
- `success: domain BPE processed-data model/loss smoke passed`

This confirms that the 45-file processed corpus, the domain tokenizer artifact, and the tiny forward/loss path remain shape-compatible and numerically valid in a no-grad smoke setting.

## 6. Comparison with D5 Expanded BPE Smoke
Previous expanded BPE smoke:
- D5 tokenizer vocab: `1846`

Current domain BPE smoke:
- D10 tokenizer vocab: `3988`

Interpretation:
- the new domain tokenizer path is validated against a substantially larger observed vocabulary than the earlier expanded BPE smoke
- the forward/loss path still remains stable after switching the tokenizer and model vocab size to the refreshed domain artifact

## 7. What It Does Not Do
This step does not:
- train a tokenizer
- train a model
- run backward
- perform an optimizer step
- save a checkpoint
- generate text
- modify model code
- perform `git push`

## 8. Current Limitations
- this remains a smoke test on a small synthetic educational corpus
- finite loss does not imply useful model quality or downstream convergence
- the observed tokenizer vocab still remains below the nominal 8192 target because corpus scale is limited
- this step validates forward/loss compatibility only, not repeated training behavior

## 9. Next Step
Recommended next step:
- D11 domain BPE small training plan
