# D17 Parallel Corpus Generation Worker Plan

## 1. Purpose
The purpose of this document is to define how multiple ClaudeCode workers can reserve and later draft candidate educational corpus files in parallel without writing directly into the approved training corpus.

This step is framework only.
It does not generate large body-text corpus files, does not approve any draft for training, and does not modify tokenizer, model, or training code.

## 2. Worker Topology
The draft queue root for this batch is:
- `data/real_corpus/draft_queue/domain_synthetic_batch_03/`

The worker split is:
- `CC1` → `cc1_ml_foundations`
- `CC2` → `cc2_python_data_systems`
- `CC3` → `cc3_transformer_architecture`
- `CC4` → `cc4_training_runtime_systems`
- `CC5` → `cc5_bilingual_qa`
- `CC6` → `cc6_code_snippets`

Each worker owns 20 reserved topics in `topic_registry.jsonl` for a total of 120 topics.

## 3. Directory Responsibilities
Category directories are intentionally separated by subject area and then by narrower subcategory:
- `cc1_ml_foundations/`
  - `loss_validation/`
  - `optimization/`
  - `evaluation_overfitting/`
- `cc2_python_data_systems/`
  - `jsonl_pipeline/`
  - `token_batching/`
  - `config_metrics/`
- `cc3_transformer_architecture/`
  - `decoder_only/`
  - `attention_masking/`
  - `embeddings_logits/`
- `cc4_training_runtime_systems/`
  - `checkpointing/`
  - `cuda_a100_profiling/`
  - `experiment_logging/`
- `cc5_bilingual_qa/`
  - `tokenizer_zh_en/`
  - `training_loop_zh_en/`
  - `debugging_zh_en/`
- `cc6_code_snippets/`
  - `minimal_pytorch/`
  - `tokenizer_utils/`
  - `training_utilities/`

## 4. Reservation Rules
Before writing a draft file, a worker should:
- choose only a row assigned to its `worker_id`
- keep the proposed filename and category path from the registry
- preserve `approved_for_training = false`
- preserve `contains_external_text = false`
- preserve `contains_private_data = false`
- treat the draft as review-only until a later review stage explicitly promotes it

Workers should not create alternative topic IDs or move topics across categories without a registry update.

## 5. Writing Rules
Allowed future outputs in this queue:
- candidate markdown drafts
- candidate python snippet drafts
- small metadata updates to the registry after review workflow is defined

Not allowed in this queue:
- direct writes into `data/real_corpus/raw/`
- direct writes into `data/real_corpus/processed/`
- bulk generated corpus dumps
- copied external text
- private data
- tokenizer or model artifacts

## 6. Expected Draft Shape
Workers should start from one of the framework templates:
- `draft_markdown_template.md`
- `draft_python_template.py`

These templates force every draft to declare that it is:
- candidate only
- synthetic_examples category
- review-only
- not approved for training

## 7. Why This Split Matters
This worker plan exists so that future parallel drafting can scale without blurring the line between:
- candidate educational writing
- approved formal corpus assets
- training-ready processed data

The queue is for controlled reservation and review, not automatic promotion.

## 8. Next Step
Recommended next step:
- define the human or scripted review workflow that can move a topic from `reserved_not_written` to reviewed draft states without granting training approval
