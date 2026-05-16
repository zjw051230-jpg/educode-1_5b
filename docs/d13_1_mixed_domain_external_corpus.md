# D13.1 Mixed Domain + External Corpus

## 1. Purpose
D13.1 builds a mixed corpus from the approved domain synthetic corpus and the approved `external_general_text` supplement without changing either source corpus in place.

This step exists so later tokenizer retraining and bounded mixed-corpus experiments can consume a single mixed processed corpus while still preserving provenance and the project-backbone constraint.

## 2. Input Corpora
Approved input corpora used in this step:
- `synthetic_expanded` processed docs = 45
- `synthetic_expanded` train docs = 41
- `synthetic_expanded` val docs = 4
- `external_general_text` processed docs = 12
- `external_general_text` train docs = 11
- `external_general_text` val docs = 1
- `external_general_text` approval scope remains limited tokenizer retraining and bounded mixed-corpus experiments only

Input files:
- `data/real_corpus/processed/synthetic_expanded.processed.jsonl`
- `data/real_corpus/processed/external_general_text.processed.jsonl`
- `data/real_corpus/metadata/source_manifest.synthetic_expanded.jsonl`
- `data/real_corpus/metadata/source_manifest.external_general_text.jsonl`

Builder script:
- `scripts/build_mixed_domain_external_corpus.py`

## 3. Mixed Outputs
D13.1 created these new derived outputs:
- `data/real_corpus/processed/mixed_domain_external.processed.jsonl`
- `data/real_corpus/splits/mixed_domain_external.train.jsonl`
- `data/real_corpus/splits/mixed_domain_external.val.jsonl`
- `data/real_corpus/metadata/mixed_domain_external.mix_summary.json`

Observed mixed-corpus totals:
- `total_docs = 57`
- `train_docs = 52`
- `val_docs = 5`
- `total_chars = 181618`
- `seed = 1337`

## 4. Source Counts
Observed source counts:
- total `synthetic_examples` docs = 45
- total `external_general_text` docs = 12
- train `synthetic_examples` docs = 41
- train `external_general_text` docs = 11
- val `synthetic_examples` docs = 4
- val `external_general_text` docs = 1

The mixed corpus therefore includes all approved domain synthetic documents and all approved external supplement documents, with no upsampling and no downsampling.

## 5. Train/Val Split
Split behavior in D13.1:
- original source `split` values were preserved
- source `train` documents remained `train`
- source `val` documents remained `val`
- shuffle used deterministic seed `1337`
- shuffle was applied within split only
- document-level split remained intact

This means D13.1 did not redefine the existing train/val boundary and did not introduce cross-split leakage.

## 6. Provenance Preservation
Provenance preservation checks passed:
- `source_category` was preserved on every mixed record
- `source_id` was preserved on every mixed record
- `candidate_id` was preserved for `external_general_text` records
- each mixed record now also includes:
  - `mixed_corpus_id`
  - `original_processed_id`
  - `metadata.mixed_stage = D13.1`
  - `metadata.project_backbone = CS/ML/Python/Transformer training systems education`
- source processed files were not overwritten
- the mixed outputs were written as new derived JSONL files only

Conclusion:
- mixed corpus created from approved domain synthetic + approved `external_general_text` supplement
- `source_category` preserved
- external text remains supplement only

## 7. Secret Scan Result
Secret review result:
- credential-style scan for `api_key | password | private_key | sk-` found no hits
- content-word scan for `secret | token` found ordinary educational/body-text matches only

Observed text-only explanations:
- `token` matches come from project-authored educational corpus records discussing tokenization, next-token prediction, and split/attention notes
- one ordinary literary `secret` match remains in the approved Alice chapter text

Classification:
- `explanatory/text-only`

No real credential-like secret was found in the mixed outputs.

## 8. Guardrails
D13.1 guardrails preserved:
- `external_general_text` remains supplement only
- the project backbone remains CS / ML / Python / Transformer training systems education
- original `synthetic_expanded` and `external_general_text` processed files were not overwritten
- no intake was re-run
- no new external data was downloaded
- no new external corpus was copied
- provenance remained attached to each mixed record

## 9. What It Does Not Do
D13.1 does not:
- train a tokenizer
- train a model
- run bounded training
- modify model code
- change the approved role of `external_general_text`

## 10. Next Step
Recommended next step:
- D14 mixed/domain BPE tokenizer retraining plan, or
- D14 train a mixed BPE tokenizer using the new mixed processed corpus while keeping tokenizer/model `vocab_size` aligned and preserving backbone-versus-supplement reporting
