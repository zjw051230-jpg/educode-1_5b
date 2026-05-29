# Run Summary: 20260529_171209_fineweb_edu_5gb_300m_10step_public16k_seq1024_sdpa_memory_preflight

## Goal
Validate the bounded A100/A800 training chain for fineweb_edu_5gb_300m_10step_public16k_seq1024_sdpa_memory_preflight.

## Hardware
cuda / a100_cuda

## Config Path
/workspace/educode-1_5b/experiments/a100/fineweb_edu_5gb_300m_10step_public16k_seq1024_sdpa_memory_preflight/run_config.json

## Result
success

## Key Metrics
- run_id: 20260529_171209_fineweb_edu_5gb_300m_10step_public16k_seq1024_sdpa_memory_preflight
- run_name: fineweb_edu_5gb_300m_10step_public16k_seq1024_sdpa_memory_preflight
- config_path: configs/a100/fineweb_edu_5gb_300m_10step_public16k_seq1024_sdpa_memory_preflight.json
- output_dir: experiments/a100/fineweb_edu_5gb_300m_10step_public16k_seq1024_sdpa_memory_preflight
- runtime_device: cuda
- runtime_device_reason: config_cuda
- runtime_dtype: bf16
- max_steps: 10
- gradient_accumulation_steps: 4
- eval_interval: 10
- batch_size: 4
- sequence_length: 1024
- data_loading_mode: streaming
- streaming_batches_used: 41
- host_ram_efficient_batching: True
- batch_precompute_disabled: True
- train_batches_used: 40
- val_batches_used: 1
- train_sampling_policy: shuffle_buffer
- val_sampling_policy: shuffle_buffer
- val_shuffle_seed: 7331
- val_shuffle_buffer_size: 64
- validation_max_blocks_per_document: 8
- validation_unique_doc_count: 4
- validation_batches_evaluated: 1
- validation_tokens_evaluated: 4096
- validation_prefix_only_risk: False
- train_data_probe: {'split_name': 'train', 'records_seen': 1024, 'docs_used': 1024, 'empty_text_count': 0, 'token_ids_streamed': 1184, 'blocks_yielded': 160, 'available_batches': 40, 'required_batches': 40, 'used_batches': 40, 'sequence_length': 1024, 'batch_size': 4, 'cycle_restarts': 0, 'streaming_mode': True, 'host_ram_efficient_batching': True, 'batch_precompute_disabled': True, 'sampling_policy': 'shuffle_buffer', 'shuffle_seed': 1337, 'shuffle_buffer_size': 1024, 'documents_buffered_total': 1024, 'max_shuffle_buffer_occupancy': 1024, 'shuffle_buffer_underfilled': False, 'bounded_prefix_batches_only': False, 'last_shuffle_seed_used': 1337, 'max_blocks_per_document': None, 'unique_doc_count': 1}
- val_data_probe: {'split_name': 'val', 'records_seen': 67, 'docs_used': 67, 'empty_text_count': 0, 'token_ids_streamed': 3198, 'blocks_yielded': 4, 'available_batches': 1, 'required_batches': 1, 'used_batches': 1, 'sequence_length': 1024, 'batch_size': 4, 'cycle_restarts': 0, 'streaming_mode': True, 'host_ram_efficient_batching': True, 'batch_precompute_disabled': True, 'sampling_policy': 'shuffle_buffer', 'shuffle_seed': 7331, 'shuffle_buffer_size': 64, 'documents_buffered_total': 67, 'max_shuffle_buffer_occupancy': 64, 'shuffle_buffer_underfilled': False, 'bounded_prefix_batches_only': False, 'last_shuffle_seed_used': 7331, 'max_blocks_per_document': 8, 'unique_doc_count': 4}
- tokenizer_vocab_size: 16384
- exact_parameter_count: 336630784
- first_train_loss: 9.911758
- final_train_loss: 2.392136
- final_val_loss: 9.044042
- loss_all_finite: True
- val_loss_all_finite: True
- grad_all_finite: True
- grad_norm_final: 0.796365
- metrics_path: experiments/a100/fineweb_edu_5gb_300m_10step_public16k_seq1024_sdpa_memory_preflight/metrics.jsonl
- validation_metrics_path: experiments/a100/fineweb_edu_5gb_300m_10step_public16k_seq1024_sdpa_memory_preflight/validation_metrics.jsonl
- metrics_rows: 10
- validation_rows: 1
- expected_validation_rows: 1
- tokens_seen: 163840
- elapsed_seconds: 6.034375
- approximate_tokens_per_sec: 27151.11506
- checkpoint_path: experiments/a100/fineweb_edu_5gb_300m_10step_public16k_seq1024_sdpa_memory_preflight/checkpoints/checkpoint_step_0010.pt
- checkpoint_path_starts_with_output_dir: True
- checkpoint_reload_match: True
- last_gpu_memory_allocated_gib: 2.649026
- last_gpu_memory_reserved_gib: 8.412109
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
- post_run_artifact_validation: {'passed': True, 'blockers': [], 'summary_json_path': 'experiments/a100/fineweb_edu_5gb_300m_10step_public16k_seq1024_sdpa_memory_preflight/summary.json', 'metrics_path': 'experiments/a100/fineweb_edu_5gb_300m_10step_public16k_seq1024_sdpa_memory_preflight/metrics.jsonl', 'validation_metrics_path': 'experiments/a100/fineweb_edu_5gb_300m_10step_public16k_seq1024_sdpa_memory_preflight/validation_metrics.jsonl', 'run_config_path': 'experiments/a100/fineweb_edu_5gb_300m_10step_public16k_seq1024_sdpa_memory_preflight/run_config.json', 'run_metadata_path': 'experiments/a100/fineweb_edu_5gb_300m_10step_public16k_seq1024_sdpa_memory_preflight/run_metadata.json', 'metrics_rows_actual': 10, 'validation_rows_actual': 1, 'expected_metrics_rows': 10, 'expected_validation_rows': 1, 'checked_at': '2026-05-29T17:12:31.323814+00:00'}

## Generation Preview


## Notes
This script uses the current core model implementation without adding new core-model features. Scheduler fields are recorded as present but not applied unless a future implementation actually applies a scheduler.

## Next Step
Review the bounded GPU artifacts with the post-run validator before making any model-quality claims.
