# D19.3 Batch 05 Sampling Review Plan

## 1. Purpose
The purpose of D19.3 is to define a bounded human review plan for batch_05 after D19.2 structural validation and automated quality review.

This step is planning only.
It does not promote any file, does not run intake, does not train tokenizer or model artifacts, and does not move draft files into the formal corpus.

## 2. Why D19.3 Is Needed
D19.2 already established that batch_05 is structurally valid.
The remaining uncertainty is no longer file hygiene.
The remaining uncertainty is concentrated drafting quality residue inside a smaller subset of workers and file families.

Authoritative D19.2 result:
- structural validation: `passed_with_notes`
- automated quality review: `passed_with_notes`
- `435` files quality-pass under automation
- `165` files marked `needs_edit`
- `0` files marked `reject`

Interpretation:
- batch_05 is much healthier than batch_04
- batch_05 is still not clean enough for forced promotion discussion
- a bounded human-review pass should confirm whether the automated note clusters are real rewrite priorities or acceptable concise styles

## 3. Main Residual Risks Carried into Human Review
The main D19.2 automated note families are:
- `repeated_internal_line`: `60`
- `trace_note_residue`: `41`
- `thin_section_structure`: `41`
- `bilingual_pairing_missing`: `31`

These notes are concentrated in three worker clusters:
- `CC-2`: repeated internal prompt residue
- `CC-5`: weaker explicit bilingual pairing signal in part of the markdown slice
- `CC-6`: repeated trace-note residue plus thin markdown structure

## 4. Recommended Review Pack Shape
Recommended D19.3 pack size:
- `180` files total

Recommended composition:
- review **all `165` automated `needs_edit` files** from D19.2
- add `15` clean baseline files from the no-note workers:
  - `CC-1`: `5`
  - `CC-3`: `5`
  - `CC-4`: `5`

Why this shape is preferred:
- batch_05 is only `600` files, so reviewing all `needs_edit` files is feasible
- this avoids hiding behind random sampling when the automated note set is already bounded
- the `15` baseline files provide a control slice so reviewers can compare note-heavy clusters against cleaner workers

## 5. Worker Priority
Recommended review order:
1. `CC-6`
2. `CC-2`
3. `CC-5`
4. `CC-1`
5. `CC-3`
6. `CC-4`

Reasoning:
- `CC-6` has the highest note concentration (`71` files) and mixes Python residue with markdown thinness
- `CC-2` has a large repeated-line markdown cluster (`60` files) that should be easy to validate manually
- `CC-5` has a smaller but more judgment-heavy bilingual markdown cluster (`34` files)
- `CC-1`, `CC-3`, and `CC-4` function mainly as baselines

## 6. File Selection Method
For the `165` automated `needs_edit` files:
- include every flagged file exactly once
- preserve the worker order above during review assignment
- keep file paths grouped by worker and subcategory

For the `15` baseline files:
- select a mix of markdown and Python where available
- include at least one file from multiple subcategories within each baseline worker
- include both shorter and longer files so reviewers see more than one drafting shape

## 7. Human Review Rubric
For each reviewed file, score:
- topic alignment
- educational usefulness
- originality versus hidden scaffold reuse
- practical usefulness of the example or artifact
- whether the automated note looks real, overstated, or harmless
- whether the file could remain a candidate without immediate rewrite

Suggested decision labels:
- `keep_as_candidate`
- `needs_rewrite`
- `reject`
- `strong_candidate_for_promotion`

Important D19.3 caveat:
- even if a file receives `strong_candidate_for_promotion`, D19.3 still does **not** promote it
- the label only marks it as a future discussion candidate after review aggregation

## 8. Worker-Specific Review Questions
### CC-2
- Are the repeated verification-prompt lines merely cosmetic, or do they materially reduce educational distinctness?
- Do the files still teach genuinely different repair or validation decisions once the repeated lines are ignored?

### CC-5
- Are the flagged markdown files truly missing bilingual pairing, or are they concise mixed-script notes that remain educationally clear?
- Does the thinner mini-lab structure still carry enough bilingual teaching value?

### CC-6
- Do the repeated `trace_note_*` lines make the Python files feel unfinished?
- Are the thinner markdown files still useful code-adjacent teaching artifacts, or should they be expanded before any later promotion review?

## 9. Expected Outcome of D19.3
D19.3 should answer three concrete questions:
1. which automated note clusters correspond to genuine rewrite needs
2. whether batch_05 contains a meaningful clean subset worth preserving as draft candidates
3. whether the next step should be targeted repair inside `CC-2` / `CC-5` / `CC-6` rather than broader regeneration

## 10. What D19.3 Does Not Do
D19.3 does not:
- promote any file into the formal corpus
- copy files into `raw/synthetic_expanded`
- run intake
- train a tokenizer
- train a model
- modify batch_04
- download external data
- push to a remote repository

## 11. Recommended Next Step After D19.3
After the human review pack is completed:
- aggregate the D19.3 reviewer judgments
- keep batch_05 draft-only unless the human review materially contradicts the automated note concentrations
- if the human review confirms the automated notes, prioritize targeted repair for `CC-2`, `CC-5`, and `CC-6` instead of broad promotion discussion
