# Run Summary: 20260523_211309_a100_fineweb_edu_50mb_300m_10step_smoke

## Goal
Validate the A100 FineWeb-Edu 300M 10-step training chain with the existing core model and mixed-domain 8k tokenizer.

## Hardware
cuda / a100_cuda

## Config Path
/workspace/educode-1_5b/experiments/a100/fineweb_edu_50mb_300m_10step_execute/run_config.json

## Result
success

## Key Metrics
- run_id: 20260523_211309_a100_fineweb_edu_50mb_300m_10step_smoke
- config_path: configs/a100/fineweb_edu_50mb_300m_10step_execute.json
- output_dir: experiments/a100/fineweb_edu_50mb_300m_10step_execute
- runtime_device: cuda
- runtime_device_reason: config_cuda
- runtime_dtype: bf16
- max_steps: 10
- gradient_accumulation_steps: 4
- eval_interval: 5
- batch_size: 8
- sequence_length: 512
- train_batches_used: 40
- val_batches_used: 2
- train_data_probe: {'split_name': 'train', 'records_seen': 140, 'docs_used': 140, 'empty_text_count': 0, 'token_ids_collected': 167913, 'available_batches': 20925, 'required_batches': 40, 'used_batches': 40, 'sequence_length': 512, 'batch_size': 8}
- val_data_probe: {'split_name': 'val', 'records_seen': 7, 'docs_used': 7, 'empty_text_count': 0, 'token_ids_collected': 8979, 'available_batches': 1058, 'required_batches': 2, 'used_batches': 2, 'sequence_length': 512, 'batch_size': 8}
- tokenizer_vocab_size: 8192
- exact_parameter_count: 319329280
- first_train_loss: 9.18121
- final_train_loss: 2.769437
- final_val_loss: 9.134018
- loss_all_finite: True
- val_loss_all_finite: True
- grad_all_finite: True
- grad_norm_final: 0.999918
- metrics_rows: 10
- validation_rows: 2
- tokens_seen: 163840
- elapsed_seconds: 3.788592
- approximate_tokens_per_sec: 43245.612399
- checkpoint_path: experiments/a100/fineweb_edu_50mb_300m_10step_execute/checkpoints/checkpoint_step_0010.pt
- checkpoint_reload_match: True
- last_gpu_memory_allocated_gib: 2.45762
- last_gpu_memory_reserved_gib: 7.830078
- declared_model_features: {'norm_type': 'rmsnorm', 'ffn_type': 'swiglu', 'position_encoding': 'rope', 'tie_embeddings': False, 'attention_backend': 'sdpa'}
- current_core_model_features: {'norm_type': 'rmsnorm', 'ffn_type': 'swiglu', 'position_encoding': 'learned_position_embedding', 'tie_embeddings': False, 'attention_backend': 'sdpa'}
- declared_vs_core_feature_mismatches: ["position_encoding: declared='rope', implemented='learned_position_embedding'"]
- scheduler_config_present_but_not_applied: True
- bounded_prefix_batches_only: True
- success: True

## Generation Preview


## Notes
This script uses the current core model implementation without adding new core-model features. The config still declares rope, but the current core model path uses learned position embeddings. Scheduler fields remain config-only in MVP-7.

## Next Step
Review the bounded A100 smoke artifacts and proceed only with an approved A100 execution session.
