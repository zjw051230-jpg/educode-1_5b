# W10.5 Sequence Dataset x/y Only

## 1. Purpose
This step only implements next-token sequence dataset construction using Python lists.

## 2. Files Added
- `src/educode/sequence_dataset.py`
- `scripts/inspect_sequence_dataset.py`

## 3. x/y Construction Formula
For token ids and sequence length `L`:
- `x = token_ids[i : i + L]`
- `y = token_ids[i + 1 : i + L + 1]`

Only full-length samples are kept.

## 4. What It Does Not Do
This step does not:
- import torch
- return torch tensors
- pad sequences
- shuffle samples
- run training
- initialize a model
- compute loss
- run backward
- initialize an optimizer
- initialize checkpoints
- do generation
- write dataset files

## 5. Test Command
Executed command:

```text
python D:/Projects/educode-1_5b/scripts/inspect_sequence_dataset.py
```

## 6. Observed Result
- `inspect_sequence_dataset.py` ran successfully
- token count was `227`
- sequence length was `16`
- sample count was `211`
- batch size was `4`
- full batch count was `52`
- the first `x` and `y` each had length `16`
- decoded previews showed that `y` is `x` shifted one token to the right

## 7. Learning Note
- `target_ids` is `input_ids` shifted one token to the right

## 8. Next Step
Suggested W10.6:
- tiny model forward only
- still do not compute loss
- still do not train
