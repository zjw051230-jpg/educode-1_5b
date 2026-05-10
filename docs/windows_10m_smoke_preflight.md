# Windows 10M Smoke Test Preflight Checklist

## 1. Purpose
The purpose of this checklist is to:
- confirm that environment, config, directories, logging expectations, and failure handling are ready before the first Windows 10M CUDA smoke test
- avoid jumping directly into training-mainline implementation or blind experiment execution
- keep the RTX 4060 Ti 16GB focused on small-model validation only
- establish discipline for later Mac / A100 / B200 stages

Important scope note:
- W9 only defines the preflight checklist
- W9 does not run the smoke test
- W9 does not write training code

## 2. Target Smoke Test
Target smoke test:
- Name: Windows 10M CUDA smoke test
- Hardware: RTX 4060 Ti 16GB
- Config file: `configs/windows/smoke_cuda_10m.json`
- Target parameter scale: about 10M
- Intended use:
  - validate CUDA forward / backward
  - validate SDPA
  - validate basic bf16 usability
  - validate future checkpoint / generation / logging pathways

This smoke test is not for:
- 1.5B full pretraining
- large-scale training
- long-duration benchmarking

## 3. Required Preflight State
The following should already be true:
- `git status` is clean
- `main` is in sync with `origin/main`
- the current commit has been recorded
- W1-W8 documents exist
- CUDA environment check has passed
- `configs/windows/smoke_cuda_10m.json` exists
- `docs/run_logging_format.md` exists
- `templates/run_manifest/` exists
- large-file directories under `logs/`, `checkpoints/`, and `data/` are still ignored by `.gitignore`

## 4. Environment Checklist
Environment checks:
- Python version has been recorded
- torch version has been recorded
- `torch.cuda.is_available()` is `True`
- GPU is RTX 4060 Ti
- GPU memory is about 16GB
- compute capability is 8.9
- bf16 sanity check has passed
- SDPA sanity check has passed
- `nvidia-smi` is available
- `nvcc` is available, but it does not need to match the torch CUDA version exactly

Notes:
- `nvidia-smi` CUDA, torch CUDA, and `nvcc` versions being different is a common situation
- Windows currently only targets functional validation, not production-grade training performance

## 5. Config Checklist
Checklist for `configs/windows/smoke_cuda_10m.json`:
- `hardware.target = windows_cuda`
- `dtype = bf16` or an explicit fallback is documented
- `tokenizer.vocab_size = model.vocab_size`
- model parameter scale is about 10M
- `context_length` is conservative, such as 128
- `num_layers` is conservative, such as 4
- `d_model` is conservative, such as 256
- `num_heads` divides `d_model`
- `head_dim = d_model / num_heads`
- `batch_size` is conservative, such as 4
- `gradient_accumulation_steps` is explicit
- `attention_backend = sdpa`
- checkpoint configuration exists
- logging configuration exists
- evaluation configuration exists
- generation configuration exists

Formula:

```text
head_dim = d_model / num_heads
```

## 6. Data Checklist
Current data expectations:
- W9 does not prepare real training data
- a future smoke test may use a toy text corpus
- toy data is only for pipeline validation
- toy data does not represent model capability
- toy data must not be committed as a large file
- the data path must be explicit
- train / val split must be explicit
- `sequence_length` must match the config

## 7. Expected Minimal Smoke Flow
This is a future execution plan only, not an implementation.

Expected flow:
1. load config
2. record git commit
3. create `run_id`
4. create experiment directory
5. copy resolved config to `run_config.json`
6. initialize tokenizer
7. prepare tiny dataset
8. initialize 10M model
9. run one forward pass
10. compute loss
11. run backward
12. optimizer step
13. write `metrics.jsonl`
14. save tiny checkpoint
15. load checkpoint
16. run one generation prompt
17. write `generation_samples.jsonl`
18. write `summary.md`

Important note:
- these are the steps a later smoke test should perform
- W9 does not implement any of them

## 8. Success Criteria

### Environment Success
- CUDA available
- bf16 sanity passed
- SDPA sanity passed

### Config Success
- JSON parse passed
- config matches the Windows target
- model dimensions are valid

### Model Flow Success
Future smoke test success means:
- model initializes
- forward works
- loss is finite
- backward works
- optimizer step works

### Logging Success
Future smoke test success means:
- `run_metadata.json` exists
- `run_config.json` exists
- `metrics.jsonl` has at least one line
- `summary.md` exists

### Generation Success
Future smoke test success means:
- prompt can be encoded
- token ids can be generated
- output can be decoded
- `generation_samples.jsonl` exists

## 9. Failure Handling
If OOM happens:
1. reduce `batch_size` first
2. then reduce `context_length`
3. then change dtype or disable high-risk features
4. do not jump directly to a bigger GPU

If CUDA is unavailable:
- return to the W2 environment check
- do not enter the smoke test

If SDPA fails:
- fall back to naive attention
- record the failure reason

If bf16 fails:
- fall back to float32 or fp16
- record hardware and torch version

General rules:
- change only one variable at a time
- every failure should still produce `failure_report.md`

## 10. Not Allowed in Windows 10M Smoke
The following are not allowed:
- training 1.5B
- using the B200 config
- using a large dataset
- long-duration training
- exaggerated performance claims
- MoE
- alignment
- RAG / Web UI
- committing checkpoint weights
- committing raw data
- jumping to a bigger GPU immediately after failure

## 11. Relation to Project Roadmap
The Windows 10M smoke test is:
- not formal training
- an engineering de-risking step before A100 / B200
- a validation of the minimal training path
- a gate that should pass before considering an A100 100M smoke run
- not a substitute for B200 preflight

B200 should only be used after earlier smoke stages pass.

## 12. What W9 Does Not Do
W9 does not:
- write training code
- run the smoke test
- implement tokenizer / model / training
- create a real experiment run
- install packages
- download models
- download data
- commit large files
- execute GitHub push

## 13. Next Step
Suggested W10 directions:
- create a read-only config validation script
- or create a Windows 10M smoke test implementation plan

Recommended next step:
- W10: Windows 10M smoke test implementation plan

Implementation caution:
- W10 should still start with a written implementation plan
- do not jump directly into a full training-code implementation
