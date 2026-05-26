# Run Summary: 20260526_192023_fineweb_edu_5gb_300m_1000step_public16k_execute

## Goal
Validate the bounded A100/A800 training chain for fineweb_edu_5gb_300m_1000step_public16k_execute.

## Hardware
cuda / a100_cuda

## Config Path
/workspace/educode-1_5b/experiments/a100/fineweb_edu_5gb_300m_1000step_public16k_execute/run_config.json

## Result
success

## Key Metrics
- run_id: 20260526_192023_fineweb_edu_5gb_300m_1000step_public16k_execute
- run_name: fineweb_edu_5gb_300m_1000step_public16k_execute
- config_path: configs/a100/fineweb_edu_5gb_300m_1000step_public16k_execute.json
- output_dir: experiments/a100/fineweb_edu_5gb_300m_1000step_public16k_execute
- runtime_device: cuda
- runtime_device_reason: config_cuda
- runtime_dtype: bf16
- max_steps: 1000
- gradient_accumulation_steps: 4
- eval_interval: 100
- batch_size: 8
- sequence_length: 512
- data_loading_mode: streaming
- streaming_batches_used: 4010
- host_ram_efficient_batching: True
- batch_precompute_disabled: True
- train_batches_used: 4000
- val_batches_used: 10
- train_sampling_policy: shuffle_buffer
- val_sampling_policy: sequential_prefix
- train_data_probe: {'split_name': 'train', 'records_seen': 1054, 'docs_used': 1054, 'empty_text_count': 0, 'token_ids_streamed': 32512, 'blocks_yielded': 32000, 'available_batches': 4000, 'required_batches': 4000, 'used_batches': 4000, 'sequence_length': 512, 'batch_size': 8, 'cycle_restarts': 0, 'streaming_mode': True, 'host_ram_efficient_batching': True, 'batch_precompute_disabled': True, 'sampling_policy': 'shuffle_buffer', 'shuffle_seed': 1337, 'shuffle_buffer_size': 1024, 'documents_buffered_total': 1054, 'max_shuffle_buffer_occupancy': 1024, 'shuffle_buffer_underfilled': False, 'bounded_prefix_batches_only': False, 'last_shuffle_seed_used': 1337}
- val_data_probe: {'split_name': 'val', 'records_seen': 1, 'docs_used': 1, 'empty_text_count': 0, 'token_ids_streamed': 592, 'blocks_yielded': 80, 'available_batches': 10, 'required_batches': 10, 'used_batches': 10, 'sequence_length': 512, 'batch_size': 8, 'cycle_restarts': 0, 'streaming_mode': True, 'host_ram_efficient_batching': True, 'batch_precompute_disabled': True, 'sampling_policy': 'sequential_prefix', 'shuffle_seed': None, 'shuffle_buffer_size': 1, 'documents_buffered_total': 0, 'max_shuffle_buffer_occupancy': 0, 'shuffle_buffer_underfilled': False, 'bounded_prefix_batches_only': True, 'last_shuffle_seed_used': None}
- tokenizer_vocab_size: 16384
- exact_parameter_count: 336106496
- first_train_loss: 9.869211
- final_train_loss: 3.160682
- final_val_loss: 9.214416
- loss_all_finite: True
- val_loss_all_finite: True
- grad_all_finite: True
- grad_norm_final: 1.001534
- metrics_path: experiments/a100/fineweb_edu_5gb_300m_1000step_public16k_execute/metrics.jsonl
- validation_metrics_path: experiments/a100/fineweb_edu_5gb_300m_1000step_public16k_execute/validation_metrics.jsonl
- metrics_rows: 1000
- validation_rows: 10
- expected_validation_rows: 10
- tokens_seen: 16384000
- elapsed_seconds: 341.633667
- approximate_tokens_per_sec: 47957.802693
- checkpoint_path: experiments/a100/fineweb_edu_5gb_300m_1000step_public16k_execute/checkpoints/checkpoint_step_1000.pt
- checkpoint_path_starts_with_output_dir: True
- checkpoint_reload_match: True
- last_gpu_memory_allocated_gib: 2.64512
- last_gpu_memory_reserved_gib: 8.416016
- declared_model_features: {'norm_type': 'rmsnorm', 'ffn_type': 'swiglu', 'position_encoding': 'learned_position_embedding', 'tie_embeddings': False, 'attention_backend': 'sdpa'}
- current_core_model_features: {'norm_type': 'rmsnorm', 'ffn_type': 'swiglu', 'position_encoding': 'learned_position_embedding', 'tie_embeddings': False, 'attention_backend': 'sdpa'}
- declared_vs_core_feature_mismatches: []
- scheduler_config_present: True
- scheduler_enabled: False
- scheduler_policy: constant
- scheduler_applied: False
- scheduler_config_present_but_not_applied: False
- learning_rate_mode: constant
- base_learning_rate: 0.0003
- final_learning_rate: 0.0003
- sampling_config_present: True
- sampling_policy: shuffle_buffer
- shuffle_seed: 1337
- shuffle_buffer_size: 1024
- bounded_prefix_batches_only: False
- success: True
- post_run_artifact_validation: {'passed': True, 'blockers': [], 'summary_json_path': 'experiments/a100/fineweb_edu_5gb_300m_1000step_public16k_execute/summary.json', 'metrics_path': 'experiments/a100/fineweb_edu_5gb_300m_1000step_public16k_execute/metrics.jsonl', 'validation_metrics_path': 'experiments/a100/fineweb_edu_5gb_300m_1000step_public16k_execute/validation_metrics.jsonl', 'run_config_path': 'experiments/a100/fineweb_edu_5gb_300m_1000step_public16k_execute/run_config.json', 'run_metadata_path': 'experiments/a100/fineweb_edu_5gb_300m_1000step_public16k_execute/run_metadata.json', 'metrics_rows_actual': 1000, 'validation_rows_actual': 10, 'expected_metrics_rows': 1000, 'expected_validation_rows': 10, 'checked_at': '2026-05-26T19:26:16.737694+00:00'}

## Generation Preview


## Notes
This script uses the current core model implementation without adding new core-model features. Scheduler fields are recorded as present but not applied unless a future implementation actually applies a scheduler.

## Next Step
Review the bounded GPU artifacts with the post-run validator before making any model-quality claims.
