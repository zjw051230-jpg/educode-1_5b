# T2.2 Tiny BPE Tokenizer Artifact

## 1. Purpose
The purpose of T2.2 is to train a tiny local BPE tokenizer artifact only for validating the BPE tokenizer artifact path.
This step is not the final formal 8k tokenizer.

## 2. Files Added
- `data/tokenizer_samples/tiny_educode_corpus.txt`
- `scripts/train_tiny_bpe_tokenizer.py`
- `scripts/inspect_tiny_bpe_tokenizer.py`
- `tokenizers/educode_bpe_toy_512/`

## 3. Tokenizer Configuration
- type: `BPE`
- library: Hugging Face `tokenizers`
- vocab_size target: `512`
- observed vocab size: `311`
- min_frequency: `1`
- special tokens:
  - `<pad>`
  - `<bos>`
  - `<eos>`
  - `<unk>`
- artifact path: `tokenizers/educode_bpe_toy_512/`

## 4. What It Does
This step:
- uses a local toy/sample corpus only
- trains a tiny BPE tokenizer with Hugging Face `tokenizers`
- saves tokenizer artifacts under `tokenizers/educode_bpe_toy_512/`
- runs encode/decode inspection on English, Chinese, code, and emoji text

## 5. What It Does Not Do
This step does not:
- download data
- download models
- install new packages
- train a language model
- replace `ByteTokenizer`
- modify model config
- modify the training loop
- represent the final formal 8k tokenizer

## 6. Inspection Results
Summary:
- vocab size: `311`
- special token ids:
  - `<pad>`: `0`
  - `<bos>`: `1`
  - `<eos>`: `2`
  - `<unk>`: `3`
- round_trip_exact = `True` for:
  - `hello world`
  - `你好，世界`
  - `Python code: print('hello')`
  - `Transformer models predict the next token.`
  - `loss = F.cross_entropy(logits, targets)`
  - `Emoji test 😊`
- no round-trip mismatches were observed in the current inspection set

## 7. Current Limitations
- this is a toy tokenizer artifact
- the sample corpus is very small
- vocab target `512` is not the final Windows formal `8k` tokenizer
- Chinese and emoji behavior should still be rechecked on a larger corpus later
- formal training still needs config integration and a real train/validation dataset path

## 8. Next Step
Recommended next step:
- T2.3: BPE tokenizer integration smoke

Suggested scope:
- load the tokenizer artifact
- use the BPE tokenizer in a dataset/model/loss smoke path
- use toy/sample text only
- do not run long training
- do not switch the formal config before the smoke path is accepted
