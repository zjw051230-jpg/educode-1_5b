# D17.0 Draft Corpus Taxonomy and Worker Framework

## 1. Purpose
The purpose of D17.0 is to create a draft-only framework for future parallel educational corpus generation without placing any new text into the formal training corpus.

This step creates the draft queue taxonomy, a 120-topic registry, review-only templates, and worker governance documents.
It does not generate large body-text corpus files, does not run intake, does not train tokenizer or model artifacts, and does not approve any draft for training.

## 2. Files Added
Files added in D17.0:
- `data/real_corpus/draft_queue/domain_synthetic_batch_03/00_framework/topic_registry.jsonl`
- `data/real_corpus/draft_queue/domain_synthetic_batch_03/00_framework/draft_markdown_template.md`
- `data/real_corpus/draft_queue/domain_synthetic_batch_03/00_framework/draft_python_template.py`
- draft-queue taxonomy directories with leaf `.gitkeep` files only
- `docs/d17_parallel_corpus_generation_worker_plan.md`
- `docs/d17_draft_corpus_review_gate_plan.md`
- this report

## 3. Taxonomy Created
The draft queue taxonomy for `domain_synthetic_batch_03` is split into six worker-owned categories:
- `cc1_ml_foundations`
- `cc2_python_data_systems`
- `cc3_transformer_architecture`
- `cc4_training_runtime_systems`
- `cc5_bilingual_qa`
- `cc6_code_snippets`

Each category is further split into three subcategories so later workers can reserve topics in narrower subject lanes.

## 4. Topic Registry
The registry created in:
- `data/real_corpus/draft_queue/domain_synthetic_batch_03/00_framework/topic_registry.jsonl`

contains 120 reserved topics total:
- `MLF-001` through `MLF-020`
- `PDS-001` through `PDS-020`
- `TRF-001` through `TRF-020`
- `RTS-001` through `RTS-020`
- `BIL-001` through `BIL-020`
- `COD-001` through `COD-020`

Every row is initialized with:
- `status = "reserved_not_written"`
- `approved_for_training = false`
- `contains_external_text = false`
- `contains_private_data = false`

## 5. Templates and Guardrails
The framework templates mark all future drafts as:
- candidate only
- `synthetic_examples`
- review-only
- not approved for training

This keeps future worker output clearly separate from the approved corpus path.

## 6. Validation Result
D17.0 validation target:
- the registry is parseable as JSONL
- the registry contains 120 rows
- the taxonomy directories exist
- only leaf `.gitkeep` placeholders are present in the taxonomy tree

## 7. Why This Matters
This framework gives the project a controlled place to scale future draft generation without weakening provenance and review boundaries.

It also protects the backbone distinction already used elsewhere in the repo:
- project-authored educational backbone remains primary
- supplements and future drafts remain explicitly separated

## 8. What D17.0 Does Not Do
D17.0 does not:
- generate large educational corpus text
- place content into formal `raw` or `processed` corpus paths
- run intake or cleaning
- retrain tokenizers
- run training
- make model-quality claims
- approve any draft for training use

## 9. Next Step
Recommended next step:
- validate future written drafts against the registry and review gate before any separate promotion discussion
