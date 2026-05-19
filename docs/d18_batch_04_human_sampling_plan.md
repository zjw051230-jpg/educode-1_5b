# D18 Batch 04 Human Sampling Plan

## 1. Purpose
The purpose of this plan is to define a targeted human sampling pass after D18 automated validation and quality review.

This plan does not change the D18 automated outputs by itself.
It identifies the smallest manual review set that can confirm whether the quality-note clusters reflect acceptable drafting variation or template over-concentration.

## 2. Sampling Rule
For each worker, sample:
- `1` python file
- `1` markdown file
- `1` longest file from that worker batch

Priority rule:
- when a worker has `needs_edit` records, choose at least one sample that already carries a D18 quality note
- when a worker has no D18 quality notes, use the worker as a cleaner control group

## 3. Recommended Worker-Level Samples
### CC-1
- `.py`: `data/real_corpus/draft_queue/domain_synthetic_batch_04/cc1_ml_foundations/loss_validation/b04-mlf-0003_loss_validation_negative_log_likelihood_intuition_v01.py`
- `.md`: `data/real_corpus/draft_queue/domain_synthetic_batch_04/cc1_ml_foundations/loss_validation/b04-mlf-0001_loss_validation_next_token_alignment_v01.md`
- longest: `data/real_corpus/draft_queue/domain_synthetic_batch_04/cc1_ml_foundations/curriculum_notes/b04-mlf-0795_curriculum_notes_mixing_frequent_and_rare_tokens_v10.md`

Sampling goal:
- treat `CC-1` as a cleaner control group for what a fully passing block looks like

### CC-2
- `.py` and flagged note sample: `data/real_corpus/draft_queue/domain_synthetic_batch_04/cc2_python_data_systems/jsonl_pipeline/b04_pds_0001_line_by_line_reader.py`
- `.md`: `data/real_corpus/draft_queue/domain_synthetic_batch_04/cc2_python_data_systems/jsonl_pipeline/b04_pds_0004_utf8_field_preservation.md`
- longest: `data/real_corpus/draft_queue/domain_synthetic_batch_04/cc2_python_data_systems/safe_text_cleaning/b04_pds_0682_leading_trailing_space_trimming.py`

Sampling goal:
- check whether repeated internal lines and heavy review scaffolds make the whole worker block feel too formulaic

### CC-3
- `.py`: `data/real_corpus/draft_queue/domain_synthetic_batch_04/cc3_transformer_architecture/decoder_only/b04-trf-0071_decoder_only_071.py`
- `.md` and flagged note sample: `data/real_corpus/draft_queue/domain_synthetic_batch_04/cc3_transformer_architecture/decoder_only/b04-trf-0001_decoder_only_001.md`
- longest: `data/real_corpus/draft_queue/domain_synthetic_batch_04/cc3_transformer_architecture/layer_norm_residual/b04-trf-0638_layer_norm_residual_038.md`

Sampling goal:
- inspect whether the architectural explanations remain distinct enough from one another beyond the shared lesson scaffold

### CC-4
- `.py`: `data/real_corpus/draft_queue/domain_synthetic_batch_04/cc4_training_runtime_systems/checkpointing/b04-rts-0071_checkpointing_071_top_level_checkpoint_key_checks.py`
- `.md`: `data/real_corpus/draft_queue/domain_synthetic_batch_04/cc4_training_runtime_systems/checkpointing/b04-rts-0001_checkpointing_001_top_level_checkpoint_key_checks.md`
- longest: `data/real_corpus/draft_queue/domain_synthetic_batch_04/cc4_training_runtime_systems/throughput_profiles/b04-rts-0897_throughput_profiles_097_throughput_without_quality_claims.py`

Sampling goal:
- treat `CC-4` as the second cleaner control group for concise runtime-review writing

### CC-5
- `.py`: `data/real_corpus/draft_queue/domain_synthetic_batch_04/cc5_bilingual_qa/tokenizer_zh_en/b04_bil_0006_tokenizer_roundtrip_checks.py`
- `.md` and flagged note sample: `data/real_corpus/draft_queue/domain_synthetic_batch_04/cc5_bilingual_qa/tokenizer_zh_en/b04_bil_0001_tokenizer_token_boundary_intuition.md`
- longest: `data/real_corpus/draft_queue/domain_synthetic_batch_04/cc5_bilingual_qa/concept_contrast_zh_en/b04_bil_0990_concept_contrast_educational_draft_versus_formal_corpus.py`

Sampling goal:
- verify that bilingual pairing still teaches one shared idea cleanly and that the markdown scaffolds do not overwhelm the bilingual value

### CC-6
- `.py`: `data/real_corpus/draft_queue/domain_synthetic_batch_04/cc6_code_snippets/minimal_pytorch/b04-cod-0031_minimal_pytorch_031.py`
- `.md` and flagged note sample: `data/real_corpus/draft_queue/domain_synthetic_batch_04/cc6_code_snippets/minimal_pytorch/b04-cod-0001_minimal_pytorch_001.md`
- longest: `data/real_corpus/draft_queue/domain_synthetic_batch_04/cc6_code_snippets/source_category_tools/b04-cod-0900_source_category_tools_100.py`

Sampling goal:
- confirm whether the markdown note family is too repetitive relative to the stronger snippet-oriented python portion of the worker batch

## 4. Review Checklist
For each sampled file, check:
- whether the teaching point is distinct after one read
- whether the draft stays inside the CS / ML / Python / transformer-training backbone
- whether the file reads like original project-authored educational material instead of a near-template duplicate
- whether markdown scaffolding is helping clarity or simply repeating boilerplate
- whether bilingual pairs actually teach the same idea on both sides
- whether the file should remain unchanged, be edited, or be deprioritized for any later promotion discussion

## 5. Priority Interpretation
Priority order for manual attention:
1. `CC-2`
2. `CC-3`
3. markdown-heavy `CC-5`
4. markdown-heavy `CC-6`
5. `CC-1` and `CC-4` as cleaner comparison baselines

This ordering follows the D18 quality-note concentration rather than re-checking workers that already passed cleanly.
