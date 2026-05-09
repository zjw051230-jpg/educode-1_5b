# EduCode-1.5B Config Validation Checklist

## 1. Purpose
The purpose of config validation is to:
- ensure every run config is complete, reproducible, and matched to the intended hardware before execution
- prevent Mac configs from being run on B200, or B200 configs from being run on Windows
- prevent mismatches in key parameters such as `vocab_size`, `context_length`, `num_heads`, and `d_model`
- prevent missing checkpoint, logging, or data path settings
- reduce debugging cost on A100 and B200

## 2. Validation Philosophy
- validate before run
- config must match target hardware
- every config must be JSON-parseable
- every config must declare `model`, `data`, `training`, `checkpoint`, and `logging` sections
- no hidden defaults for important training parameters
- every run must snapshot resolved config
- large GPU runs require preflight validation
- B200 runs require stricter checks than Windows / Mac smoke tests

## 3. Basic JSON Validation
Basic checks:
- the JSON file can be parsed
- there is no trailing comma
- field names are spelled consistently
- numeric values use correct numeric types
- boolean values are not written as strings
- path fields are not empty
- the config filename clearly describes its purpose

Current configs to cover:
- `configs/windows/smoke_cuda_10m.json`
- `configs/mac/tiny_10m.json`
- `configs/a100/smoke_100m.json`
- `configs/b200/educode_1_5b.json`

## 4. Required Top-level Sections
Every config should contain:
- `run`
- `hardware`
- `tokenizer`
- `data`
- `model`
- `training`
- `optimizer`
- `scheduler`
- `checkpoint`
- `evaluation`
- `generation`
- `profiling`
- `logging`

Notes:
- smoke configs may simplify some sections
- critical sections should not be completely absent
- if something is omitted, there must be a clear reason

## 5. Hardware Validation
Checks:
- `hardware.target` must be one of:
  - `windows_cuda`
  - `mac_mps`
  - `a100_cuda`
  - `b200_cuda`

- `dtype` must fit the hardware target:
  - Windows 4060 Ti: `bf16` may be used for sanity / smoke, but with caution
  - Mac MPS: `float32` / `bf16` must be validated empirically
  - A100: `bf16` recommended
  - B200: `bf16` recommended

- `distributed.enabled` must be reasonable:
  - Windows / Mac default `false`
  - A100 single-card `false`
  - B200 single-card `false`
  - multi-card B200 is the first case where `true` should be considered

- `attention_backend` must be reasonable:
  - Windows: `sdpa`
  - Mac: `naive` or `sdpa`, subject to real MPS validation
  - A100: `sdpa` baseline, `flash_attention_2` planned
  - B200: `sdpa` initial, `flash_attention_2` planned

## 6. Tokenizer Validation
Checks:
- `tokenizer.type` must be `byte` or `bpe`
- formal training should use `bpe`
- smoke tests may use `byte` or toy `bpe`
- `tokenizer.vocab_size` must match `model.vocab_size`
- `tokenizer_path` must be fixed before formal training
- `special_tokens` must be explicit
- tokenizer outputs token ids, not embeddings

## 7. Data Validation
Checks:
- `data_paths` must exist or be clearly marked as placeholder
- `train_split` and `val_split` must be defined
- `data.sequence_length` must match `model.context_length` and `training.sequence_length`
- `max_tokens` must fit the intended stage
- `streaming` must be explicit
- `num_workers` should fit the target hardware
- Windows smoke should not point to large-scale data paths
- B200 runs should not use toy data

## 8. Model Validation
Checks:
- `architecture` must be `dense_decoder_only`
- MoE is not allowed in the current stage
- `model.vocab_size` must match `tokenizer.vocab_size`
- `context_length` must be reasonable for the target stage
- `d_model` must be divisible by `num_heads`
- `head_dim` must equal `d_model / num_heads`
- `d_ff` must match the intended `ffn_type`
- `ffn_type` currently only allows `swiglu` or `dense_mlp`; `moe` is not allowed
- `norm_type` should be `rmsnorm`
- `position_encoding` should be `rope`
- `rope_theta` must be defined
- `dropout` must be explicit and reasonable
- `tie_embeddings` must be explicit

Formula:

```text
head_dim = d_model / num_heads
```

If `d_model` is not divisible by `num_heads`, the config is invalid.

## 9. Training Validation
Checks:
- at least one of `max_steps` or `max_tokens` must be defined
- `batch_size > 0`
- `gradient_accumulation_steps > 0`
- `global_batch_tokens` should be derivable or explicit
- `sequence_length` must match data and model settings
- `log_interval > 0`
- `eval_interval > 0`
- `save_interval > 0`
- `grad_clip` must be defined
- `mixed_precision` should align with `hardware.dtype`

## 10. Optimizer Validation
Checks:
- `optimizer.name` currently allows:
  - `adamw`
  - `muon`

- baseline before implementation should be `adamw`
- `muon` may be marked as planned but should not be the default enabled path
- `learning_rate > 0`
- `weight_decay >= 0`
- `betas` length must be 2
- `eps > 0`

## 11. Scheduler Validation
Checks:
- `scheduler.name` must be defined
- `warmup_steps >= 0`
- `max_lr >= min_lr`
- `warmup_steps` should not exceed `max_steps`
- if `max_steps` is absent, the schedule computation rule must be explicit

## 12. Checkpoint Validation
Checks:
- `save_dir` must be defined
- `save_latest` must be explicit
- `save_best` must be explicit
- `keep_last_n >= 1`
- `save_optimizer_state` must be explicit
- long runs must support resume-related behavior
- B200 runs must define checkpoint strategy clearly
- checkpoint files must not be committed to Git

## 13. Evaluation Validation
Checks:
- `evaluation.enabled` must be explicit
- `eval_interval` or `eval_steps` must be defined
- `eval_tokens` must be reasonable
- metrics should include at least `val_loss`
- training should not run without evaluation planning
- B200 runs must enable evaluation

## 14. Generation Validation
Checks:
- `generation.enabled` must be explicit
- `prompts` must exist
- `max_new_tokens > 0`
- `temperature > 0`
- `top_k` and `top_p` must be reasonable
- generation samples should be saved into the run logging directory
- smoke tests must include at least one generation prompt

## 15. Profiling Validation
Checks:
- `profiling.enabled` must be explicit
- `profile_steps` must be reasonable
- `record_memory` must be explicit
- `record_tokens_per_sec` must be explicit
- `record_mfu` must be explicit
- `attention_backend` must be one of:
  - `naive`
  - `sdpa`
  - `flash_attention_2`

Notes:
- Windows currently only validates SDPA
- FlashAttention-2 should not be assumed by default on Windows
- A100 / B200 profiling should record `tokens_per_sec` and memory
- B200 runs should record MFU

## 16. Logging Validation
Checks:
- `log_dir` must be defined
- `log_jsonl` should be enabled
- `use_wandb` must be explicit
- the default path should not depend on wandb
- every run must be able to produce:
  - `run_metadata.json`
  - `run_config.json`
  - `metrics.jsonl`
  - `summary.md`

Note:
- W6 defines logging rules only and does not implement a logger.

## 17. Stage-specific Validation

### Windows 4060 Ti
Must confirm:
- `target = windows_cuda`
- parameter scale is around 10M
- B200 config is not used
- no 1.5B full pretraining
- batch size is conservative
- context length is conservative
- `attention_backend = sdpa`
- usage is smoke test only

### Mac M3 Max
Must confirm:
- `target = mac_mps`
- parameter scale is 10M-40M
- speed is not the priority
- the goal is learning and MPS observation
- dtype needs real validation
- CUDA-only features are not used

### A100
Must confirm:
- `target = a100_cuda`
- parameter scale is 100M-300M
- `bf16`
- `sdpa` baseline
- `flash_attention_2` only after installation and validation
- profiling enabled
- checkpoint resume should be tested

### B200
Must confirm:
- `target = b200_cuda`
- it runs only after earlier smoke tests pass
- the 1.5B config is not used on Windows / Mac
- checkpoint strategy is complete
- logging is complete
- token budget is explicit
- storage path is confirmed
- budget is confirmed
- failure recovery is explicit

## 18. Pre-run Checklist
General pre-run checklist:
- git status clean
- git commit hash recorded
- config JSON parse passed
- target hardware confirmed
- tokenizer path confirmed
- data path confirmed
- `output_dir` confirmed
- checkpoint dir confirmed
- logging dir confirmed
- dry-run planned
- expected memory estimated
- failure plan written

## 19. What W6 Does Not Do
W6 does not:
- implement a config validator
- write Python validation code
- run training
- change existing config contents unless there is an obvious JSON error
- implement tokenizer / model / training
- do MoE / alignment / RAG / Web UI
- download data or models

## 20. Next Step
Suggested W7 directions:
- create a minimal run manifest template
- or start a read-only config validation script draft

Recommendation:
- if you want to keep the current safety boundary, prefer the minimal run manifest template first
- the validation script can come after that
