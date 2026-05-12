# EduCode-1.5B Config Schema

## 1. Purpose
The config schema exists to:
- unify Mac / A100 / B200 experiment configuration
- avoid hard-coded settings inside future training scripts
- support scaling from 10M small models to a 1.5B target model
- support later profiling, checkpoint, generation, and scaling experiments

## 2. Design Principles
- JSON first to avoid extra dependencies
- small-to-large scalability
- explicit hardware target
- reproducibility
- no hidden training assumptions
- dense Transformer only for the current stage
- MoE reserved but not implemented

## 3. Top-level Config Sections
```json
{
  "run": {},
  "hardware": {},
  "tokenizer": {},
  "data": {},
  "model": {},
  "training": {},
  "optimizer": {},
  "scheduler": {},
  "checkpoint": {},
  "evaluation": {},
  "generation": {},
  "profiling": {},
  "logging": {}
}
```

Section responsibilities:
- `run`: experiment naming, seed, output path, notes
- `hardware`: hardware target, device, dtype, TF32, compile, distributed intent
- `tokenizer`: tokenizer family, vocab size, special tokens, artifact path
- `data`: dataset references, splits, sequence length, workers, streaming, token limits
- `model`: dense decoder-only architecture definition
- `training`: step count, batching, accumulation, intervals, clipping, precision mode
- `optimizer`: optimizer type and hyperparameters
- `scheduler`: learning rate schedule settings
- `checkpoint`: checkpoint save and resume behavior
- `evaluation`: evaluation cadence and metrics
- `generation`: generation-time sampling settings for spot checks
- `profiling`: memory, throughput, MFU, and attention backend profiling options
- `logging`: local logging and optional wandb metadata

## 4. Run Config
Suggested fields:
- `run_name`
- `seed`
- `output_dir`
- `notes`

## 5. Hardware Config
Suggested fields:
- `target`: `"mac_mps" | "a100_cuda" | "b200_cuda" | "windows_cuda"`
- `device`
- `dtype`
- `use_tf32`
- `compile`
- `distributed.enabled`
- `distributed.backend`
- `distributed.world_size`

Notes:
- The current Windows RTX 4060 Ti line is for smoke tests only, not formal 1.5B training.
- The Mac line is for gradual learning and MPS profiling.
- The A100 line is for CUDA profiling.
- The B200 line is for the main 1.5B training plan.

## 6. Tokenizer Config
Suggested fields:
- `type`: `"byte" | "bpe"`
- `vocab_size`
- `path`
- `artifact_dir`
- `special_tokens`
- `pad_token_id`
- `bos_token_id`
- `eos_token_id`
- `unk_token_id`

Rules:
- `tokenizer.type` must be one of: `byte`, `bpe`
- if `tokenizer.type == "bpe"`:
  - `tokenizer.path` is required
  - `tokenizer.path` must point to `tokenizer.json`
  - `tokenizer.artifact_dir` should point to the containing artifact directory
  - `tokenizer.vocab_size` must match the loaded tokenizer vocab size
  - `model.vocab_size` must equal `tokenizer.vocab_size`
- if `tokenizer.type == "byte"`:
  - `tokenizer.vocab_size` should be `256`
  - `tokenizer.path` may be `null`

Required formula:

`model.vocab_size = tokenizer.vocab_size = loaded_tokenizer.vocab_size`

Notes:
- The current Mac learning line starts from a ByteTokenizer mindset.
- Formal training is expected to use byte-level BPE.
- The tokenizer outputs token ids, not embeddings.

## 7. Data Config
Suggested fields:
- `dataset_name`
- `data_paths`
- `train_split`
- `val_split`
- `sequence_length`
- `num_workers`
- `shuffle`
- `streaming`
- `max_tokens`

Current stage note:
- This phase only defines configuration shape and does not implement a data pipeline.

## 8. Model Config
Suggested fields:
- `architecture`: `"dense_decoder_only"`
- `vocab_size`
- `context_length`
- `num_layers`
- `d_model`
- `num_heads`
- `head_dim`
- `ffn_type`: `"swiglu"`
- `d_ff`
- `norm_type`: `"rmsnorm"`
- `position_encoding`: `"rope"`
- `rope_theta`
- `dropout`
- `tie_embeddings`

Notes:
- The current stage only targets a dense Transformer.
- `ffn_type` may expand later, but MoE is not implemented in the current stage.
- The 1.5B draft config follows a LLaMA-style structure.

## 9. Training Config
Suggested fields:
- `max_steps`
- `batch_size`
- `gradient_accumulation_steps`
- `global_batch_tokens`
- `sequence_length`
- `eval_interval`
- `log_interval`
- `save_interval`
- `grad_clip`
- `mixed_precision`

## 10. Optimizer Config
Suggested fields:
- `name`: `"adamw" | "muon"`
- `learning_rate`
- `weight_decay`
- `betas`
- `eps`

Notes:
- AdamW is the baseline.
- Muon is a later ablation and is not part of the current implementation.

## 11. Scheduler Config
Suggested fields:
- `name`
- `warmup_steps`
- `min_lr`
- `max_lr`

## 12. Checkpoint Config
Suggested fields:
- `save_dir`
- `resume_from`
- `save_latest`
- `save_best`
- `keep_last_n`
- `save_optimizer_state`

Notes:
- Checkpoints support resume, best-model retention, and experiment comparison.

## 13. Evaluation Config
Suggested fields:
- `enabled`
- `eval_steps`
- `eval_tokens`
- `metrics`

## 14. Generation Config
Suggested fields:
- `enabled`
- `prompts`
- `max_new_tokens`
- `temperature`
- `top_k`
- `top_p`

## 15. Profiling Config
Suggested fields:
- `enabled`
- `profile_steps`
- `record_memory`
- `record_tokens_per_sec`
- `record_mfu`
- `attention_backend`: `"naive" | "sdpa" | "flash_attention_2"`

Notes:
- Windows currently only validates SDPA availability.
- FlashAttention-2 is planned for later A100 / B200 work and should not be assumed on Windows.

## 16. Logging Config
Suggested fields:
- `log_dir`
- `log_jsonl`
- `use_wandb`
- `wandb_project`

Notes:
- The default path should not depend on wandb.
- Local jsonl logging is the initial baseline.

## 17. Example Configs
This step creates the following example configuration files:
- `configs/mac/tiny_10m.json`
- `configs/a100/smoke_100m.json`
- `configs/b200/educode_1_5b.json`
- `configs/windows/smoke_cuda_10m.json`

## 18. Non-goals
The current stage does not:
- write a config loader
- write training code
- implement tokenizer / model / training
- implement MoE
- implement alignment
- implement RAG / Web UI
- run any experiments

## 19. Next Step
Suggested W4 directions:
- create a smoke test plan document
- or create a config validation checklist
- still do not implement the training mainline
