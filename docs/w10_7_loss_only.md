# W10.7 Loss Only

## 1. Purpose
This step only implements next-token cross entropy loss.

## 2. Files Added
- `src/educode/losses.py`
- `scripts/inspect_loss.py`

## 3. What It Does
This step:
- accepts logits with shape `[B, T, V]`
- accepts `target_ids` with shape `[B, T]`
- reshapes them to `[B*T, V]` and `[B*T]`
- computes cross entropy
- returns a scalar loss tensor

## 4. What It Does Not Do
This step does not:
- run backward
- perform an optimizer step
- save checkpoints
- do generation
- run a training loop
- update parameters

## 5. Test Command
Executed command:

```text
python D:/Projects/educode-1_5b/scripts/inspect_loss.py
```

## 6. Observed Result
- `inspect_loss.py` ran successfully
- device was `cuda`
- `input_ids` shape was `(4, 16)`
- `target_ids` shape was `(4, 16)`
- logits shape was `(4, 16, 8192)`
- loss value was `9.091713`
- loss finite check was `True`

## 7. Learning Note
- the model outputs logits, not probabilities
- cross entropy handles logits directly
- `target_ids` is `input_ids` shifted one token to the right
- an untrained model loss is often near `ln(vocab_size)`
- for `vocab_size = 8192`, `ln(8192)` is about `9.01`
- this step only shows that loss can be computed correctly, not that the model has learned

## 8. Next Step
Suggested W10.8:
- backward + optimizer step only
- run one backward pass
- check whether parameters change
- still do not run a full training loop
