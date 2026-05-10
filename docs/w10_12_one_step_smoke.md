# W10.12 One-Step Smoke Run

## 1. Purpose
This step verifies one closed-loop smoke step.

## 2. Files Added
- `scripts/run_one_step_smoke.py`

## 3. What It Does
This step:
- loads and validates the Windows smoke config
- creates a run directory
- snapshots `run_config.json`
- writes `run_metadata.json`
- builds one toy batch
- initializes the tiny model
- runs forward
- computes loss
- runs `backward()`
- runs one `optimizer.step()`
- saves one checkpoint
- loads the checkpoint back
- compares model parameters after reload
- runs one generation preview
- writes `metrics.jsonl`
- writes `generation_samples.jsonl`
- writes `summary.md`

## 4. What It Does Not Do
This step does not:
- write a multi-step training loop
- run for many optimizer steps
- run evaluation
- save multiple checkpoints
- perform resume training
- use a real BPE tokenizer yet
- commit generated run artifacts
- do MoE / alignment / RAG / Web UI

## 5. Test Command
Executed command:

```text
python D:/Projects/educode-1_5b/scripts/run_one_step_smoke.py
```

## 6. Observed Result
- `run_one_step_smoke.py` ran successfully
- one run directory was created under `experiments/windows_cuda/`
- `run_metadata.json` existed
- `run_config.json` existed
- `checkpoint.pt` existed
- `metrics.jsonl` existed
- `generation_samples.jsonl` existed
- `summary.md` existed
- one forward / loss / backward / optimizer step completed
- checkpoint reload matched model parameters
- one generation preview was written
- generated run artifacts remained ignored by Git

## 7. Git Tracking Note
- `experiments/<stage>/<run_id>/` is a generated run directory
- checkpoint files and logging outputs from this step are generated artifacts
- generated run artifacts are not committed
- this step only commits the smoke-run script and documentation updates

## 8. Learning Note
- this is the first closed-loop smoke step that connects the earlier isolated W10.x pieces
- the current tokenizer path is still `ByteTokenizer` on toy text, not the final config-declared BPE path
- one successful step proves the plumbing works, but it is not evidence of meaningful training quality
- checkpoint reload verification is useful because it confirms the saved model state matches the updated model after the optimizer step

## 9. Next Step
Suggested W10.13:
- multi-step smoke loop
- repeat the same path for a small number of steps
- keep logging, checkpoint, and generation integrated
- still stay far below a real training run
