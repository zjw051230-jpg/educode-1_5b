# W10.8 Backward + Optimizer Step Only

## 1. Purpose
This step only verifies one backward pass and one optimizer step.

## 2. Files Added
- `scripts/inspect_optimizer_step.py`

## 3. What It Does
This step:
- builds a toy batch
- initializes the tiny model
- runs forward to get logits
- computes next-token cross entropy loss
- runs `loss.backward()`
- runs `optimizer.step()`
- checks whether a parameter changed

## 4. What It Does Not Do
This step does not:
- write a full training loop
- run multi-step training
- save checkpoints
- generate text
- write metrics files
- create a run directory
- run evaluation
- run distributed training
- do MoE / alignment / RAG / Web UI

## 5. Test Command
Executed command:

```text
python D:/Projects/educode-1_5b/scripts/inspect_optimizer_step.py
```

## 6. Observed Result
- `inspect_optimizer_step.py` ran successfully
- device was `cuda`
- `input_ids` shape was `(4, 16)`
- `target_ids` shape was `(4, 16)`
- logits shape was `(4, 16, 8192)`
- loss value was `9.043324`
- loss finite check was `True`
- chosen parameter name was `token_embedding.weight`
- gradient existed and was finite
- the parameter changed after the optimizer step
- max absolute parameter delta was `0.0004019737`

## 7. Learning Note
- forward only computes logits
- loss connects logits and `target_ids`
- backward computes gradients from the loss
- `optimizer.step()` updates parameters using those gradients
- this step proves parameters are learnable, but it does not mean the model is already trained well
- a full training loop would repeat this process many times later

## 8. Next Step
Suggested W10.9:
- checkpoint save/load only
- save model / optimizer / state / config metadata
- load and verify parameter equality
- still do not run a full training loop
