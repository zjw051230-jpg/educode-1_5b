# D19.2 Batch 05 Repair-Aware Validation and Quality Review

## 1. Purpose
The purpose of D19.2 is to validate and quality-review the repair-aware draft batch under:
- `data/real_corpus/draft_queue/domain_synthetic_batch_05/`

This step is a draft-queue validation and review step only.
It does not promote any file into the formal corpus, does not enter formal `raw/synthetic_expanded`, does not run intake, does not train tokenizer artifacts or models, does not modify batch_04, and does not push to a remote.

## 2. Inputs and Outputs
D19.2 input scope:
- `data/real_corpus/draft_queue/domain_synthetic_batch_05/`
- six worker directories
- worker manifests plus support files (`batch_summary.md`, `anti_template_self_check.md`, `progress_0025.md`, `progress_0050.md`, `progress_0075.md`, `progress_0100.md`)

Validation outputs created:
- `data/real_corpus/draft_queue/domain_synthetic_batch_05/batch_05_validation_summary.json`
- `data/real_corpus/draft_queue/domain_synthetic_batch_05/batch_05_validation_manifest.jsonl`

Quality-review outputs created:
- `data/real_corpus/draft_queue/domain_synthetic_batch_05/batch_05_quality_review_summary.json`
- `data/real_corpus/draft_queue/domain_synthetic_batch_05/batch_05_quality_review_manifest.jsonl`

Automation created for this step:
- `scripts/validate_draft_corpus_batch_05.py`
- `scripts/review_draft_corpus_quality_batch_05.py`
- `tests/test_validate_draft_corpus_batch_05.py`
- `tests/test_review_draft_corpus_quality_batch_05.py`

## 3. Structural Validation Result
Observed structural counts:
- total topic files: `600`
- markdown files: `365`
- python files: `235`
- worker manifests: `6`
- worker summaries: `6`
- anti-template self-check files: `6`
- progress checkpoint files: `24`

Observed validation hygiene:
- validation status: `passed_with_notes`
- missing files: `0`
- metadata errors: `0`
- scope errors: `0`
- duplicate topic ids: `0`
- duplicate file paths: `0`
- credential-style secret hits: `0`

Important interpretation:
- the batch passes structural scope, metadata, and path-hygiene checks
- `passed_with_notes` comes from explanatory secret-pattern mentions in support text, not from leaked credentials
- all batch_05 draft files remain review-only and continue to carry `approved_for_training: false`

## 4. Automated Quality Review Result
Observed quality-review totals:
- total reviewed records: `600`
- `quality_pass`: `435`
- `needs_edit`: `165`
- `reject`: `0`
- quality gate status: `passed_with_notes`

Observed global automated note counts:
- `repeated_internal_line`: `60`
- `trace_note_residue`: `41`
- `thin_section_structure`: `41`
- `bilingual_pairing_missing`: `31`

Observed worker-level quality state counts:
- `CC-1`: `100` pass / `0` needs_edit / `0` reject
- `CC-2`: `40` pass / `60` needs_edit / `0` reject
- `CC-3`: `100` pass / `0` needs_edit / `0` reject
- `CC-4`: `100` pass / `0` needs_edit / `0` reject
- `CC-5`: `66` pass / `34` needs_edit / `0` reject
- `CC-6`: `29` pass / `71` needs_edit / `0` reject

## 5. Main Residual Quality Clusters
The automated review does not show a batch-wide collapse like batch_04, but it does show three concentrated residual clusters.

### CC-2: repeated internal prompt residue
Main pattern:
- `60` files flagged with `repeated_internal_line`

Representative examples:
- `B05-PDS-0001` — `.../cc2_python_data_systems/jsonl_repair/b05_pds_0001_broken_jsonl_first_bad_line.md`
- `B05-PDS-0003` — `.../cc2_python_data_systems/jsonl_repair/b05_pds_0003_embedded_tab_normalization.md`
- `B05-PDS-0005` — `.../cc2_python_data_systems/jsonl_repair/b05_pds_0005_multi_line_field_rejection.md`

Interpretation:
- these files are topic-grounded and structurally valid
- the main residue is repeated verification-prompt language that still reads like reusable scaffold text rather than uniquely authored explanation

### CC-5: thinner bilingual signal in part of the markdown slice
Main pattern:
- `31` automated hits for `bilingual_pairing_missing`
- `11` automated hits for `thin_section_structure`

Representative examples:
- `B05-BIL-0035` — `.../cc5_bilingual_qa/bpe_zh_en/b05_bil_0035_bpe_merge_priority_collision.md`
- `B05-BIL-0036` — `.../cc5_bilingual_qa/bpe_zh_en/b05_bil_0036_bpe_rare_term_budget.md`
- `B05-BIL-0037` — `.../cc5_bilingual_qa/bpe_zh_en/b05_bil_0037_bpe_english_acronym_preservation.md`

Interpretation:
- this is an automated note cluster, not an automatic rejection result
- several files still look useful, but the bilingual pairing signal is sometimes implicit rather than explicit, and some mini-lab markdown entries are thinner than the stronger mixed-script analysis files

### CC-6: trace-note residue plus thin markdown structure
Main pattern:
- `41` automated hits for `trace_note_residue`
- `30` automated hits for `thin_section_structure`

Representative examples:
- `B05-COD-0027` — `.../cc6_code_snippets/checkpoint_metadata/b05-cod-0027_checkpoint_metadata_007.py`
- `B05-COD-0001` — `.../cc6_code_snippets/source_category_tools/b05-cod-0001_source_category_tools_001.md`
- `B05-COD-0002` — `.../cc6_code_snippets/source_category_tools/b05-cod-0002_source_category_tools_002.md`

Interpretation:
- many CC-6 Python files are meaningfully more topic-grounded than the batch_04 generic numeric-summary pattern
- the remaining problem is not missing grounding but visible drafting residue (`trace_note_*`) and a markdown slice that is still thinner than the stronger workers

## 6. Overall Interpretation
D19.2 shows a meaningful improvement over batch_04:
- structural validation is clean
- automated quality review finds `0` rejects
- `435 / 600` files pass the automated quality screen without notes
- quality issues are concentrated in specific worker/style clusters rather than spread uniformly across the batch

But D19.2 does **not** support promotion:
- the authoritative quality result is still `passed_with_notes`, not `passed`
- `165` files still need edit attention under automated review
- the remaining problems are exactly the kind of template/scaffold residue that D19 was supposed to reduce
- the correct next step is targeted human sampling, not forced promotion

Current decision:
- batch_05 remains a draft-queue asset only
- batch_05 should not be promoted into the formal corpus in D19.2
- no intake, tokenizer training, or model training should follow directly from this step

## 7. What D19.2 Does Not Do
D19.2 does not:
- promote any batch_05 draft into the formal corpus
- copy files into formal `raw/synthetic_expanded`
- run intake
- train a tokenizer
- train a model
- modify batch_04
- download external data
- push to a remote repository

## 8. Next Step
Recommended next step:
- use the D19.2 automated note concentrations to build a targeted D19.3 human sampling review pack

Priority order for manual follow-up:
1. `CC-6`
2. `CC-2`
3. `CC-5`
4. `CC-1` / `CC-3` / `CC-4` as cleaner baselines

D19.2 conclusion:
- batch_05 is structurally valid
- batch_05 shows real repair-aware improvement over batch_04
- batch_05 still contains concentrated template residue and should remain draft-only pending targeted human review
