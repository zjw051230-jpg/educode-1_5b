# D20 Promotion Subset Plan

## 1. Purpose
The purpose of D20 is to define a conservative planning shape for any future batch_05 promotion-candidate subset after D19.3 sampled review.

This step is planning only.
It does not promote files, does not copy files into the formal corpus, does not run intake, does not train tokenizer artifacts or models, and does not change any batch_05 file away from `approved_for_training: false`.

## 2. Authoritative Input State
Authoritative inputs for this plan:
- `docs/d19_2_batch_05_repair_aware_validation_review.md`
- `docs/d19_3_batch_05_targeted_sampling_review.md`
- `data/real_corpus/draft_queue/domain_synthetic_batch_05/batch_05_targeted_sample_review_manifest.jsonl`
- `data/real_corpus/draft_queue/domain_synthetic_batch_05/batch_05_targeted_sample_review_summary.json`

Authoritative sampled review result carried into D20:
- reviewed sampled files: `120`
- `strong_candidate_for_promotion`: `92`
- `keep_as_candidate`: `17`
- `needs_rewrite`: `11`
- `reject`: `0`
- readiness label: `may_support_small_promotion_subset`

Important interpretation:
- this evidence applies only to the `120` reviewed sampled files
- it does **not** justify worker-wide or batch-wide promotion of unseen files
- any future subset must be built only from files already reviewed in D19.3

## 3. Planning Principles
D20 should follow these rules:
- use only D19.3-reviewed files as candidate inputs
- prefer the cleanest sampled worker slices first
- do not convert `keep_as_candidate` into promotion candidates by optimism alone
- do not include `needs_rewrite` or `reject` files in any candidate subset
- keep all batch_05 files draft-only until a later execution step explicitly approves otherwise

Conservative interpretation rule:
- D19.3 is strong enough to support a bounded subset discussion
- D19.3 is not strong enough to support broad worker-level extrapolation from a partial sample

## 4. Recommended Candidate Tiers
### Tier 1: clean reviewed baseline subset
Recommended Tier 1 pool:
- the `60` sampled files rated `strong_candidate_for_promotion` from `CC-1`, `CC-3`, and `CC-4`

Why Tier 1 comes first:
- these workers produced `20 / 20` strong sampled outcomes each
- they produced `0` sampled rewrites and `0` sampled rejects
- this is the cleanest evidence-backed subset in the entire D19.3 review

Recommended D20 stance:
- if a future step needs a first bounded promotion-candidate pool, start here
- do not automatically expand beyond these `60` reviewed files in the first pass

### Tier 2: conditional reviewed strong candidates from note-heavy workers
Conditional Tier 2 pool:
- `CC-2`: `11` strong candidates
- `CC-5`: `11` strong candidates
- `CC-6`: `10` strong candidates
- conditional Tier 2 total: `32`

Why Tier 2 is conditional rather than immediate:
- `CC-2` still produced `9` sampled rewrites from repeated-scaffold residue
- `CC-5` still produced `9` keep-as-candidate results rather than an all-strong slice
- `CC-6` still produced `2` sampled rewrites and `8` keeps

Recommended D20 stance:
- hold these `32` strong files behind a narrower second-pass decision
- treat them as promising but not yet first-pass subset material

### Tier 3: hold queue
Hold queue:
- the `17` sampled files rated `keep_as_candidate`

Recommended D20 stance:
- preserve them as draft candidates only
- do not include them in a first promotion-candidate subset
- use them later only if a future spot-check explicitly upgrades them

### Tier 4: explicit exclusion set
Exclude from any future subset discussion:
- the `11` sampled files rated `needs_rewrite`
- any future `reject` files if later review expands

Recommended D20 stance:
- these files remain repair targets, not subset candidates

## 5. Recommended D20 Execution Shape
If a later D20 execution step is approved, use this order:
1. filter the D19.3 review manifest to `promotion_decision == strong_candidate_for_promotion`
2. keep only already reviewed files; do not add unseen neighbors from the same worker or topic family
3. freeze the `60` reviewed strong files from `CC-1`, `CC-3`, and `CC-4` as the first candidate ledger
4. separately ledger the `32` reviewed strong files from `CC-2`, `CC-5`, and `CC-6` as conditional candidates
5. keep the `17` keep-as-candidate files in a non-promotion hold queue
6. exclude all `11` rewrite files from subset discussion

## 6. Suggested Review Checks Before Any Future Promotion Action
Before any later file-level promotion step, verify for each candidate file:
- it appears in the D19.3 sampled review manifest
- `promotion_decision == strong_candidate_for_promotion`
- `metadata_ok == true`
- it is still present at the same path
- its draft metadata still matches the sampled review record
- no later manual note downgrades it

Additional caution for conditional Tier 2 files:
- `CC-2`: re-check for hidden repeated scaffold language
- `CC-5`: re-check whether bilingual teaching signal is explicit enough without relying on inference
- `CC-6`: re-check for residual `trace_note_*` or thin-structure signs that were not strong enough to trigger rewrite in the sampled script

## 7. Recommended First Pass Size
Recommended first-pass subset size:
- `<= 60` files

Why this cap is appropriate:
- it stays inside the cleanest fully reviewed baseline slice
- it avoids pretending that D19.3 reviewed the entire `600`-file batch
- it preserves a narrow blast radius if a later file-level verification still finds edge cases

If an even smaller pilot is preferred, the most conservative fallback is:
- start with a `20` to `40` file subset drawn only from the reviewed strong files in `CC-1` and `CC-3`

## 8. What D20 Does Not Do
D20 does not:
- promote files during this planning step
- copy files into formal `raw/synthetic_expanded`
- run intake
- train a tokenizer
- train a model
- modify model code
- download external data
- push to a remote repository

Explicit hold state:
- all batch_05 draft files remain `approved_for_training: false`

## 9. Recommended Next Step
Recommended next step after this plan:
- if a future promotion-candidate step is approved, start with Tier 1 only
- keep Tier 2 as a conditional queue until a narrower second-pass review explicitly clears those files
- keep Tier 3 in the draft queue
- send Tier 4 files back to targeted repair rather than subset discussion

D20 conclusion:
- D19.3 supports a small promotion-candidate discussion
- the clean evidence-backed core is the `60` reviewed strong files from `CC-1`, `CC-3`, and `CC-4`
- everything else should remain conditional, held, or excluded until a later explicit decision step
