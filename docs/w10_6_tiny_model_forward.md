# W10.6 Tiny Model Forward Only

## 1. Purpose
This step only implements a tiny decoder-only Transformer forward path for shape and finite-value checking.

## 2. Files Added
- `src/educode/tiny_model.py`
- `scripts/inspect_tiny_model_forward.py`

## 3. What It Does
This step:
- builds a tiny model config from the existing JSON config
- initializes a tiny dense decoder-only Transformer
- maps `input_ids -> logits`
- checks logits shape
- checks whether logits are finite

## 4. Current Tiny Model Design
The current tiny model includes:
- token embedding
- learned position embedding
- RMSNorm
- causal self-attention via PyTorch SDPA
- SwiGLU MLP
- decoder blocks
- final norm
- `lm_head`

Notes:
- learned position embedding is a temporary implementation for W10.6
- RoPE will be introduced later
- FlashAttention-2 will be considered later on A100 / B200 lines
- this is not the final 1.5B model, only a smoke forward model

## 5. What It Does Not Do
This step does not:
- compute loss
- run backward
- perform an optimizer step
- save checkpoints
- do generation
- run training
- implement RoPE
- implement FlashAttention-2
- implement MoE
- implement distributed training

## 6. Test Command
Executed command:

```text
python D:/Projects/educode-1_5b/scripts/inspect_tiny_model_forward.py
```

## 7. Observed Result
- `inspect_tiny_model_forward.py` ran successfully
- device was `cuda`
- `input_ids` shape was `(4, 16)`
- logits shape was `(4, 16, 8192)`
- expected logits shape was `(4, 16, 8192)`
- parameter count was `8423680`
- logits finite check was `True`
- the forward smoke check succeeded

## 8. Learning Note
- the model input is token ids
- embeddings are produced inside the model
- the model output is logits
- logits shape is `[B, T, vocab_size]`
- loss will later be computed from logits and `target_ids`
- the dataset does not compute loss, and the current model step does not compute loss

## 9. Next Step
Suggested W10.7:
- loss only
- use logits and `target_ids` to compute next-token cross entropy
- still do not run backward
- still do not initialize an optimizer
