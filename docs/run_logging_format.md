# EduCode-1.5B Run Logging Format

## 1. Purpose
The purpose of run logging is to:
- make every experiment reproducible
- record hardware, config, git commit, environment, and metrics
- support Windows / Mac / A100 / B200 multi-stage experimentation
- support later project reports, resume bullets, and experiment tables
- avoid situations where a run was "done before" but nobody knows how it was run or what result it produced

## 2. Logging Principles
- every run has a unique `run_id`
- every run links to exactly one config file
- every run records git commit hash
- every run records hardware target
- every run records start time and end time
- every run records success or failure
- every failed run must include an error summary
- every successful training run must include loss metrics
- every generation run must save prompts and outputs
- logs should be append-only when possible
- prefer JSONL for machine-readable logs
- prefer Markdown summaries for human-readable reports

## 3. Run Directory Layout
Recommended per-run layout:

```text
experiments/<stage>/<run_id>/
  run_config.json
  run_metadata.json
  metrics.jsonl
  console.log
  generation_samples.jsonl
  checkpoints_manifest.json
  failure_report.md
  summary.md
```

File roles:
- `run_config.json`: snapshot of the effective config used for the run
- `run_metadata.json`: environment, hardware, git, timing, and status metadata
- `metrics.jsonl`: machine-readable step-level metrics stream
- `console.log`: raw stdout / stderr and warnings
- `generation_samples.jsonl`: saved prompts and outputs for generation checks
- `checkpoints_manifest.json`: tracked checkpoint metadata without committing large checkpoint files
- `failure_report.md`: human-readable failure diagnosis for failed or interrupted runs
- `summary.md`: concise human-readable experiment summary

Notes:
- W5 only defines the format and does not create real experiment directories.
- `logs/`, `checkpoints/`, and `data/` are currently ignored by Git and should not contain committed large files.
- `summary.md` may be selectively committed later if useful.

## 4. run_id Format
Recommended format:

```text
YYYYMMDD_HHMMSS_<stage>_<short_name>
```

Examples:
- `20260510_213000_windows_cuda_10m_smoke`
- `20260511_101500_mac_mps_tiny_10m`
- `20260512_020000_a100_100m_sdpa`
- `20260513_030000_b200_1_5b_preflight`

Requirements:
- `run_id` must be readable
- `run_id` must be unique
- `run_id` must include stage or hardware context

## 5. run_metadata.json Schema
Suggested fields:
- `run_id`
- `project`
- `stage`
- `hardware_target`
- `hostname`
- `os`
- `python_version`
- `torch_version`
- `cuda_available`
- `cuda_version`
- `cudnn_version`
- `gpu_name`
- `gpu_memory_gib`
- `git_commit`
- `git_branch`
- `config_path`
- `start_time`
- `end_time`
- `status`: `"success" | "failed" | "interrupted"`
- `notes`

Purpose:
- `run_metadata.json` answers: what environment, what code, and what config produced this run.

## 6. run_config.json
Guidelines:
- `run_config.json` should be a snapshot of the exact config used for that run.
- A run should not only reference `configs/...` because those files can change later.
- Every run should save a resolved config copy.
- The resolved config should include at least `model`, `training`, `optimizer`, `hardware`, `profiling`, and `logging` sections.

## 7. metrics.jsonl Format
Each line should be one JSON object.

Suggested fields:
- `step`
- `tokens_seen`
- `train_loss`
- `val_loss`
- `learning_rate`
- `grad_norm`
- `tokens_per_sec`
- `examples_per_sec`
- `gpu_memory_allocated_gib`
- `gpu_memory_reserved_gib`
- `mfu`
- `elapsed_seconds`
- `timestamp`

Example JSONL lines:

```json
{"step": 10, "tokens_seen": 5120, "train_loss": 4.82, "val_loss": null, "learning_rate": 0.0003, "grad_norm": 1.42, "tokens_per_sec": 18500.0, "examples_per_sec": 144.5, "gpu_memory_allocated_gib": 3.1, "gpu_memory_reserved_gib": 3.8, "mfu": null, "elapsed_seconds": 12.4, "timestamp": "2026-05-10T21:30:12Z"}
{"step": 20, "tokens_seen": 10240, "train_loss": 4.51, "val_loss": 4.67, "learning_rate": 0.00029, "grad_norm": 1.35, "tokens_per_sec": 18620.0, "examples_per_sec": 145.4, "gpu_memory_allocated_gib": 3.1, "gpu_memory_reserved_gib": 3.8, "mfu": 0.21, "elapsed_seconds": 24.8, "timestamp": "2026-05-10T21:30:24Z"}
```

Notes:
- Smoke tests may only populate a subset of fields.
- A100 / B200 profiling should record `tokens_per_sec`, memory, and `mfu`.
- Mac MPS runs may keep some GPU-specific fields as `null` if unavailable.

## 8. console.log
Guidelines:
- `console.log` should capture stdout, stderr, warnings, and important runtime messages.
- It should not be the only log source.
- Machine-readable metrics should go into `metrics.jsonl`.

## 9. generation_samples.jsonl Format
Suggested fields:
- `step`
- `prompt`
- `output`
- `max_new_tokens`
- `temperature`
- `top_k`
- `top_p`
- `checkpoint_path`
- `timestamp`

Example JSONL line:

```json
{"step": 200, "prompt": "def add(a, b):", "output": "\n    return a + b", "max_new_tokens": 32, "temperature": 0.7, "top_k": 50, "top_p": 0.95, "checkpoint_path": "checkpoints/run_200/latest.pt", "timestamp": "2026-05-10T21:45:00Z"}
```

Notes:
- Generation is necessary evidence that the model path is closed-loop.
- The first version does not need high generation quality.
- It must still record prompt and output.

## 10. checkpoints_manifest.json
Suggested fields:
- `checkpoint_id`
- `step`
- `path`
- `type`: `"latest" | "best" | "periodic"`
- `train_loss`
- `val_loss`
- `saved_at`
- `contains_optimizer_state`
- `contains_scheduler_state`
- `config_hash`

Notes:
- Checkpoint files themselves should not be committed to Git.
- The manifest can track local or cloud checkpoint state.

## 11. failure_report.md
Failure reports must include:
- `run_id`
- `hardware`
- `config_path`
- `git_commit`
- `error_type`
- `error_message`
- `stack_trace_summary`
- `suspected_cause`
- `attempted_fix`
- `next_action`

Failure handling principles:
- reduce batch size first on OOM
- then reduce context length
- then disable high-risk features
- do not jump directly to B200
- change only one variable at a time
- failed runs must still be recorded

## 12. summary.md
A human-readable summary should include:
- run goal
- hardware
- config
- result
- key metrics
- loss curve notes
- generation notes
- whether the run is resumeable
- whether the run is suitable for report / resume use
- next step

## 13. Stage-specific Logging Requirements

### Windows 4060 Ti
Must record:
- CUDA available
- bf16 sanity
- SDPA sanity
- small smoke result
- no 1.5B full training

### Mac M3 Max
Must record:
- MPS availability
- tokenizer tests
- loss decrease
- MPS speed / memory observations
- Apple Silicon notes

### A100
Must record:
- CUDA bf16
- SDPA / FlashAttention status
- tokens/sec
- memory
- checkpoint resume
- profiling notes

### B200
Must record:
- preflight checklist
- storage path
- token budget
- checkpoint strategy
- resume test
- failure recovery strategy
- cost estimate

## 14. What W5 Does Not Do
W5 does not:
- implement a logger
- write training code
- create real run directories
- run experiments
- download data
- download models
- implement tokenizer / model / training
- do MoE / alignment / RAG / Web UI

## 15. Next Step
Suggested W6 directions:
- create a config validation checklist
- or create a minimal run manifest template
- still do not implement the training mainline
