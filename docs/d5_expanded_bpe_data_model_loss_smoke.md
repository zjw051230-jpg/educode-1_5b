# D5 Expanded BPE Data / Model / Loss Smoke

## 1. Purpose
The purpose of D5 is to verify that the processed expanded synthetic corpus, the expanded BPE tokenizer artifact, the tiny decoder-only model forward path, and the next-token loss function remain connected.

This is a bounded forward/loss smoke only.
It does not perform backward, optimizer stepping, checkpoint saving, or generation.

## 2. Files Added
- `configs/windows/bpe_expanded_8k_smoke.json`
- `scripts/inspect_expanded_bpe_data_model_loss_smoke.py`
- `docs/d5_expanded_bpe_data_model_loss_smoke.md`

## 3. Corpus Used
Input corpus:
- `data/real_corpus/processed/synthetic_expanded.processed.jsonl`

Selection rule:
- use only records with `split = train`

Observed result:
- train docs: `13`
- total token count after BPE encoding: `2142`
- sequence_length used: `128`
- batch_size used: `4`

## 4. Tokenizer Used
Tokenizer artifact:
- `tokenizers/educode_bpe_expanded_8k/tokenizer.json`

Observed tokenizer state:
- tokenizer vocab size: `1846`
- special token set remained aligned with the D4 artifact

## 5. Observed Result
Smoke config:
- `configs/windows/bpe_expanded_8k_smoke.json`

Observed runtime result:
- config validation passed with `repo_root=PROJECT_ROOT`
- device: `cuda`
- `input_ids` shape: `(4, 128)`
- `logits` shape: `(4, 128, 1846)`
- loss value: `7.641596`
- loss finite: `True`
- decoded preview was produced successfully
- status: success

This confirms that the expanded processed corpus and expanded BPE tokenizer can drive a bounded tiny-model forward pass and next-token loss computation without training.

## 6. What It Does Not Do
This step does not:
- download data
- copy external corpora
- train a tokenizer
- train a model
- run backward
- run an optimizer step
- save a checkpoint
- run generation
- modify model code
- perform `git push`

## 7. Current Limitations
- the smoke path uses a tiny bounded model configuration rather than a training-scale setup
- the corpus is still small synthetic educational data
- only the first full batch is checked in this smoke
- a finite loss confirms path connectivity, not model quality
- this step validates integration at forward/loss level only

## 8. Next Step
Recommended next step:
- D6 expanded corpus small training plan
