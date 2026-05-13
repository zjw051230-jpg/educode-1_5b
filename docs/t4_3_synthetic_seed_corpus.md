# T4.3 Synthetic Seed Corpus

## 1. Purpose
The purpose of T4.3 is to create a small project-authored synthetic educational seed corpus.

## 2. Files Added
- `data/real_corpus/raw/synthetic_seed/README.md`
- `data/real_corpus/raw/synthetic_seed/transformer_notes.md`
- `data/real_corpus/raw/synthetic_seed/tokenizer_notes.md`
- `data/real_corpus/raw/synthetic_seed/training_loop_notes.md`
- `data/real_corpus/raw/synthetic_seed/loss_and_logits.txt`
- `data/real_corpus/raw/synthetic_seed/checkpoint_generation_notes.md`
- `data/real_corpus/raw/synthetic_seed/python_examples.py`
- `data/real_corpus/raw/synthetic_seed/bilingual_ml_notes.md`

## 3. Source Status
- `source_id`: `source_synthetic_seed_000001`
- `source_category`: `synthetic_examples`
- `approval_status`: `approved_for_training`
- `allowed_for_training`: `true`
- `allowed_to_commit`: `true`
- `privacy_risk`: `none`
- `external_download`: `false`

## 4. What It Does
This step:
- creates small synthetic CS/ML/code examples
- provides a seed corpus for future intake, cleaning, tokenizer, and data pipeline validation

## 5. What It Does Not Do
This step does not:
- download data
- use real external corpora
- train a tokenizer
- train a model
- write a data pipeline
- run training

## 6. Limitations
- the synthetic corpus is very small
- it does not represent real data distribution
- it cannot be used to claim formal pretraining quality
- later stages still need real or permissively licensed corpora

## 7. Next Step
Recommended next step:
- T5: Real Data Intake / Cleaning Script Plan
