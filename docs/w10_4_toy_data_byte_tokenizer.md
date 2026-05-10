# W10.4 Toy Data + ByteTokenizer Only

## 1. Purpose
This step only implements toy data and a minimal ByteTokenizer.

## 2. Files Added
- `src/educode/byte_tokenizer.py`
- `src/educode/toy_data.py`
- `scripts/inspect_toy_tokenizer.py`

## 3. What ByteTokenizer Does
The ByteTokenizer:
- converts `str -> UTF-8 bytes -> list[int]`
- converts `list[int] -> bytes -> UTF-8 str`
- supports a round-trip check
- uses `vocab_size = 256`

## 4. What Toy Data Does
Toy data:
- provides a very small toy corpus
- covers English, Chinese, numbers, punctuation, emoji, and CS / ML / code-themed text
- is only for pipeline validation
- does not represent model capability

## 5. What It Does Not Do
This step does not:
- implement BPE
- implement special tokens
- implement tokenizer save/load
- construct dataset x/y
- implement a model
- compute loss
- import torch
- run training
- download data or models

## 6. Test Command
Executed command:

```text
python D:/Projects/educode-1_5b/scripts/inspect_toy_tokenizer.py
```

## 7. Observed Result
- `inspect_toy_tokenizer.py` ran successfully
- `round_trip_ok` was `True`
- token count was `227`
- min token id was `10`
- max token id was `240`
- unique token id count was `62`

## 8. Relation to Mac Learning Line
- In the Mac learning line, the user already manually understood byte-level encode/decode
- The Windows engineering line now turns that minimal concept into a reusable module
- This can later be replaced or extended with a BPE tokenizer

## 9. Next Step
Suggested W10.5:
- dataset x/y only
- use token ids to construct `input_ids` and `target_ids`
- still do not initialize a model
- still do not train
