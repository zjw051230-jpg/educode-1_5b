# D19.2 Batch 05 Worker Aggregation Summary

## 1. Purpose
This note summarizes batch_05 quality-review outcomes by worker so the next human-review step can target the highest-value clusters first.

Authoritative sources:
- `data/real_corpus/draft_queue/domain_synthetic_batch_05/batch_05_validation_summary.json`
- `data/real_corpus/draft_queue/domain_synthetic_batch_05/batch_05_quality_review_summary.json`
- `data/real_corpus/draft_queue/domain_synthetic_batch_05/batch_05_quality_review_manifest.jsonl`

## 2. Worker-Level Outcome Table

| worker | pass | needs_edit | reject | main note pattern |
|---|---:|---:|---:|---|
| `CC-1` | 100 | 0 | 0 | no automated note concentration |
| `CC-2` | 40 | 60 | 0 | repeated internal verification-prompt residue |
| `CC-3` | 100 | 0 | 0 | no automated note concentration |
| `CC-4` | 100 | 0 | 0 | no automated note concentration |
| `CC-5` | 66 | 34 | 0 | weaker explicit bilingual pairing signal in part of the markdown slice |
| `CC-6` | 29 | 71 | 0 | repeated `trace_note_*` residue plus thin markdown structure |

## 3. Worker Notes

### CC-1
Observed result:
- `100` pass
- `0` needs_edit
- `0` reject

Interpretation:
- the repair-aware constraints appear to have held across the sampled themes here
- CC-1 is the cleanest baseline worker for later human comparison

### CC-2
Observed result:
- `40` pass
- `60` needs_edit
- `0` reject

Observed automated flag concentration:
- `repeated_internal_line`: `60`

Representative flagged files:
- `B05-PDS-0001` — `jsonl_repair/b05_pds_0001_broken_jsonl_first_bad_line.md`
- `B05-PDS-0003` — `jsonl_repair/b05_pds_0003_embedded_tab_normalization.md`
- `B05-PDS-0005` — `jsonl_repair/b05_pds_0005_multi_line_field_rejection.md`

Interpretation:
- the remaining issue is not metadata or scope failure
- the remaining issue is repeated instructional prompt residue that still makes many markdown files feel partially templated

### CC-3
Observed result:
- `100` pass
- `0` needs_edit
- `0` reject

Interpretation:
- CC-3 looks materially cleaner than the batch_04 transformer-architecture cluster
- this worker should serve as a second clean baseline for human review

### CC-4
Observed result:
- `100` pass
- `0` needs_edit
- `0` reject

Interpretation:
- CC-4 runtime-system drafts appear structurally and stylistically stable under the current automated review
- this worker is another clean baseline for comparison against the noisier worker clusters

### CC-5
Observed result:
- `66` pass
- `34` needs_edit
- `0` reject

Observed automated flag concentration:
- `bilingual_pairing_missing`: `31`
- `thin_section_structure`: `11`

Representative flagged files:
- `B05-BIL-0035` — `bpe_zh_en/b05_bil_0035_bpe_merge_priority_collision.md`
- `B05-BIL-0036` — `bpe_zh_en/b05_bil_0036_bpe_rare_term_budget.md`
- `B05-BIL-0037` — `bpe_zh_en/b05_bil_0037_bpe_english_acronym_preservation.md`

Interpretation:
- CC-5 improved over batch_04 by avoiding a universal bilingual template collapse
- the remaining review task is to decide whether the thinner BPE markdown slice is still educationally strong enough or should be rewritten into more explicit bilingual pairings

### CC-6
Observed result:
- `29` pass
- `71` needs_edit
- `0` reject

Observed automated flag concentration:
- `trace_note_residue`: `41`
- `thin_section_structure`: `30`

Representative flagged files:
- `B05-COD-0027` — `checkpoint_metadata/b05-cod-0027_checkpoint_metadata_007.py`
- `B05-COD-0001` — `source_category_tools/b05-cod-0001_source_category_tools_001.md`
- `B05-COD-0002` — `source_category_tools/b05-cod-0002_source_category_tools_002.md`

Interpretation:
- CC-6 code files are more genuinely topic-grounded than the batch_04 generic wrapper pattern
- the dominant remaining issue is visible drafting residue in Python plus a markdown family that still feels too thin

## 4. Priority Ranking for Human Review
Recommended worker review order:
1. `CC-6`
2. `CC-2`
3. `CC-5`
4. `CC-1`
5. `CC-3`
6. `CC-4`

Reasoning:
- `CC-6` has the largest note concentration and spans both markdown and Python residue
- `CC-2` has a broad markdown repetition cluster that is likely real and easy for human reviewers to confirm
- `CC-5` has a smaller but still meaningful bilingual-quality ambiguity cluster that needs human judgment
- `CC-1`, `CC-3`, and `CC-4` are useful cleaner baselines rather than primary risk pools

## 5. Decision Summary
Worker-level interpretation summary:
- `CC-1`, `CC-3`, and `CC-4` look ready to serve as low-risk baselines in later review work
- `CC-2`, `CC-5`, and `CC-6` still need targeted human inspection before any discussion of promotion readiness
- no worker has reject-level automated failure, but no note-heavy worker should be treated as automatically promotion-ready
