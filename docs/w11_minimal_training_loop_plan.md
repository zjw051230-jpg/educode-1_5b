# W11 Minimal Training Loop Plan

## 1. Purpose
The purpose of W11 is to:
- extend W10.12 one-step smoke into a strictly bounded minimal training loop
- run only a small-step training check on Windows RTX 4060 Ti
- verify that loss can be logged, checkpoint can be saved, and generation can be called after training
- not pursue model quality
- not enter long training
- not enter A100/B200

## 2. Current Baseline
The following path is already complete:
- config loader
- config validator
- run setup
- toy data
- ByteTokenizer
- sequence x/y dataset
- tiny decoder-only model forward
- next-token cross entropy loss
- backward
- optimizer step
- checkpoint save/load
- generation
- run logging
- one-step smoke run
- one-step smoke review

Most important current conclusions:
- Windows 4060 Ti has passed the one-step smoke milestone
- the project can move into a minimal loop plan
- the project still must not jump to long training or 1.5B work

## 3. Minimal Training Loop Goal
The W11 loop goal is:
- max_steps: 10 or 20
- use toy corpus
- use `configs/windows/smoke_cuda_10m.json`
- use temporary ByteTokenizer path
- use tiny model
- on each step run:
  - get batch
  - forward
  - loss
  - backward
  - optimizer step
  - log metrics
- after training ends:
  - save final checkpoint
  - run one generation prompt
  - write `summary.md`

This is a minimal loop, not formal training.
Loss may fluctuate slightly and does not need to show a clearly meaningful downward curve.
If the loop runs stably, logs completely, and checkpoint reload works, that is success.

## 4. Training Loop Boundaries
Allowed:
- `torch`
- `model.train()`
- AdamW optimizer
- 10-20 steps
- local toy data
- `metrics.jsonl`
- final checkpoint
- final generation sample
- `summary.md`

Forbidden:
- no real large dataset
- no data download
- no pretrained model download
- no long training
- no 1.5B
- no A100/B200
- no distributed training
- no gradient accumulation unless explicitly planned
- no mixed precision complexity unless already safe
- no FlashAttention-2
- no RoPE/BPE integration
- no MoE/alignment/RAG/Web UI

## 5. Proposed Loop Flow
1. load config
2. validate config
3. create run_id
4. create run directory
5. snapshot config
6. write `run_metadata.json`
7. prepare toy corpus
8. ByteTokenizer encode
9. build samples and batches
10. initialize tiny model
11. initialize AdamW
12. for `step in range(max_steps)`:
    - choose batch
    - move `input_ids` / `target_ids` to device
    - `zero_grad`
    - forward
    - loss
    - backward
    - grad norm
    - optimizer step
    - log metrics
13. save final checkpoint
14. reload checkpoint sanity check
15. run generation
16. write `generation_samples.jsonl`
17. write `summary.md`
18. print final report

## 6. Metrics to Log
Required metrics:
- step
- tokens_seen
- train_loss
- learning_rate
- grad_norm
- tokens_per_sec
- gpu_memory_allocated_gib
- gpu_memory_reserved_gib
- elapsed_seconds
- timestamp

Notes:
- `val_loss` can stay `null` for now
- `mfu` can stay `null` for now
- no validation loop is planned here

## 7. Success Criteria
### Execution Success
- script runs without crash
- max_steps completed
- no OOM
- no NaN loss

### Metrics Success
- `metrics.jsonl` exists
- it contains one record per step
- `train_loss` is finite
- `grad_norm` is finite

### Checkpoint Success
- final checkpoint exists
- checkpoint reload succeeds
- model parameters match after reload

### Generation Success
- prompt accepted
- output generated
- `generation_samples.jsonl` exists

### Logging Success
- `run_metadata.json` exists
- `run_config.json` exists
- `summary.md` exists

## 8. Failure Handling
- OOM:
  1. lower `batch_size`
  2. lower `sequence_length`
  3. use CPU fallback only for debugging
- NaN loss:
  1. lower `learning_rate`
  2. check target ids
  3. check logits finite
- checkpoint failure:
  1. verify ignored directory
  2. verify path permissions
- generation decode failure:
  1. use safe decode
  2. record the limitation
- change only one variable at a time
- failed run should still write `failure_report.md`

## 9. Expected Limitations
- toy data only
- ByteTokenizer temporary path
- config says BPE/8192, but current smoke path uses byte token ids within vocab range
- learned position embedding, not RoPE
- SDPA, not FlashAttention-2
- tiny model, not 1.5B
- loss curve is not meaningful yet
- generation quality is meaningless

## 10. Implementation Breakdown
Suggested follow-up breakdown:
- W11.1 create minimal training loop script
- W11.2 run 10-step smoke training
- W11.3 review training logs
- W11.4 cleanup docs and experiment index

Notes:
- W11 only creates the plan
- W11.1 is where script writing would start
- W11.2 is where training would actually run

## 11. What W11 Does Not Do
W11 does not:
- write training loop code
- run training
- modify model code
- download data or models
- do A100/B200 work
- do 1.5B work
- do BPE/RoPE/FlashAttention-2 integration
- do MoE/alignment/RAG/Web UI
- execute `git push`

## 12. Next Step
Suggested next step:
- W11.1 minimal training loop script

W11.1 must still stay strictly bounded:
- max_steps defaults to 10
- toy data only
- no real dataset
- no long training
- no A100/B200
- no 1.5B
