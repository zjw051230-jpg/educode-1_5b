# EduCode-1.5B Experiment Index

## 1. Purpose
The purpose of the experiment index is to:
- register all Windows / Mac / A100 / B200 experiments in one place
- connect config, run_id, hardware, git commit, result, and report references
- avoid scattered experiment tracking
- support later project reports and resume writing
- keep the current stage documentation-only without running experiments

## 2. Experiment Tracking Principles
- every experiment gets a unique `experiment_id`
- every experiment links to a `run_id`
- every experiment links to a config file
- every experiment records hardware target
- every experiment records git commit
- every experiment records status
- failed experiments should still be recorded
- no large files are committed
- summaries can be committed when useful
- raw logs / checkpoints / data stay ignored

## 3. Experiment ID Format
Recommended format:

```text
EXP-YYYYMMDD-XXX-short-name
```

Examples:
- `EXP-20260510-001-windows-cuda-env-check`
- `EXP-20260510-002-windows-10m-smoke`
- `EXP-20260511-001-mac-byte-tokenizer`
- `EXP-20260512-001-a100-100m-sdpa`
- `EXP-20260513-001-b200-1p5b-preflight`

Meaning:
- `YYYYMMDD` is the experiment date
- `XXX` is the sequence number for that day
- `short-name` is a compact description of the goal

## 4. Experiment Index Table

| experiment_id | run_id | stage | hardware | config | git_commit | status | result_summary | report_path | next_action |
|---|---|---|---|---|---|---|---|---|---|
| EXP-20260510-001-project-skeleton | N/A | documentation | local repo setup | N/A | 311a2fa | success | W1 project skeleton established | `README.md` | proceed to environment validation |
| EXP-20260510-002-windows-cuda-env-check | N/A | documentation | Windows RTX 4060 Ti | `scripts/check_cuda_env.py` | 9957630 | success | CUDA environment check documented; no training run executed | `docs/w2_cuda_env_check.md` | use as baseline for smoke planning |
| EXP-20260510-003-config-schema-draft | N/A | planning | cross-hardware | `docs/config_schema.md` | 03ac8e1 | success | minimal config schema drafted for Windows / Mac / A100 / B200 | `docs/config_schema.md` | use schema for future run configs |
| EXP-20260510-004-smoke-test-plan | N/A | planning | cross-hardware | `docs/smoke_test_plan.md` | e5f5564 | success | smoke test ladder and stage responsibilities documented | `docs/smoke_test_plan.md` | use as preflight planning reference |
| EXP-20260510-005-run-logging-format | N/A | planning | cross-hardware | `docs/run_logging_format.md` | e55381a | success | run logging file format and logging principles defined | `docs/run_logging_format.md` | align future runs with logging standard |
| EXP-20260510-006-config-validation-checklist | N/A | planning | cross-hardware | `docs/config_validation_checklist.md` | d13209a | success | config validation checklist drafted for all hardware stages | `docs/config_validation_checklist.md` | use before any real run |
| EXP-20260510-007-run-manifest-templates | N/A | planning | cross-hardware | `docs/run_manifest_templates.md` | 858ed77 | success | minimal run manifest templates added for future experiments | `docs/run_manifest_templates.md` | instantiate templates per run later |
| EXP-20260511-001-windows-one-step-smoke | `20260511_024724_windows_cuda_one_step_smoke` | windows_cuda | Windows RTX 4060 Ti | `configs/windows/smoke_cuda_10m.json` | 2d30630 | success | one-step smoke path completed with checkpoint, generation, and logging artifacts | `docs/w10_12_one_step_smoke.md` | review the milestone before any repeated loop |
| EXP-20260511-002-windows-one-step-smoke-review | `20260511_024724_windows_cuda_one_step_smoke` | review | Windows RTX 4060 Ti | `configs/windows/smoke_cuda_10m.json` | pending local commit | success | one-step smoke reviewed and accepted | `docs/w10_13_one_step_smoke_review.md` | proceed to W11 minimal training loop plan |

Notes:
- These entries are documentation / planning records, not training runs.
- No fake training metrics or fake run outputs are recorded here.

## 5. Planned Smoke Experiments

| planned_experiment | hardware | config | goal | prerequisite | success_criteria | current_status |
|---|---|---|---|---|---|---|
| Windows 10M CUDA smoke test | Windows RTX 4060 Ti | `configs/windows/smoke_cuda_10m.json` | verify minimal CUDA smoke path on local Windows machine | W2, W3, W4, W5, W6, W7 complete | forward/backward/checkpoint/generation path planned and validated | planned |
| Mac M3 Max ByteTokenizer / BPE learning run | Mac M3 Max 36GB | `configs/mac/tiny_10m.json` | learn tokenizer behavior and small data flow on MPS | tokenizer implementation phase ready | byte round-trip and BPE encode/decode verified | planned |
| Mac M3 Max tiny 10M training run | Mac M3 Max 36GB | `configs/mac/tiny_10m.json` | validate tiny dense Transformer training behavior | tokenizer and model path implemented | loss decreases and checkpoint path works | planned |
| A100 100M SDPA smoke run | A100 | `configs/a100/smoke_100m.json` | validate CUDA bf16 + SDPA baseline on datacenter GPU | local smoke path stable | logs, checkpoint, and validation path work | planned |
| A100 300M profiling run | A100 | future A100 profiling config | measure tokens/sec, memory, and backend behavior | 100M smoke run passes | profiling logs, memory, and resume path verified | planned |
| B200 1.5B preflight run | B200 | `configs/b200/educode_1_5b.json` | validate target-hardware preflight before longer training | A100 smoke/profiling path passes | config, logging, checkpoint, generation, storage, and budget checks pass | planned |
| B200 1.5B short run | B200 | `configs/b200/educode_1_5b.json` | run short end-to-end validation on target hardware | B200 preflight passes | short training, checkpoint, eval, and generation path complete | planned |
| B200 1.5B main run | B200 | `configs/b200/educode_1_5b.json` | execute formal main training campaign | all preflight gates pass | stable long-run logging, evaluation, resume, and reporting | planned |

## 6. Status Definitions
- `planned`
- `running`
- `success`
- `failed`
- `interrupted`
- `blocked`
- `deprecated`

## 7. What Should Be Linked
Each experiment should link, when available, to:
- config file
- run directory
- `summary.md`
- `metrics.jsonl`
- generation samples
- checkpoint manifest
- failure report
- relevant commit

## 8. What Should Not Be Committed
Do not commit:
- raw datasets
- model weights
- large checkpoints
- full logs when they are huge
- cache files
- private credentials
- API keys

## 9. Relation to Previous Docs
This index works together with:
- `docs/config_schema.md`
- `docs/smoke_test_plan.md`
- `docs/run_logging_format.md`
- `docs/config_validation_checklist.md`
- `docs/run_manifest_templates.md`

## 10. What W8 Does Not Do
W8 does not:
- run experiments
- write training code
- implement tokenizer / model / training
- create real run directories
- commit large files from `logs/`, `checkpoints/`, or `data/`
- do GitHub push

## 11. Next Step
Suggested W9 directions:
- create a read-only config validation script draft
- or start a Windows 10M smoke test preflight checklist

Recommended next step:
- Windows 10M smoke test preflight checklist
