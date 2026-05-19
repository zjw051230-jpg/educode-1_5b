# D19.3 Batch 05 Targeted Sampling Review

## 1. Purpose
The purpose of D19.3 is to create and review a bounded targeted sampling pack for:
- `data/real_corpus/draft_queue/domain_synthetic_batch_05/`

This step remains draft-queue review work only.
It does not promote any file into the formal corpus, does not copy files into formal `raw/synthetic_expanded`, does not run intake, does not train tokenizer artifacts or models, and does not push to a remote.

## 2. Inputs and Outputs
Authoritative D19.3 inputs:
- `data/real_corpus/draft_queue/domain_synthetic_batch_05/batch_05_validation_manifest.jsonl`
- `data/real_corpus/draft_queue/domain_synthetic_batch_05/batch_05_quality_review_manifest.jsonl`
- `data/real_corpus/draft_queue/domain_synthetic_batch_05/batch_05_quality_review_summary.json`
- `docs/d19_2_batch_05_repair_aware_validation_review.md`
- `docs/d19_3_batch_05_sampling_review_plan.md`

Automation created or finalized for D19.3:
- `scripts/create_batch_05_targeted_sampling_pack.py`
- `scripts/review_batch_05_targeted_samples.py`
- `tests/test_create_batch_05_targeted_sampling_pack.py`
- `tests/test_review_batch_05_targeted_samples.py`

D19.3 outputs created:
- `data/real_corpus/draft_queue/domain_synthetic_batch_05/batch_05_targeted_sampling_manifest.jsonl`
- `data/real_corpus/draft_queue/domain_synthetic_batch_05/batch_05_targeted_sampling_summary.json`
- `data/real_corpus/draft_queue/domain_synthetic_batch_05/batch_05_targeted_sample_review_manifest.jsonl`
- `data/real_corpus/draft_queue/domain_synthetic_batch_05/batch_05_targeted_sample_review_summary.json`

## 3. Sampling Pack Shape
Observed sampling pack shape:
- `120` sampled files total
- `20` sampled files per worker across `6` workers
- per worker target:
  - `10` quality-pass representative files
  - `5` needs-edit risk cases
  - `5` boundary or representative files

Important pack-construction behavior:
- sampling joins the D19.2 quality manifest back to the validation manifest so `writing_form` and `concrete_anchor` remain available during sampled review
- selection balances markdown and Python coverage, varied `writing_form`, varied `concrete_anchor`, and worker-specific residual clusters
- representative residual-cluster topics are forced into the pack so the sampled review definitely covers known D19.2 problem examples:
  - `B05-PDS-0001`
  - `B05-BIL-0035`
  - `B05-COD-0027`

## 4. Sampling Coverage Result
Observed D19.3 sampling totals:
- sampled files: `120`
- worker distribution: `20` files for each of `CC-1` through `CC-6`
- quality-state mix: `95` `quality_pass` and `25` `needs_edit`
- file-type mix: `71` markdown and `49` Python

Observed sampled residual-risk counts:
- `repeated_internal_line`: `9`
- `bilingual_pairing_missing`: `6`
- `thin_section_structure`: `13`
- `trace_note_residue`: `2`

Observed worker-level sampled note pressure:
- `CC-1`: `20` sampled / `20` quality-pass / `0` needs-edit
- `CC-2`: `20` sampled / `11` quality-pass / `9` needs-edit
- `CC-3`: `20` sampled / `20` quality-pass / `0` needs-edit
- `CC-4`: `20` sampled / `20` quality-pass / `0` needs-edit
- `CC-5`: `20` sampled / `14` quality-pass / `6` needs-edit
- `CC-6`: `20` sampled / `10` quality-pass / `10` needs-edit

Interpretation:
- D19.3 preserved a clean baseline slice from `CC-1`, `CC-3`, and `CC-4`
- D19.3 also preserved direct visibility into the known D19.2 residual clusters instead of letting them disappear inside random sampling

## 5. Sampled Review Result
Observed sampled review totals:
- total reviewed samples: `120`
- `strong_candidate_for_promotion`: `92`
- `keep_as_candidate`: `17`
- `needs_rewrite`: `11`
- `reject`: `0`
- sampled promotion readiness: `may_support_small_promotion_subset`

Observed worker-level sampled review decisions:
- `CC-1`: `20` strong / `0` keep / `0` rewrite / `0` reject
- `CC-2`: `11` strong / `0` keep / `9` rewrite / `0` reject
- `CC-3`: `20` strong / `0` keep / `0` rewrite / `0` reject
- `CC-4`: `20` strong / `0` keep / `0` rewrite / `0` reject
- `CC-5`: `11` strong / `9` keep / `0` rewrite / `0` reject
- `CC-6`: `10` strong / `8` keep / `2` rewrite / `0` reject

Validation checks completed for this step:
- `tests/test_create_batch_05_targeted_sampling_pack.py` passed
- `tests/test_review_batch_05_targeted_samples.py` passed
- both generated JSONL manifests were parsed successfully at `120` rows each

## 6. Main Findings
### Clean baseline workers are genuinely strong in the sampled slice
`CC-1`, `CC-3`, and `CC-4` each produced `20 / 20` strong sampled review outcomes.
This is the clearest evidence that batch_05 is materially healthier than batch_04 and that the repair-aware generation pass produced a usable clean baseline.

### CC-2 still contains a real repeated-scaffold rewrite cluster
`CC-2` produced `9` sampled rewrites and `11` sampled strong candidates.
The rewrite examples remain concentrated in the repeated-internal-line family, including the pinned representative file `B05-PDS-0001`.
This means the D19.2 residual note cluster was real rather than merely over-sensitive automation.

### CC-5 looks mixed but not broken
`CC-5` produced `11` strong candidates and `9` keep-as-candidate files, with `0` sampled rewrites.
The bilingual/thin-structure concern remains worth watching, but the sampled review result suggests a meaningful portion of `CC-5` is preservable as draft candidates rather than a blanket rewrite target.

### CC-6 improved sharply but still retains a small rewrite tail
`CC-6` produced `10` strong candidates, `8` keepers, and `2` rewrites.
The pinned representative file `B05-COD-0027` remained a rewrite case because the trace-note residue still pushed template-repetition risk to `high`.
This means the worker improved substantially versus batch_04, but D19.3 still confirms a real cleanup tail rather than a fully clean worker slice.

## 7. D19.3 Decision
D19.3 decision:
- batch_05 remains a draft-queue asset only
- D19.3 does **not** promote any file into the formal corpus
- all batch_05 draft files remain `approved_for_training: false`
- D19.3 does support planning a **small and conservative future promotion-candidate subset**, but only from files already reviewed in the sampled pack

Decision rationale:
- sampled review found `92` strong candidates and `0` rejects, which is materially stronger than the batch_04 result
- sampled review also found `11` rewrites concentrated in the same residual worker clusters already identified in D19.2
- because D19.3 reviews only `120 / 600` files, it supports a bounded subset discussion, not worker-wide promotion or batch-wide promotion

## 8. What D19.3 Does Not Do
D19.3 does not:
- perform formal corpus promotion
- copy any draft into formal `raw/synthetic_expanded`
- change any batch_05 draft away from `approved_for_training: false`
- run intake
- train a tokenizer
- train a model
- modify model code
- download external data
- push to a remote repository

## 9. Recommended Next Step
Recommended next step:
- prepare a D20 promotion-subset plan that is limited to already reviewed strong candidates
- keep the first conservative candidate tier focused on the clean sampled baseline from `CC-1`, `CC-3`, and `CC-4`
- hold `CC-2`, `CC-5`, and `CC-6` strong/keep files behind a narrower second-pass decision instead of broad promotion

D19.3 conclusion:
- batch_05 is much stronger than batch_04 in the reviewed slice
- the clean baseline slice is real
- the residual rewrite pressure is still concentrated rather than eliminated
- the correct next move is conservative subset planning, not immediate promotion
