# EduCode-1.5B Experiment Index

## 1. Purpose
The purpose of the experiment index is to:
- register all Windows / Mac / A100 / B200 experiments in one place
- connect config, run_id, hardware, git commit, result, and report references
- avoid scattered experiment tracking
- support later project reports and resume writing
- Project has completed the Windows smoke and bounded small-training validation milestones through T7.6.
- Tokenizer planning, BPE artifact creation, config migration, processed-data smoke, validation-loop smoke, and expanded-corpus small-training validation have been completed through D6.1.
- The current stage has moved from A100 scaling validation through permitted corpus expansion into bounded local expanded-BPE training validation.
- The project has validated real A100 single-GPU smoke behavior through 2.15B-scale optimizer profiling, but meaningful longer training is now limited by corpus scale, tokenizer quality, and approved data sources rather than raw GPU feasibility.

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
| EXP-20260514-026-t7-6-50-vs-100-step-comparison | N/A | T7.6 | Windows RTX 2080 Ti | `docs/t7_6_50_vs_100_step_comparison.md` | 46a6f3d | success | 50-step and 100-step small training runs compared | `docs/t7_6_50_vs_100_step_comparison.md` | move to T8 A100/100M planning next |
| EXP-20260514-027-t8-a100-100m-scaling-plan | N/A | T8 | A100 | `docs/t8_a100_100m_scaling_plan.md` | 538642d | success | A100 100M scaling plan created | `docs/t8_a100_100m_scaling_plan.md` | create the A100 100M config draft next |
| EXP-20260514-028-t8-1-a100-100m-config-draft | N/A | T8.1 | A100 | `configs/a100/educode_100m_a100_draft.json` | fd5686b | success | A100 100M draft config created and validated with a read-only inspection script | `docs/t8_1_a100_100m_config_draft.md` | prepare an A100 environment preflight checklist next |
| EXP-20260514-029-t8-2-a100-environment-preflight-checklist | N/A | T8.2 | A100 | `docs/t8_2_a100_environment_preflight_checklist.md` | ff508ed | success | A100 environment preflight checklist created | `docs/t8_2_a100_environment_preflight_checklist.md` | write an A100 100M forward/loss smoke plan or script after hardware is available |
| EXP-20260514-030-t8-3-a100-100m-forward-loss-smoke-plan | N/A | T8.3 | A100 | `docs/t8_3_a100_100m_forward_loss_smoke_plan.md` | 723dd50 | success | A100 100M forward/loss smoke plan created | `docs/t8_3_a100_100m_forward_loss_smoke_plan.md` | implement the A100 100M forward/loss smoke script after hardware is available |
| EXP-20260514-031-t8-4-a100-execution-runbook | N/A | T8.4 | A100 | `docs/t8_4_a100_execution_runbook.md` | ca5be8d | success | A100 execution runbook and handoff checklist created | `docs/t8_4_a100_execution_runbook.md` | implement the A100 forward/loss smoke script after A100 access is available |
| EXP-20260514-032-t8-5-a100-access-decision-checklist | N/A | T8.5 | A100 | `docs/t8_5_a100_access_decision_checklist.md` | 245ec3c | success | A100 access decision checklist created | `docs/t8_5_a100_access_decision_checklist.md` | create an A100 provider selection record after a provider or instance is chosen |
| EXP-20260514-033-t8-6-a100-provider-selection-record | N/A | T8.6 | A100 | `docs/t8_6_a100_provider_selection_record.md` | 4f8bf3f | success | selected first A100 target as single A100 80GB | `docs/t8_6_a100_provider_selection_record.md` | create an A100 first-session command checklist next |
| EXP-20260514-034-t8-7-a100-first-session-commands | N/A | T8.7 | A100 | `docs/t8_7_a100_first_session_commands.md` | d358742 | success | A100 first-session command checklist created | `docs/t8_7_a100_first_session_commands.md` | use the checklist on the selected A100 machine and report the environment and config-check outputs |
| EXP-20260514-035-t8-8-a100-first-session-report-template | N/A | T8.8 | A100 | `docs/t8_8_a100_first_session_report_template.md` | 0f77972 | success | A100 first-session report template created | `docs/t8_8_a100_first_session_report_template.md` | fill the template after the first real A100 session and use it to decide whether forward/loss smoke is approved |
| EXP-20260514-036-a1-a100-smoke-milestone-report | N/A | A1 | A100 | `docs/a1_a100_smoke_milestone_report.md` | c7fec6c | success | A100 80GB smoke results imported; 2.15B seq512 50-step optimizer profile passed | `docs/a1_a100_smoke_milestone_report.md` | use the imported A100 smoke milestone to plan D1 permitted corpus expansion and later longer training gates |
| EXP-20260515-001-d1-expand-permitted-corpus-plan | N/A | D1 | planning | `docs/d1_expand_permitted_corpus_plan.md` | 6c806ea | success | permitted corpus expansion plan created | `docs/d1_expand_permitted_corpus_plan.md` | use the source ladder and intake rules to define the first approved expanded corpus without downloading or copying external data |
| EXP-20260515-002-d2-expanded-synthetic-educational-corpus-plan | N/A | D2 | planning | `docs/d2_expanded_synthetic_educational_corpus_plan.md` | 6719621 | success | expanded synthetic educational corpus plan created | `docs/d2_expanded_synthetic_educational_corpus_plan.md` | use the content categories and directory plan to create a small inspectable synthetic_expanded source skeleton next |
| EXP-20260515-003-d2-1-synthetic-expanded-source-decision | N/A | D2.1 | planning | `docs/d2_1_synthetic_expanded_source_decision.md` | 7df1bf4 | success | expanded synthetic corpus source decision and directory skeleton created | `docs/d2_1_synthetic_expanded_source_decision.md` | create the first small inspectable synthetic_expanded content batch next without introducing external corpus data |
| EXP-20260515-004-d2-2-first-expanded-synthetic-corpus-batch | N/A | D2.2 | data | `docs/d2_2_first_expanded_synthetic_corpus_batch.md` | 2fc6857 | success | first expanded synthetic corpus batch created | `docs/d2_2_first_expanded_synthetic_corpus_batch.md` | intake the expanded synthetic corpus and produce processed JSONL plus train/val split next |
| EXP-20260515-005-d3-synthetic-expanded-intake | N/A | D3 | data | `scripts/intake_synthetic_expanded_corpus.py` | ff5a1d6 | success | expanded synthetic corpus intake and train/val split completed | `docs/d3_synthetic_expanded_intake_cleaning.md` | train an updated BPE tokenizer on the expanded synthetic corpus next |
| EXP-20260515-006-d4-expanded-bpe-tokenizer | N/A | D4 | tokenizer | `scripts/train_expanded_bpe_tokenizer.py` | c977f5b | success | expanded synthetic corpus BPE tokenizer artifact trained | `docs/d4_expanded_bpe_tokenizer.md` | run an expanded BPE data/model/loss smoke next |
| EXP-20260515-007-d5-expanded-bpe-data-model-loss-smoke | N/A | D5 | smoke | `scripts/inspect_expanded_bpe_data_model_loss_smoke.py` | a3d005d | success | expanded BPE processed-data model/loss smoke completed | `docs/d5_expanded_bpe_data_model_loss_smoke.md` | write an expanded corpus small-training plan next |
| EXP-20260515-008-d6-expanded-corpus-small-training-plan | N/A | D6 | planning | `docs/d6_expanded_corpus_small_training_plan.md` | 6281623 | success | expanded corpus small training plan created | `docs/d6_expanded_corpus_small_training_plan.md` | implement a bounded 50-step expanded BPE training run next |
| EXP-20260515-009-d6-1-50-step-expanded-bpe-training | `20260515_014657_windows_cuda_50_step_expanded_bpe_training` | D6.1 | Windows RTX 2080 Ti | `configs/windows/bpe_expanded_8k_smoke.json` | 42ef3dd | success | bounded 50-step expanded BPE training completed with periodic validation, checkpoint reload, and structured logs | `docs/d6_1_50_step_expanded_bpe_training.md` | review the bounded expanded-BPE training artifacts before any longer or non-local run |
| EXP-20260515-010-d6-2-50-step-expanded-bpe-training-review | `20260515_014657_windows_cuda_50_step_expanded_bpe_training` | D6.2 | Windows RTX 2080 Ti | `configs/windows/bpe_expanded_8k_smoke.json` | 47d562c | success | 50-step expanded BPE training run reviewed and accepted | `docs/d6_2_50_step_expanded_bpe_training_review.md` | prepare a bounded 100-step expanded-BPE training plan or run next |
| EXP-20260515-011-d6-3-100-step-expanded-bpe-training-plan | N/A | D6.3 | planning | `docs/d6_3_100_step_expanded_bpe_training_plan.md` | b2566dd | success | 100-step expanded BPE training plan created | `docs/d6_3_100_step_expanded_bpe_training_plan.md` | implement a bounded 100-step expanded BPE training run next |
| EXP-20260515-012-d6-4-100-step-expanded-bpe-training | `20260515_023640_windows_cuda_100_step_expanded_bpe_training` | D6.4 | Windows RTX 2080 Ti | `configs/windows/bpe_expanded_8k_smoke.json` | 40c35a6 | success | 100-step expanded BPE training completed | `docs/d6_4_100_step_expanded_bpe_training.md` | review the bounded 100-step expanded-BPE training artifacts before any longer or non-local run |
| EXP-20260515-013-d6-5-100-step-expanded-bpe-training-review | `20260515_023640_windows_cuda_100_step_expanded_bpe_training` | D6.5 | Windows RTX 2080 Ti | `configs/windows/bpe_expanded_8k_smoke.json` | 1898973 | success | 100-step expanded BPE training run reviewed and accepted | `docs/d6_5_100_step_expanded_bpe_training_review.md` | compare the bounded 50-step and 100-step expanded-BPE runs next |
| EXP-20260515-014-d6-6-50-vs-100-step-expanded-bpe-comparison | N/A | D6.6 | comparison | `docs/d6_6_50_vs_100_step_expanded_bpe_comparison.md` | 2c96bf8 | success | 50-step and 100-step expanded BPE training runs compared | `docs/d6_6_50_vs_100_step_expanded_bpe_comparison.md` | expand the approved corpus before any longer expanded-BPE training |
| EXP-20260515-015-d7-expanded-synthetic-corpus-batch-2 | N/A | D7 | data | `docs/d7_expanded_synthetic_corpus_batch_2.md` | 7656adb | success | second expanded synthetic corpus batch created, bringing the approved synthetic_expanded source to 45 files | `docs/d7_expanded_synthetic_corpus_batch_2.md` | re-run expanded corpus intake before future tokenizer or training comparisons |
| EXP-20260515-016-d8-synthetic-expanded-45-file-intake | N/A | D8 | data | `scripts/intake_synthetic_expanded_corpus.py` | ae64aea | success | 45-file expanded synthetic corpus intake completed | `docs/d8_synthetic_expanded_45_file_intake.md` | retrain the expanded/domain BPE tokenizer on the refreshed 45-file corpus next |
| EXP-20260515-017-d9-domain-bpe-tokenizer-45-file-corpus | N/A | D9 | tokenizer | `scripts/train_domain_bpe_tokenizer_45file.py` | 5954b50 | success | domain BPE tokenizer trained on 45-file corpus | `docs/d9_domain_bpe_tokenizer_45file.md` | run a domain BPE data/model/loss smoke next |
| EXP-20260515-018-d10-domain-bpe-data-model-loss-smoke | N/A | D10 | smoke | `configs/windows/bpe_domain_8k_smoke.json` | 0372085 | success | domain BPE processed-data model/loss smoke completed | `docs/d10_domain_bpe_data_model_loss_smoke.md` | prepare a domain BPE small training plan next |
| EXP-20260515-019-d11-domain-bpe-small-training-plan | N/A | D11 | planning | `docs/d11_domain_bpe_small_training_plan.md` | b525118 | success | domain BPE small training plan created | `docs/d11_domain_bpe_small_training_plan.md` | implement a bounded 50-step domain BPE small training run next |
| EXP-20260515-020-d11-1-50-step-domain-bpe-training | `20260515_034606_windows_cuda_50_step_domain_bpe_training` | D11.1 | Windows RTX 2080 Ti | `configs/windows/bpe_domain_8k_smoke.json` | 9c62bb6 | success | 50-step domain BPE training completed | `docs/d11_1_50_step_domain_bpe_training.md` | review the bounded domain BPE training artifacts before any longer or non-local run |
| EXP-20260516-001-d11-2-50-step-domain-bpe-training-review | `20260515_034606_windows_cuda_50_step_domain_bpe_training` | D11.2 | review | `docs/d11_2_50_step_domain_bpe_training_review.md` | fcd34c4 | success | 50-step domain BPE training run reviewed and accepted | `docs/d11_2_50_step_domain_bpe_training_review.md` | write a bounded 100-step domain BPE plan or expand the corpus next |
| EXP-20260516-002-d11-3-100-step-domain-bpe-training-plan | N/A | D11.3 | planning | `docs/d11_3_100_step_domain_bpe_training_plan.md` | pending local commit | success | 100-step domain BPE training plan created | `docs/d11_3_100_step_domain_bpe_training_plan.md` | implement a bounded 100-step domain BPE training run next |

Notes:
- These entries include planning records, inspections, and real bounded local training runs.
- Only summary/report metadata is committed here; raw logs, checkpoints, and datasets remain ignored.

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
