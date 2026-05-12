# T2.3 BPE Tokenizer Integration Smoke

## 1. Purpose
The purpose of T2.3 is to verify that the tiny BPE tokenizer artifact can enter the dataset/model/loss smoke path.
This step checks BPE tokenizer integration only.

## 2. Files Added
- `src/educode/bpe_tokenizer.py`
- `scripts/inspect_bpe_integration_smoke.py`

## 3. What It Does
This step:
- loads `tokenizers/educode_bpe_toy_512/tokenizer.json`
- performs BPE encode/decode through `BPETokenizer`
- builds x/y next-token samples with the existing dataset utilities
- initializes a tiny model with `vocab_size = 311`
- runs one forward pass
- computes one next-token loss value

## 4. What It Does Not Do
This step does not:
- train the model
- run backward
- run an optimizer step
- save checkpoints
- run generation
- modify `ByteTokenizer`
- modify the formal config
- replace the training loop
- download data or models

## 5. Test Command
```text
python scripts/inspect_bpe_integration_smoke.py
```

## 6. Observed Result
- tokenizer path: `tokenizers/educode_bpe_toy_512/tokenizer.json`
- vocab_size: `311`
- token count: `31`
- sequence_length: `16`
- batch_size: `2`
- input_ids shape: `(2, 16)`
- logits shape: `(2, 16, 311)`
- loss value: `5.944768`
- loss finite check: `True`
- round trip summary:
  - `hello world` -> `True`
  - `Transformer models predict the next token.` -> `True`
  - `Python code: print('hello')` -> `True`
  - `loss = F.cross_entropy(logits, targets)` -> `True`

## 7. Current Limitations
- the toy BPE vocab is `311`, not the final `8k`
- the sample corpus is tiny
- this path is not yet integrated into a real training script
- `configs/windows/smoke_cuda_10m.json` still declares the formal `8192` BPE target
- this is only an integration smoke step

## 8. Next Step
Recommended next step:
- T2.4: formal tokenizer config plan / config schema update

Suggested scope:
- add `tokenizer.path`
- add `tokenizer.artifact_dir`
- add validator checks for tokenizer path
- still do not claim real training yet
