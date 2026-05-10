# W11.3 Bounded 50-Step Toy Training Plan

## 1. Purpose
The purpose of W11.3 is to:
- safely extend W11.1 from a 10-step minimal training loop to a bounded 50-step toy training run
- continue using only the Windows RTX 4060 Ti
- continue using only the toy corpus
- observe a fuller loss logging, checkpoint, generation, and summary flow
- avoid making any model quality claim
- avoid entering real-data training
- avoid entering A100/B200 work
- avoid entering 1.5B training

## 2. Current Baseline
W11.1 and W11.2 have already established:
- 10-step minimal training loop succeeded
- device = `cuda`
- first_loss = `9.139446`
- final_loss = `8.856288`
- loss_all_finite = `True`
- grad_all_finite = `True`
- checkpoint reload match = `True`
- metrics rows = `10`
- W11.2 review accepted

This baseline proves that the tiny training loop can safely repeat for a small number of steps.
It does not prove that the model has learned anything meaningful.
The toy corpus is far too small, and the generation quality is not meaningful.

## 3. 50-Step Toy Training Goal
The bounded 50-step toy training goal is:
- `max_steps = 50`
- toy data only
- `ByteTokenizer` temporary path
- tiny model only
- Windows CUDA only
- record metrics on every step
- save one final checkpoint at the end
- reload the final checkpoint for a sanity check at the end
- run one generation at the end
- write `summary.md` at the end

This is bounded toy training, not formal training.
It must not exceed 50 steps.
It must not switch to real data.
It must not scale up the model.
It must not move to A100/B200.

## 4. Proposed Script Strategy
W11.4 can reuse the existing baseline script:
- `scripts/run_minimal_training_loop.py`

But W11.4 should avoid breaking the already validated W11.1 path.
Two acceptable strategies are:

Option A:
- create `scripts/run_50_step_toy_training.py`

Option B:
- add a CLI parameter such as `--max-steps 50` to `run_minimal_training_loop.py`

Recommended priority:
- Option A

Why Option A is preferred:
- it keeps the W11.1 10-step baseline unchanged
- it avoids accidental regression in an already validated script
- it makes 10-step and 50-step results easier to compare directly

## 5. Allowed Changes in W11.4
If W11.4 is executed later, only the following are allowed:
- create a dedicated 50-step toy training script
- reuse the existing config, toy data, `ByteTokenizer`, dataset path, tiny model, loss, checkpoint, generation, and logging code
- keep `max_steps` fixed at `50`, or default to `50` through a CLI entry point
- record metrics on every step
- save one final checkpoint
- write a summary
- update the experiment index

The following are not allowed:
- modify the tiny model structure
- introduce real data
- introduce new dependencies
- introduce a scheduler
- introduce mixed precision
- introduce gradient accumulation
- introduce distributed training
- introduce BPE, RoPE, or FlashAttention-2

## 6. Metrics to Compare
The later review must record and compare:
- `first_loss`
- `final_loss`
- `min_loss`
- `max_loss`
- `mean_loss`
- `loss_all_finite`
- `grad_all_finite`
- `final_grad_norm`
- `tokens_seen`
- `elapsed_seconds`
- approximate tokens/sec
- GPU memory allocated/reserved
- checkpoint reload match
- generation preview

Important interpretation notes:
- loss does not need to decrease monotonically
- the toy corpus is extremely small, so 50 steps may overfit quickly
- the goal is stability and logging completeness, not model capability

## 7. Success Criteria
### Execution Success
- script runs without crash
- exactly 50 steps complete
- no OOM
- no NaN or Inf loss

### Metrics Success
- `metrics.jsonl` exists
- `metrics.jsonl` has 50 rows
- every row has `step` / `train_loss` / `grad_norm` / `tokens_seen`
- all losses are finite
- all grad norms are finite

### Checkpoint Success
- `checkpoint_final.pt` exists
- checkpoint reload succeeds
- parameter match check passes

### Generation Success
- `generation_samples.jsonl` exists
- prompt and output are recorded
- output may still be poor or contain replacement characters

### Logging Success
- `run_metadata.json` exists
- `run_config.json` exists
- `summary.md` exists
- the summary records the current limitations

## 8. Failure Handling
Failure handling for the later W11.4 run must stay simple and bounded.

OOM:
1. lower `batch_size`
2. lower `sequence_length`
3. return to the 10-step script

NaN / Inf loss:
1. lower `learning_rate`
2. verify target ids
3. verify logits are finite
4. stop the run and write a failure report

Checkpoint failure:
1. verify the directory is ignored by Git
2. verify path permissions
3. avoid committing the checkpoint

Generation decode failure:
1. use safe decode
2. record the limitation

General rule:
- change only one variable at a time
- even a failed run should still write `failure_report.md`

## 9. Boundary Check
W11.3 and W11.4 do not do:
- no real dataset
- no long training
- no A100/B200
- no 1.5B
- no distributed training
- no scheduler
- no gradient accumulation
- no mixed precision
- no BPE integration
- no RoPE
- no FlashAttention-2
- no MoE
- no alignment / RLHF / DPO
- no RAG / Web UI
- no claim of model quality

## 10. Current Limitations
Current limitations remain:
- toy data only
- `ByteTokenizer` temporary path
- config still declares BPE/8192
- learned position embedding, not RoPE
- PyTorch SDPA only
- tiny model only
- no validation set
- generation quality is meaningless
- 50 steps would still be far too small for real learning claims

## 11. Recommended Next Step
Recommended next step:
- W11.4: bounded 50-step toy training script

W11.4 must:
- create or run only a bounded 50-step toy script
- keep artifacts ignored
- write metrics, generation, and summary artifacts
- not proceed to 100-step or real data without a new review
