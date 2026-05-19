# D18.1 Human Sampling Review Template

Use one row per sampled file.

| sample_id | topic_id | worker_id | file_path | reviewer_decision | issue_type | notes | promote_candidate | rewrite_needed |
|---|---|---|---|---|---|---|---|---|
| B04-TSR-CC1-001 | B04-MLF-0001 | CC-1 | `data/real_corpus/draft_queue/domain_synthetic_batch_04/...` | keep_as_candidate | none | baseline sample reads distinct and clear | no | no |
| B04-TSR-CC2-001 | B04-PDS-0004 | CC-2 | `data/real_corpus/draft_queue/domain_synthetic_batch_04/...` | needs_rewrite | templated_opening_family | opening and review scaffold feel too repetitive across neighboring drafts | no | yes |

Suggested `reviewer_decision` values:
- `keep_as_candidate`
- `needs_rewrite`
- `reject`
- `strong_candidate_for_promotion`

Suggested `issue_type` values:
- `none`
- `boilerplate_density_high`
- `templated_opening_family`
- `repeated_internal_line`
- `metadata_mismatch`
- `topic_drift`
- `practical_usefulness_low`
- `misleading_claim_risk`
- `external_copy_risk`
- `other`
