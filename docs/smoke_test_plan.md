# EduCode-1.5B Smoke Test Plan

## 1. Purpose
The purpose of smoke testing is to:
- verify that code, config, environment, data paths, checkpoint flow, and generation flow can run before formal training
- avoid burning A100 / B200 budget on basic debugging
- clearly separate the roles of Mac / Windows / A100 / B200
- keep the current stage focused on planning rather than running training

## 2. Smoke Test Philosophy
- small first
- fail fast
- one change at a time
- never debug first on B200
- every successful stage must produce logs
- every run must be reproducible from config
- checkpoint / resume must be tested before long training
- generation must be tested before claiming the model works

## 3. Stage W: Windows RTX 4060 Ti Smoke Test
Windows line goals:
- CUDA availability validation
- PyTorch SDPA availability validation
- bf16 sanity check
- small-model forward / backward smoke test
- later LoRA / PEFT preparation

Required constraints:
- Windows does not do 1.5B full pretraining.
- Windows may do 10M-scale smoke tests.
- Planned config: `configs/windows/smoke_cuda_10m.json`

Planned checks:
- config can be read
- tiny dataset can be read
- model can initialize
- forward can run
- loss can be computed
- backward can run
- optimizer step can run
- checkpoint can be saved
- checkpoint can be loaded
- generation can output text

W4 note:
- This stage is planning only. None of the above checks are implemented in W4.

## 4. Stage M: Mac M3 Max Learning Smoke Test
Mac line goals:
- help the user gradually learn tokenizer, model, and training internals
- understand Apple Silicon / MPS behavior
- observe unified memory and CPU / GPU data movement
- validate small-model training behavior

Planned config:
- `configs/mac/tiny_10m.json`

Required constraints:
- Mac is the learning slow line.
- It does not optimize for speed.
- It does not target large models.
- The focus is understanding each module.

Planned checks:
- ByteTokenizer round-trip
- BPE tokenizer train / encode / decode
- dataset x/y construction
- dense Transformer forward
- loss decreases
- checkpoint save / load
- generation demo
- MPS memory / speed observation

## 5. Stage A: A100 CUDA Smoke / Profiling Test
A100 line goals:
- migrate from local small-model experiments to CUDA training conditions
- run 100M / 300M scale experiments
- profile tokens/sec, memory, and attention backend choices
- de-risk B200 training preparation

Planned config:
- `configs/a100/smoke_100m.json`

Planned checks:
- CUDA bf16
- SDPA baseline
- FlashAttention-2 planned but not assumed
- activation checkpointing planned
- tokens/sec logging
- memory logging
- checkpoint resume
- validation loss
- generation samples

## 6. Stage B: B200 1.5B Preflight
B200 line goals:
- B200 is not the first debug machine
- B200 is only used after Windows / Mac / A100 gates pass
- B200 is the main 1.5B training platform

Planned config:
- `configs/b200/educode_1_5b.json`

B200 preflight checklist:
- A100 smoke run has passed
- config has been validated
- tokenizer has been fixed
- data shards have been prepared
- checkpoint / resume has been validated
- logging has been validated
- validation has been validated
- generation has been validated
- storage paths have been confirmed
- budget has been confirmed
- failure recovery strategy has been confirmed

## 7. Minimal Smoke Test Ladder

| stage | hardware | config | parameter scale | token budget | goal | success criteria | not allowed |
|---|---|---|---|---|---|---|---|
| 10M Windows smoke | RTX 4060 Ti 16GB | `configs/windows/smoke_cuda_10m.json` | 10M | tiny smoke budget | verify CUDA path and minimal train loop plumbing assumptions | forward/backward works, checkpoint save/load works, generation path works | no 1.5B training, no long-run profiling |
| 10M Mac learning run | Mac M3 Max 36GB | `configs/mac/tiny_10m.json` | 10M | tiny learning budget | understand tokenizer/model/training pieces on MPS | tokenizer round-trip works, loss is finite, checkpoint and generation demo work | no speed chasing, no large-model scaling |
| 100M A100 smoke | A100 | `configs/a100/smoke_100m.json` | 100M | small smoke budget | validate CUDA training path on datacenter GPU | bf16 works, SDPA works, logs and checkpoints work | no direct jump to 1.5B |
| 300M A100 profiling | A100 | future A100 profiling config | 300M | medium profiling budget | measure tokens/sec, memory, backend behavior | profiling logs exist, validation path works, resume works | no B200 main-run assumptions without data |
| 1.5B B200 short run | B200 | `configs/b200/educode_1_5b.json` | 1.5B | short preflight budget | validate end-to-end preflight on target hardware | short run completes, logs exist, checkpoint exists, generation path works | no full campaign before preflight passes |
| 1.5B B200 main run | B200 | `configs/b200/educode_1_5b.json` | 1.5B | 5B / 10B / 30B token options | formal main training campaign | stable logging, validated resume, tracked evals, generation samples, storage discipline | no debugging of basic environment issues |

## 8. Success Criteria

### Environment success
- CUDA / MPS available
- dtype sanity check passes
- SDPA or attention primitive is available

### Model success
- forward pass works
- loss is finite
- backward works
- optimizer step works

### Training success
- loss decreases
- logs are written
- checkpoint is saved
- checkpoint is loaded

### Generation success
- prompt is accepted
- tokens are generated
- decode works
- output is stored in logs

## 9. Failure Handling
- when OOM happens, reduce batch size first
- then reduce context length
- then disable high-risk features
- do not switch to a bigger GPU as the first reaction
- change only one variable at a time
- every failure record must include config, error, hardware, and commit hash

## 10. What W4 Does Not Do
W4 does not:
- write training code
- run smoke tests
- implement tokenizer / model / training
- install packages
- download models
- do 1.5B training
- do MoE / alignment / RAG / Web UI

## 11. Next Step
Suggested W5 directions:
- create a config validation checklist
- or create a run logging format document
- still do not implement the training mainline
