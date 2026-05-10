# W10.9 Checkpoint Save/Load Only

## 1. Purpose
This step only verifies checkpoint saving and loading.

## 2. Files Added
- `src/educode/checkpoint.py`
- `scripts/inspect_checkpoint.py`

## 3. What It Does
This step:
- saves model state
- saves optimizer state
- saves step
- saves config
- saves metadata
- loads the checkpoint
- restores model and optimizer
- compares model parameters before and after loading

## 4. What It Does Not Do
This step does not:
- write a full training loop
- run multi-step training
- do generation
- do evaluation
- commit checkpoint files
- do distributed checkpointing
- do sharded checkpointing
- do MoE / alignment / RAG / Web UI

## 5. Test Command
Executed command:

```text
python D:/Projects/educode-1_5b/scripts/inspect_checkpoint.py
```

## 6. Observed Result
- `inspect_checkpoint.py` ran successfully
- device was `cuda`
- checkpoint path was `D:/Projects/educode-1_5b/experiments/windows_cuda/checkpoint_inspect_tmp/checkpoint.pt`
- checkpoint file exists was `True`
- step was `1`
- model parameter all_match was `True`
- max_abs_diff was `0.0`
- optimizer state loaded was `True`
- config loaded was `True`
- metadata loaded was `True`

## 7. Git Tracking Note
- checkpoint files are written under an ignored experiment/checkpoint directory
- `.pt`, `.pth`, and `.safetensors` files should not be committed
- Git should only track checkpoint utility code and documentation

## 8. Learning Note
- checkpointing is the basis for resumable training
- saving only model weights is not enough for continuing training; optimizer state also matters
- step, config, and metadata help identify which experiment a checkpoint belongs to
- this step proves save/load works, but it is not yet a full training system

## 9. Next Step
Suggested W10.10:
- generation only
- use the current random model for prompt -> token ids -> logits -> next token -> decode
- do not train
- do not judge generation quality
