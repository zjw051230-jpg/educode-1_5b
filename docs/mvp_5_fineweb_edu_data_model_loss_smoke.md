# MVP-5 FineWeb-Edu Data / Model / Loss Smoke

## 1. Purpose
The purpose of MVP-5 is to verify the shortest bounded integration path from the FineWeb-Edu public-corpus train/val local artifacts through the existing mixed-domain tokenizer, the tiny decoder-only model forward pass, and next-token cross-entropy loss computation.

## 2. Input Data
Input artifacts used:
- `data/public_corpus/fineweb_edu_sample10bt_50mb/intake_summary.json`
- `data/public_corpus/fineweb_edu_sample10bt_50mb/intake_validation_summary.json`
- `data/public_corpus/fineweb_edu_sample10bt_50mb/splits/fineweb_edu_50mb.train.jsonl`
- `data/public_corpus/fineweb_edu_sample10bt_50mb/splits/fineweb_edu_50mb.val.jsonl`

Observed corpus counts:
- train_docs: `10503`
- val_docs: `567`

## 3. Tokenizer Decision
Tokenizer reused in this smoke step:
- `tokenizers/educode_bpe_mixed_domain_8k/tokenizer.json`

This follows the MVP-4 decision to reuse the existing mixed-domain `8k` tokenizer for the shortest smoke path rather than training a new public-corpus tokenizer.

## 4. Smoke Config
Config created:
- `configs/windows/fineweb_edu_50mb_mixed_tokenizer_smoke.json`

Key settings:
- `run_name=fineweb_edu_50mb_mixed_tokenizer_smoke`
- `train_path=data/public_corpus/fineweb_edu_sample10bt_50mb/splits/fineweb_edu_50mb.train.jsonl`
- `val_path=data/public_corpus/fineweb_edu_sample10bt_50mb/splits/fineweb_edu_50mb.val.jsonl`
- `tokenizer_path=tokenizers/educode_bpe_mixed_domain_8k/tokenizer.json`
- `vocab_size=8192`
- `sequence_length=128`
- `batch_size=4`
- `seed=336`
- `no_training=true`

## 5. Data Batch Check
Smoke script created:
- `scripts/inspect_fineweb_edu_data_model_loss_smoke.py`

Observed batch result:
- `input_ids shape = (4, 128)`
- `targets shape = (4, 128)`
- tokenizer vocab size: `8192`

This confirms that the FineWeb-Edu public train split could be encoded and converted into a full next-token batch with the reused mixed-domain tokenizer.

## 6. Model Forward Check
Observed model forward result:
- `logits shape = (4, 128, 8192)`
- `device = cuda`

The bounded tiny decoder-only forward pass completed successfully.

## 7. Loss Check
Observed loss result:
- `loss_value = 9.149983406066895`
- `loss_finite = true`

This confirms the data → tokenizer → model → next-token loss path is numerically valid for the current bounded public-corpus smoke.

## 8. Result Summary
Summary artifact written:
- `data/public_corpus/fineweb_edu_sample10bt_50mb/fineweb_edu_data_model_loss_smoke_summary.json`

Recorded summary fields include:
- train_docs
- val_docs
- tokenizer_path
- tokenizer_vocab_size
- sequence_length
- batch_size
- input_ids_shape
- logits_shape
- loss_value
- loss_finite
- device
- no_backward
- no_optimizer_step
- no_checkpoint
- no_training

## 9. What MVP-5 Does Not Do
MVP-5 does not:
- train a tokenizer
- train a model
- run backward
- run an optimizer step
- save a checkpoint
- enter A100
- commit `raw.jsonl`
- commit the local `processed/` or `splits/` artifacts

## 10. Next Step
Recommended next step:
- `MVP-6 A100 300M 10-step smoke plan`

That next step should turn this local public-corpus smoke success into an explicit A100-side execution plan, still keeping tokenizer reuse and bounded scope under control.