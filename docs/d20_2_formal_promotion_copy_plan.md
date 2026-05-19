# D20.2 Formal Promotion Copy Plan

## 1. Purpose
The purpose of D20.2 is to define how a future formal promotion-copy step could move reviewed batch_05 candidates into the formal synthetic educational corpus.

This document is planning only.
D20.2 can copy selected candidates into formal `synthetic_expanded` only after explicit user approval.

## 2. Promotion Gate
D20.2 may proceed only if the user explicitly approves a formal promotion-copy step.
Without that approval:
- no file copy happens
- no formal manifest changes happen
- no intake happens
- no tokenizer or model training happens

## 3. Candidate Scope
Recommended maximum first promotion scope:
- exactly the `92` selected candidates already listed in `batch_05_promotion_subset_candidates.jsonl`
- not the full `600`-file batch_05 draft set

Reasoning:
- the `92` candidates are the only records already reviewed and selected by D20.1
- broadening beyond the reviewed candidate ledger would exceed the evidence boundary established by D19.3 and D20.1

## 4. Target Formal Raw Directory Proposal
If D20.2 is approved, the proposed destination should be a new formal raw directory under the synthetic educational corpus tree, for example:
- `data/real_corpus/raw/synthetic_expanded/batch_05_promotion_subset/`

Recommended organization shape:
- preserve worker/category subdirectories where practical
- avoid flattening source paths if that would obscure provenance
- keep destination naming tied to `batch_05` and the promotion-subset scope

## 5. Source Provenance Preservation
Any future D20.2 copy step should preserve provenance explicitly:
- retain original `topic_id`
- retain original `worker_id`
- retain original source `file_path` in the promotion manifest
- retain `source_batch_id = domain_synthetic_batch_05`
- record original draft-queue path alongside any new formal raw path
- preserve source-category identity as `synthetic_examples`

Recommended provenance ledger fields for a future D20.2 manifest:
- `topic_id`
- `worker_id`
- `source_batch_id`
- `source_draft_path`
- `formal_raw_path`
- `promoted_from_candidate_manifest`
- `promotion_commit`

## 6. Manifest Update Requirements
If D20.2 is approved, update requirements should include:
- create a formal promotion manifest for copied files
- record one row per copied candidate
- preserve candidate IDs or map them deterministically into promotion IDs
- keep the D20.1 candidate manifest unchanged as the source ledger
- ensure copied files can be traced back to their D19.3 review decision and D20.1 candidate record

## 7. Approval Fields
Important approval rule:
- D20.2 should not modify the original batch_05 draft files in place

Recommended approval handling:
- original draft files remain `approved_for_training: false`
- if formal copies are created, approval-state changes should happen only in the formal-copy path and its associated formal manifest records
- any formal approval field should be written only after the copy step and after post-copy validation passes

## 8. Post-Copy Validation
After any future D20.2 copy operation, run post-copy validation before intake:
- copied file count matches the approved candidate count
- all copied files still have readable metadata
- source and copied topic IDs match
- source and copied worker IDs match
- source provenance fields are preserved
- copied files remain inside the approved formal raw target directory
- no unexpected file-type drift or missing files occurred

## 9. Intake and Training Hold
Even after formal copy, D20.2 still should not immediately run downstream stages.
No intake or training should happen until after formal promotion is committed and validated.

Explicit holds after copy planning:
- no intake until the formal copy step is complete and validated
- no tokenizer training until after formal promotion is committed
- no model training until after formal promotion is committed

## 10. Recommended Next Step After D20.2 Planning
If the user later approves D20.2 execution:
1. copy only the approved candidate ledger
2. create a formal promotion manifest with provenance
3. run post-copy validation
4. commit the formal-copy step locally
5. discuss intake only after the formal promotion commit exists

D20.2 conclusion:
- D20.2 can copy selected candidates into formal `synthetic_expanded` only after user approval
- provenance and approval boundaries must remain explicit
- no intake or training should happen until after formal promotion is committed
- the recommended maximum first promotion remains exactly the `92` D20.1-selected candidates
