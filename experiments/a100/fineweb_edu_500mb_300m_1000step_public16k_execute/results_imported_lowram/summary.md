# Run Summary: 20260524_050841_fineweb_edu_500mb_300m_1000step_public16k_execute

## Goal
Validate the bounded A100/A800 training chain for fineweb_edu_500mb_300m_1000step_public16k_execute.

## Hardware
cuda / a100_cuda

## Config Path
/workspace/educode-1_5b/experiments/a100/fineweb_edu_500mb_300m_1000step_public16k_execute/run_config.json

## Result
success

## Key Metrics
- run_id: 20260524_050841_fineweb_edu_500mb_300m_1000step_public16k_execute
- run_name: fineweb_edu_500mb_300m_1000step_public16k_execute
- config_path: configs/a100/fineweb_edu_500mb_300m_1000step_public16k_lowram_execute.json
- output_dir: experiments/a100/fineweb_edu_500mb_300m_1000step_public16k_execute
- runtime_device: cuda
- runtime_device_reason: config_cuda
- runtime_dtype: bf16
- max_steps: 1000
- gradient_accumulation_steps: 1
- eval_interval: 100
- batch_size: 1
- sequence_length: 512
- train_batches_used: 1000
- val_batches_used: 10
- train_data_probe: {'split_name': 'train', 'records_seen': 510, 'docs_used': 510, 'empty_text_count': 0, 'token_ids_collected': 512048, 'available_batches': 511536, 'required_batches': 1000, 'used_batches': 1000, 'sequence_length': 512, 'batch_size': 1}
- val_data_probe: {'split_name': 'val', 'records_seen': 7, 'docs_used': 7, 'empty_text_count': 0, 'token_ids_collected': 6211, 'available_batches': 5699, 'required_batches': 10, 'used_batches': 10, 'sequence_length': 512, 'batch_size': 1}
- tokenizer_vocab_size: 16384
- exact_parameter_count: 336106496
- first_train_loss: 9.873169
- final_train_loss: 0.213472
- final_val_loss: 11.513049
- loss_all_finite: True
- val_loss_all_finite: True
- grad_all_finite: True
- grad_norm_final: 0.81053
- metrics_path: experiments/a100/fineweb_edu_500mb_300m_1000step_public16k_execute/metrics.jsonl
- validation_metrics_path: experiments/a100/fineweb_edu_500mb_300m_1000step_public16k_execute/validation_metrics.jsonl
- metrics_rows: 1000
- validation_rows: 10
- expected_validation_rows: 10
- tokens_seen: 512000
- elapsed_seconds: 55.984806
- approximate_tokens_per_sec: 9145.338413
- checkpoint_path: experiments/a100/fineweb_edu_500mb_300m_1000step_public16k_execute/checkpoints/checkpoint_step_1000.pt
- checkpoint_path_starts_with_output_dir: True
- checkpoint_reload_match: True
- last_gpu_memory_allocated_gib: 2.543504
- last_gpu_memory_reserved_gib: 3.617188
- declared_model_features: {'norm_type': 'rmsnorm', 'ffn_type': 'swiglu', 'position_encoding': 'learned_position_embedding', 'tie_embeddings': False, 'attention_backend': 'sdpa'}
- current_core_model_features: {'norm_type': 'rmsnorm', 'ffn_type': 'swiglu', 'position_encoding': 'learned_position_embedding', 'tie_embeddings': False, 'attention_backend': 'sdpa'}
- declared_vs_core_feature_mismatches: []
- scheduler_config_present: True
- scheduler_applied: False
- scheduler_policy: not_applied
- scheduler_config_present_but_not_applied: True
- bounded_prefix_batches_only: True
- success: True
- post_run_artifact_validation: {'passed': True, 'blockers': [], 'summary_json_path': 'experiments/a100/fineweb_edu_500mb_300m_1000step_public16k_execute/summary.json', 'metrics_path': 'experiments/a100/fineweb_edu_500mb_300m_1000step_public16k_execute/metrics.jsonl', 'validation_metrics_path': 'experiments/a100/fineweb_edu_500mb_300m_1000step_public16k_execute/validation_metrics.jsonl', 'run_config_path': 'experiments/a100/fineweb_edu_500mb_300m_1000step_public16k_execute/run_config.json', 'run_metadata_path': 'experiments/a100/fineweb_edu_500mb_300m_1000step_public16k_execute/run_metadata.json', 'metrics_rows_actual': 1000, 'validation_rows_actual': 10, 'expected_metrics_rows': 1000, 'expected_validation_rows': 10, 'checked_at': '2026-05-23T21:09:49.591270+00:00'}

## Generation Preview


## Notes
This script uses the current core model implementation without adding new core-model features. Scheduler fields are recorded as present but not applied unless a future implementation actually applies a scheduler.

## Next Step
Review the bounded GPU artifacts with the post-run validator before making any model-quality claims.
