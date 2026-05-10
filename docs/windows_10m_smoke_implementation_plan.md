# Windows 10M Smoke Test Implementation Plan

## 1. Purpose
The purpose of this plan is to:
- break the Windows 10M smoke test into small implementation modules
- avoid writing a full training mainline in one shot
- stay aligned with the Mac learning line, where each module can be understood, tested, and replaced independently
- establish a minimal engineering closed loop before later A100 / B200 scaling stages

Important scope note:
- W10 only writes the implementation plan
- W10 does not implement code
- W10 does not run the smoke test

## 2. Target
Target smoke test definition:
- Name: Windows 10M CUDA smoke test
- Hardware: RTX 4060 Ti 16GB
- Config file: `configs/windows/smoke_cuda_10m.json`
- Parameter scale: about 10M
- Attention backend: SDPA
- Dtype: `bf16`, with fallback if it fails
- The goal is not to train a good model, but to validate the training closed loop

## 3. Minimal End-to-End Flow
Future minimal smoke flow:
1. load config
2. validate config
3. create `run_id`
4. create experiment directory
5. snapshot resolved config
6. collect environment metadata
7. prepare toy text corpus
8. initialize tokenizer
9. tokenize toy corpus
10. build dataset x/y
11. build dataloader
12. initialize tiny dense Transformer model
13. run forward pass
14. compute next-token cross entropy loss
15. run backward
16. optimizer step
17. log metrics
18. save checkpoint
19. load checkpoint
20. run generation prompt
21. save generation samples
22. write `summary.md`
23. update experiment index manually

Important note:
- every step above is only for a smoke test path
- none of these steps imply formal training

## 4. Module Breakdown

### 4.1 Config Loader
Responsibilities:
- read JSON config
- return a dict or dataclass representation
- do not perform training
- do not add complex dependencies

Input:
- config path

Output:
- config object

Not responsible for:
- model creation
- training execution
- checkpointing

### 4.2 Config Validator
Responsibilities:
- check that target is `windows_cuda`
- check key model / tokenizer / training fields
- check `d_model % num_heads == 0`
- check `head_dim = d_model / num_heads`
- check that batch size and context length are conservative

Input:
- config

Output:
- validation result

Not responsible for:
- running the model
- fixing config automatically

### 4.3 Run Setup
Responsibilities:
- generate `run_id`
- create `experiments/windows_cuda/<run_id>/`
- copy resolved config
- write `run_metadata.json`

Input:
- config
- git commit
- environment info

Output:
- run directory

Not responsible for:
- training loop
- data loading logic

### 4.4 Toy Data
Responsibilities:
- provide a very small text corpus
- support pipeline validation only
- not represent real model capability

Input:
- embedded toy text or a tiny text file

Output:
- raw text or token ids

Not responsible for:
- real dataset quality
- benchmarking

### 4.5 Tokenizer
Responsibilities:
- version one may use ByteTokenizer
- later may be replaced by a BPE tokenizer
- output token ids
- do not output embeddings

Input:
- text

Output:
- token ids

Not responsible for:
- model forward
- loss computation

### 4.6 Dataset / Dataloader
Responsibilities:
- split token ids into x/y
- create batches
- do not compute loss

Input:
- token ids
- `sequence_length`
- `batch_size`

Output:
- `input_ids`
- `target_ids`

Not responsible for:
- optimizer behavior
- checkpointing

### 4.7 Tiny Dense Transformer
Responsibilities:
- initialize a small model from config
- map `input_ids -> logits`
- do not handle tokenizer
- do not handle loss
- do not handle optimizer

Input:
- `input_ids [B, T]`

Output:
- `logits [B, T, vocab_size]`

Not responsible for:
- data pipeline
- generation decoding

### 4.8 Loss
Responsibilities:
- compute next-token cross entropy from logits and targets
- output scalar loss

Input:
- logits
- `target_ids`

Output:
- loss

Not responsible for:
- parameter update
- logging

### 4.9 Optimizer Step
Responsibilities:
- `zero_grad`
- `backward`
- gradient clipping
- optimizer step

Input:
- loss
- model parameters

Output:
- updated parameters

Not responsible for:
- checkpointing
- generation

### 4.10 Checkpoint
Responsibilities:
- save model state
- save optimizer state
- save step and config metadata
- load checkpoint

Input:
- model
- optimizer
- metadata

Output:
- checkpoint file
- loaded state

Not responsible for:
- experiment indexing
- metrics analysis

### 4.11 Generation
Responsibilities:
- prompt to token ids
- logits to next token
- decode output
- save `generation_samples.jsonl`

Input:
- prompt
- model
- tokenizer

Output:
- generated text

Not responsible for:
- training loop
- checkpoint retention policy

### 4.12 Logging
Responsibilities:
- write `metrics.jsonl`
- write console log
- write generation samples
- write `summary.md`
- write failure report when needed

Input:
- run events
- metrics
- errors

Output:
- run files

Not responsible for:
- model optimization
- config design

## 5. Implementation Order
Implementation must proceed in small steps, not as a full training system in one pass.

Recommended order:
- W10.1 config loader only
- W10.2 config validator only
- W10.3 run setup only
- W10.4 toy data + ByteTokenizer only
- W10.5 dataset x/y only
- W10.6 tiny model forward only
- W10.7 loss only
- W10.8 backward + optimizer step only
- W10.9 checkpoint save/load only
- W10.10 generation only
- W10.11 logging integration only
- W10.12 one-step smoke run

Rules:
- each step must be testable on its own
- each step should land as a small commit
- do not implement everything at once

## 6. Success Criteria by Step
Success criteria:
- config loader: can read `configs/windows/smoke_cuda_10m.json`
- validator: can detect obviously invalid config
- run setup: can create run directory and metadata
- tokenizer: `decode(encode(text)) == text`
- dataset: x/y shapes are correct
- model: logits shape is correct
- loss: loss is finite
- optimizer: parameters can update
- checkpoint: save/load can restore state
- generation: text can be produced
- logging: metrics / generation / summary files exist
- one-step smoke: the full short closed loop works

## 7. Risk Controls
Risk controls:
- if OOM happens, reduce `batch_size` first
- then reduce `sequence_length`
- then change dtype
- then switch to naive attention
- do not jump directly to a bigger GPU
- do not turn the Windows smoke test into a long training run
- do not introduce large dependencies
- change only one variable at a time
- failures must produce `failure_report.md`

## 8. What W10 Does Not Do
W10 does not:
- write any Python implementation
- run training
- create a real run directory
- implement tokenizer / model / training
- download data
- download models
- install packages
- do MoE / alignment / RAG / Web UI
- execute GitHub push

## 9. Next Step
Suggested W10.1 direction:
- implement config loader only

Constraints for W10.1:
- it may only read JSON config
- it may not write training code
- it may not initialize a model
- it may not run the smoke test
- it may only create a minimal script or module that reads config and prints read-only inspection output
