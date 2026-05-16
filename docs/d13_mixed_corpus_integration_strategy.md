# D13 Mixed Corpus Integration Strategy

## 1. Purpose
Plan how to integrate the domain synthetic corpus and the `external_general_text` supplement into a mixed corpus for later tokenizer retraining and bounded mixed-corpus experiments.

## 2. Current Inputs
Current approved inputs:
- `synthetic_expanded` processed docs = 45
- `synthetic_expanded` train docs = 41
- `synthetic_expanded` val docs = 4
- `external_general_text` processed docs = 12
- `external_general_text` train docs = 11
- `external_general_text` val docs = 1
- `external_general_text` approved scope = limited tokenizer retraining and bounded mixed-corpus experiments

## 3. Project Backbone Constraint
EduCode-1.5B remains a CS / ML / Python / Transformer training-systems educational domain model pipeline.

This constraint means:
- `external_general_text` is supplement only
- `source_category` must be preserved
- external text must not redefine the project identity
- later reports must continue to distinguish the educational-domain backbone from the external supplement

## 4. Mixed Corpus Policy
The mixed-corpus strategy should follow these rules:
- keep `synthetic_domain` and `external_general_text` as separate `source_category` values
- preserve `source_id` and `candidate_id`
- do not overwrite original processed files
- create new mixed processed and split outputs only in later D13.1
- keep document-level split assignment
- avoid train/val leakage across source documents
- preserve provenance metadata on every mixed record

## 5. Proposed Mixed Corpus Outputs
D13.1 may create these new outputs:
- `data/real_corpus/processed/mixed_domain_external.processed.jsonl`
- `data/real_corpus/splits/mixed_domain_external.train.jsonl`
- `data/real_corpus/splits/mixed_domain_external.val.jsonl`
- `data/real_corpus/metadata/mixed_domain_external.mix_summary.json`

## 6. Mixing Ratio
Recommended first version:
- include all domain synthetic docs
- include all approved `external_general_text` docs
- report source counts separately
- do not upsample or downsample yet
- later versions may weight the domain corpus higher if external text starts to dominate

## 7. Success Criteria for D13.1
- mixed processed JSONL is valid
- train/val split is valid
- `source_category` is preserved
- source counts are recorded
- no secret hits are present
- no raw Gutenberg header/footer leakage appears if it was already removed in processed text
- no training is run yet

## 8. Tokenizer Implication
Later D14 should:
- retrain a mixed or mixed/domain BPE tokenizer
- compare resulting vocab size against the D9 domain BPE vocab size `3988`
- expect better general English coverage than the domain-only tokenizer path
- keep tokenizer and model `vocab_size` aligned

## 9. What D13 Does Not Do
- does not merge data
- does not train a tokenizer
- does not train a model
- does not enter the A100 path

## 10. Next Step
D13.1: implement a mixed corpus builder and generate mixed processed, train, and val JSONL outputs.
