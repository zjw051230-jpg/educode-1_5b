# D17.2 Human Review Sampling Plan

## 1. Purpose
The purpose of this plan is to define a lightweight human sampling pass before any future D17.3 promotion step.

This sampling plan does not change the D17.2 automated review-gate outcome.
It is a follow-up recommendation only.

## 2. Sampling Rule
For each worker, sample `3` files with this priority:
- `1` `.py` file
- `1` `.md` file
- `1` longest or shortest file from that worker batch

Recommended worker-level sampling targets:

### CC-1
- `.py`: `data/real_corpus/draft_queue/domain_synthetic_batch_03/cc1_ml_foundations/loss_validation/tiny_batch_loss_sanity_check.py`
- `.md`: `data/real_corpus/draft_queue/domain_synthetic_batch_03/cc1_ml_foundations/loss_validation/cross_entropy_next_token_objective.md`
- longest/shortest: `data/real_corpus/draft_queue/domain_synthetic_batch_03/cc1_ml_foundations/optimization/finite_gradient_check_helper.py`

### CC-2
- `.py`: `data/real_corpus/draft_queue/domain_synthetic_batch_03/cc2_python_data_systems/jsonl_pipeline/jsonl_line_by_line_loader.py`
- `.md`: `data/real_corpus/draft_queue/domain_synthetic_batch_03/cc2_python_data_systems/jsonl_pipeline/draft_queue_vs_formal_corpus_boundaries.md`
- longest/shortest: `data/real_corpus/draft_queue/domain_synthetic_batch_03/cc2_python_data_systems/config_metrics/config_validation_error_formatting.py`

### CC-3
- `.py`: `data/real_corpus/draft_queue/domain_synthetic_batch_03/cc3_transformer_architecture/decoder_only/stacked_block_shape_trace.py`
- `.md`: `data/real_corpus/draft_queue/domain_synthetic_batch_03/cc3_transformer_architecture/attention_masking/why_future_tokens_must_be_hidden.md`
- longest/shortest: `data/real_corpus/draft_queue/domain_synthetic_batch_03/cc3_transformer_architecture/embeddings_logits/embedding_table_shape_check.py`

### CC-4
- `.py`: `data/real_corpus/draft_queue/domain_synthetic_batch_03/cc4_training_runtime_systems/experiment_logging/summary_data_dict_pattern.py`
- `.md`: `data/real_corpus/draft_queue/domain_synthetic_batch_03/cc4_training_runtime_systems/cuda_a100_profiling/a100_smoke_run_guardrails.md`
- longest/shortest: `data/real_corpus/draft_queue/domain_synthetic_batch_03/cc4_training_runtime_systems/experiment_logging/metrics_logging_per_step_vs_per_eval.md`

### CC-5
- `.py`: `data/real_corpus/draft_queue/domain_synthetic_batch_03/cc5_bilingual_qa/tokenizer_zh_en/simple_bilingual_token_count.py`
- `.md`: `data/real_corpus/draft_queue/domain_synthetic_batch_03/cc5_bilingual_qa/tokenizer_zh_en/zh_en_token_boundary_intuition.md`
- longest/shortest: `data/real_corpus/draft_queue/domain_synthetic_batch_03/cc5_bilingual_qa/debugging_zh_en/encoding_probe_snippet.py`

### CC-6
- `.py`: `data/real_corpus/draft_queue/domain_synthetic_batch_03/cc6_code_snippets/training_utilities/summary_data_dict_pattern.py`
- `.md`: `data/real_corpus/draft_queue/domain_synthetic_batch_03/cc6_code_snippets/tokenizer_utils/tokenizer_smoke_checklist.md`
- longest/shortest: `data/real_corpus/draft_queue/domain_synthetic_batch_03/cc6_code_snippets/training_utilities/validation_loss_helper.py`

## 3. Review Checklist
For each sampled file, check:
- whether the content stays centered on the project backbone
- whether it reads like original educational material
- whether it shows repetitive template flavor
- whether any external-text risk is present
- whether it makes misleading claims
- whether it is suitable for future entry into a formal synthetic corpus

## 4. Special Follow-Up
Give additional attention to the duplicate-filename pair flagged in D17.2:
- `cc4_training_runtime_systems/experiment_logging/summary_data_dict_pattern.py`
- `cc6_code_snippets/training_utilities/summary_data_dict_pattern.py`

The goal is to decide whether:
- both should remain with clearer differentiation,
- one should be renamed,
- or one should be dropped from later promotion consideration.

## 5. Interpretation
Human sampling is a recommended step before D17.3 promotion work.
It does not alter the D17.2 automated review-gate result by itself.
