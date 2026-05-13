# EduCode-1.5B Experiment Index

## 1. Purpose
The purpose of the experiment index is to:
- register all Windows / Mac / A100 / B200 experiments in one place
- connect config, run_id, hardware, git commit, result, and report references
- avoid scattered experiment tracking
- support later project reports and resume writing
- Project has completed the Windows one-step smoke milestone and the bounded W11 minimal training loop review.
- The current stage is deciding between a bounded 50-step toy training plan and a return to the Mac learning line.
- Documentation, config, run setup, logging, one-step smoke, checkpoint, generation, optimizer-step checks, and a bounded 10-step toy training loop have been completed.
- The project has not yet entered real-data training, long training, A100/B200 scaling, BPE integration, RoPE integration, FlashAttention-2 integration, or 1.5B pretraining.

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
| EXP-20260511-002-windows-one-step-smoke-review | `20260511_024724_windows_cuda_one_step_smoke` | review | Windows RTX 4060 Ti | `configs/windows/smoke_cuda_10m.json` | 8abbcda | success | one-step smoke reviewed and accepted | `docs/w10_13_one_step_smoke_review.md` | proceed to W11 minimal training loop plan |
| EXP-20260511-003-w11-minimal-training-loop-plan | N/A | planning | Windows RTX 4060 Ti | `configs/windows/smoke_cuda_10m.json` | b213897 | success | minimal training loop plan created | `docs/w11_minimal_training_loop_plan.md` | create a strictly bounded minimal training loop script next |
| EXP-20260511-004-w11-1-minimal-training-loop-script | `20260511_041027_windows_cuda_minimal_training_loop` | windows_cuda | Windows RTX 4060 Ti | `configs/windows/smoke_cuda_10m.json` | 09d8bae | success | minimal training loop script completed on toy data | `docs/w11_1_minimal_training_loop.md` | review the toy-loop metrics and artifacts next |
| EXP-20260511-005-w11-2-minimal-training-loop-review | `20260511_041027_windows_cuda_minimal_training_loop` | review | Windows RTX 4060 Ti | `configs/windows/smoke_cuda_10m.json` | 8ae95bf | success | minimal training loop reviewed and accepted | `docs/w11_2_minimal_training_loop_review.md` | write a bounded 50-step toy training plan or return to the Mac learning line |
| EXP-20260511-006-w11-3-bounded-50-step-toy-training-plan | N/A | planning | Windows RTX 4060 Ti | `configs/windows/smoke_cuda_10m.json` | f90af9a | success | bounded 50-step toy training plan created | `docs/w11_3_bounded_50_step_toy_training_plan.md` | implement only the bounded 50-step toy script next |
| EXP-20260511-007-w11-4-bounded-50-step-toy-training | `20260511_044948_windows_cuda_bounded_50_step_toy` | windows_cuda | Windows RTX 4060 Ti | `configs/windows/smoke_cuda_10m.json` | d7798a8 | success | bounded 50-step toy training completed | `docs/w11_4_bounded_50_step_toy_training.md` | review the 50-step toy training artifacts next |
| EXP-20260511-008-w11-5-bounded-50-step-toy-training-review | `20260511_044948_windows_cuda_bounded_50_step_toy` | review | Windows RTX 4060 Ti | `configs/windows/smoke_cuda_10m.json` | 6eb6eb6 | success | bounded 50-step toy training reviewed and accepted | `docs/w11_5_bounded_50_step_toy_training_review.md` | write a bounded 100-step toy training plan or return to the Mac learning line |
| EXP-20260511-009-r1-resume-mvp-pack | N/A | R1 | Windows RTX 4060 Ti | `scripts/run_resume_demo.py` | 24418ba | success | resume-ready project packaging created | `docs/resume_project_report.md` | polish the repository landing page and resume summary next |
| EXP-20260511-010-r2-final-repository-polish | N/A | R2 | Windows RTX 4060 Ti | `scripts/run_resume_demo.py` | 0f7d4a6 | success | final repository polish and showcase checklists created | `docs/quickstart.md` | prepare final resume wording and visibility decision next |
| EXP-20260511-011-t1-formal-training-roadmap | N/A | T1 | Windows RTX 4060 Ti | `configs/windows/smoke_cuda_10m.json` | 4d7ba0a | success | formal training roadmap and dataset/tokenizer plan created | `docs/t1_formal_training_roadmap.md` | define the BPE tokenizer plan next |
| EXP-20260512-001-t2-bpe-tokenizer-plan | N/A | T2 | Windows RTX 4060 Ti | `configs/windows/smoke_cuda_10m.json` | ad08cc2 | success | BPE tokenizer plan created | `docs/t2_bpe_tokenizer_plan.md` | run tokenizer environment checks next |
| EXP-20260512-002-t2-1-tokenizer-environment-check | N/A | T2.1 | Windows RTX 4060 Ti | `scripts/check_tokenizer_env.py` | e908069 | success | tokenizer environment checked | `docs/t2_1_tokenizer_environment_check.md` | train a tiny BPE tokenizer next only if the chosen dependency path stays approved |
| EXP-20260512-003-t2-2-tiny-bpe-tokenizer-artifact | N/A | T2.2 | Windows RTX 4060 Ti | `scripts/train_tiny_bpe_tokenizer.py` | 088e393 | success | tiny BPE tokenizer artifact created from local sample corpus | `docs/t2_2_tiny_bpe_tokenizer_artifact.md` | run a BPE tokenizer integration smoke next before changing the formal config |
| EXP-20260512-004-t2-3-bpe-tokenizer-integration-smoke | N/A | T2.3 | Windows RTX 4060 Ti | `scripts/inspect_bpe_integration_smoke.py` | 7d1dd5e | success | tiny BPE tokenizer passed dataset/model/loss integration smoke | `docs/t2_3_bpe_integration_smoke.md` | define formal tokenizer config fields and validator checks next |
| EXP-20260512-005-t2-4-tokenizer-config-schema-update | N/A | T2.4 | Windows RTX 4060 Ti | `configs/windows/bpe_toy_512_smoke.json` | 2ca1bb2 | success | tokenizer config schema and validator updated for BPE artifact paths | `docs/t2_4_tokenizer_config_schema_update.md` | migrate or split the legacy tokenizer configs next |
| EXP-20260514-006-t2-5-tokenizer-config-migration | N/A | T2.5 | Windows RTX 2080 Ti | `configs/windows/byte_smoke_10m.json` | 70663f1 | success | tokenizer configs split into byte smoke, toy BPE smoke, and formal BPE placeholder | `docs/t2_5_tokenizer_config_migration.md` | plan a small real dataset path next |
| EXP-20260514-007-t3-small-real-dataset-plan | N/A | T3 | Windows RTX 2080 Ti | `docs/t3_small_real_dataset_plan.md` | fc96288 | success | small real dataset plan created | `docs/t3_small_real_dataset_plan.md` | create the real corpus directory skeleton and data intake checklist next |
| EXP-20260514-008-t4-real-corpus-intake-structure | N/A | T4 | Windows RTX 2080 Ti | `docs/t4_real_corpus_intake_structure.md` | b06d52c | success | real corpus intake structure and data checklist created | `docs/t4_real_corpus_intake_structure.md` | choose the first approved local corpus source next |
| EXP-20260514-009-t4-1-first-corpus-source-decision | N/A | T4.1 | Windows RTX 2080 Ti | `docs/t4_1_first_corpus_source_decision.md` | e8e7392 | success | first corpus source decision gate and schema created; awaiting user-approved source | `docs/t4_1_first_corpus_source_decision.md` | provide one approved local source path next |
| EXP-20260514-010-t4-2s-synthetic-seed-source-decision | N/A | T4.2S | Windows RTX 2080 Ti | `docs/t4_2s_synthetic_seed_source_decision.md` | 6ed333b | success | synthetic seed corpus source decision created | `docs/t4_2s_synthetic_seed_source_decision.md` | create the synthetic seed corpus next |
| EXP-20260514-011-t4-3-synthetic-seed-corpus | N/A | T4.3 | Windows RTX 2080 Ti | `docs/t4_3_synthetic_seed_corpus.md` | a67cd43 | success | project-authored synthetic seed corpus created | `docs/t4_3_synthetic_seed_corpus.md` | plan the real data intake and cleaning scripts next |
| EXP-20260514-012-t5-real-data-intake-cleaning-script-plan | N/A | T5 | Windows RTX 2080 Ti | `docs/t5_real_data_intake_cleaning_script_plan.md` | a46b493 | success | future intake and cleaning script responsibilities documented for the synthetic seed corpus path | `docs/t5_real_data_intake_cleaning_script_plan.md` | implement a minimal synthetic-seed-only intake and cleaning script next |
| EXP-20260514-013-t5-1-synthetic-seed-intake-cleaning-script | N/A | T5.1 | Windows RTX 2080 Ti | `scripts/intake_synthetic_seed_corpus.py` | e2ad9c5 | success | synthetic seed corpus intake and cleaning script completed | `docs/t5_1_synthetic_seed_intake_cleaning.md` | plan a formal BPE 8k tokenizer step or a validation loop next |
| EXP-20260514-014-t5-2-bpe-8k-tokenizer-training-plan | N/A | T5.2 | Windows RTX 2080 Ti | `docs/t5_2_bpe_8k_tokenizer_training_plan.md` | 8455315 | success | BPE 8k tokenizer training plan created | `docs/t5_2_bpe_8k_tokenizer_training_plan.md` | train a formal-path synthetic-corpus tokenizer smoke artifact next |
| EXP-20260514-015-t5-3-bpe-8k-tokenizer-artifact | N/A | T5.3 | Windows RTX 2080 Ti | `scripts/train_bpe_8k_tokenizer.py` | f6e9f41 | success | educode_bpe_8k tokenizer artifact trained on synthetic seed corpus | `docs/t5_3_bpe_8k_tokenizer_artifact.md` | validate the formal 8k config path against the new artifact next |
| EXP-20260514-016-t5-4-bpe-8k-config-linkage-validation | N/A | T5.4 | Windows RTX 2080 Ti | `configs/windows/bpe_8k_formal_placeholder.json` | 494bf9c | success | BPE tokenizer artifact linked to formal config placeholder | `docs/t5_4_bpe_8k_config_linkage.md` | plan a validation loop or run a BPE-based smoke next |
| EXP-20260514-017-t5-5-bpe-data-model-loss-smoke | N/A | T5.5 | Windows RTX 2080 Ti | `scripts/inspect_bpe_data_model_loss_smoke.py` | 0f24bd9 | success | BPE processed-data model/loss smoke completed | `docs/t5_5_bpe_data_model_loss_smoke.md` | plan a validation loop next |
| EXP-20260514-018-t6-validation-loop-plan | N/A | T6 | Windows RTX 2080 Ti | `docs/t6_validation_loop_plan.md` | d128bd6 | success | validation loop plan created | `docs/t6_validation_loop_plan.md` | implement a bounded validation-loop smoke script next |
| EXP-20260514-019-t6-1-validation-loop-smoke | N/A | T6.1 | Windows RTX 2080 Ti | `scripts/inspect_validation_loop_smoke.py` | 86349bc | success | one-batch train/val loss smoke completed | `docs/t6_1_validation_loop_smoke.md` | plan a small real-data training stage next |
| EXP-20260514-020-t7-small-real-data-training-plan | N/A | T7 | Windows RTX 2080 Ti | `docs/t7_small_real_data_training_plan.md` | 6484840 | success | small real-data training plan created | `docs/t7_small_real_data_training_plan.md` | implement a bounded small real-data training script next |
| EXP-20260514-021-t7-1-50-step-small-real-data-training | `20260514_024451_windows_cuda_50_step_small_real_data_training` | windows_cuda | Windows RTX 2080 Ti | `configs/windows/bpe_8k_formal_placeholder.json` | d8c883c | success | bounded 50-step synthetic-seed small training completed with periodic validation, checkpoint reload, generation, and structured logs | `docs/t7_1_50_step_small_real_data_training.md` | review the bounded small-training artifacts before any longer run |
| EXP-20260514-022-t7-2-50-step-small-real-data-training-review | `20260514_024451_windows_cuda_50_step_small_real_data_training` | review | Windows RTX 2080 Ti | `configs/windows/bpe_8k_formal_placeholder.json` | e63888b | success | 50-step small training run reviewed and accepted | `docs/t7_2_50_step_small_real_data_training_review.md` | prepare a bounded 100-step follow-up plan or run next |
| EXP-20260514-023-t7-3-100-step-small-training-plan | N/A | T7.3 | Windows RTX 2080 Ti | `docs/t7_3_100_step_small_training_plan.md` | 0836c12 | success | bounded 100-step small training plan created | `docs/t7_3_100_step_small_training_plan.md` | implement the bounded 100-step small training run next |
| EXP-20260514-024-t7-4-100-step-small-real-data-training | `20260514_030554_windows_cuda_100_step_small_real_data_training` | windows_cuda | Windows RTX 2080 Ti | `configs/windows/bpe_8k_formal_placeholder.json` | 4e4488f | success | bounded 100-step small training run completed | `docs/t7_4_100_step_small_real_data_training.md` | review the bounded 100-step small-training artifacts next |
| EXP-20260514-025-t7-5-100-step-small-training-review | `20260514_030554_windows_cuda_100_step_small_real_data_training` | review | Windows RTX 2080 Ti | `configs/windows/bpe_8k_formal_placeholder.json` | 4f9324e | success | 100-step small training run reviewed and accepted as pipeline validation | `docs/t7_5_100_step_small_training_review.md` | compare the 50-step and 100-step runs next, then plan A100/100M |
| EXP-20260514-026-t7-6-50-vs-100-step-comparison | N/A | T7.6 | Windows RTX 2080 Ti | `docs/t7_6_50_vs_100_step_comparison.md` | pending local commit | success | 50-step and 100-step small training runs compared | `docs/t7_6_50_vs_100_step_comparison.md` | move to T8 A100/100M planning next |

Notes:
- These entries are documentation / planning records, not training runs.
- No fake training metrics or fake run outputs are recorded here.

## 5. Planned Smoke Experiments

| planned_experiment | hardware | config | goal | prerequisite | success_criteria | current_status |
|---|---|---|---|---|---|---|
| Windows one-step smoke | Windows RTX 4060 Ti | `configs/windows/smoke_cuda_10m.json` | verify the smallest end-to-end CUDA smoke path on the local Windows machine | W2-W10.11 complete | one-step smoke completed with checkpoint, generation, and logging artifacts | success |
| Windows minimal multi-step training loop | Windows RTX 4060 Ti | `configs/windows/smoke_cuda_10m.json` | extend the smoke path into a carefully bounded repeated loop | W10.12 one-step smoke accepted and W10.13 review complete | one-step smoke completed; minimal training loop not started yet | planned |
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
