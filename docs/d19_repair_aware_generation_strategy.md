# D19 Repair-Aware Generation Strategy

## 1. Why Repair-Aware Generation Is Needed
Repair-aware generation is needed because D18.2 plus D18.3 showed that batch_04 is not blocked by metadata, safety, or scope hygiene.
The main blocker is quality collapse caused by repeated scaffolding, shallow specificity, and weak distinction across many neighboring files.

D19 therefore should not ask for another blind large-batch generation run.
It should use the observed review failures to constrain the next draft generation pass.

## 2. Problems Observed
The dominant problems observed in the D18.2 sampling reviews were:
- scaffold repetition
- templated opening
- topic phrase substitution
- shallow generic review framing
- weak topic-specific examples

Interpretation of these problems:
- many files swap topic words while preserving nearly identical explanatory skeletons
- markdown structure is often more memorable than the actual concept being taught
- some Python files look like generic draft wrappers instead of true topic-grounded code artifacts
- repeated review scaffolding overwhelms educational value and lowers corpus diversity

## 3. New Generation Constraints
The next generation pass must apply stronger constraints than batch_04.

Required constraints:
- no fixed `Concept / Explanation / Minimal Example / Common Pitfalls / Review Notes` template for every file
- each file must have a unique learning objective
- each file must include a topic-specific concrete example
- markdown files must vary structure across families
- Python files must implement the actual topic, not a generic summary pattern
- no review scaffold leakage
- no repeated opening families

Additional operational guidance:
- each worker prompt should explicitly ban slot-filled phrasing
- each worker prompt should require concrete observable evidence such as values, shapes, traces, artifacts, or decision branches where appropriate
- adjacent files inside the same subcategory should not be allowed to differ only by noun substitution
- repeated review-checklist wording should be treated as a generation failure, not as acceptable drafting style

## 4. Worker-Specific Repair Notes
### CC-1
- rewrite curriculum / optimization / regularization clusters
- replace repeated backbone wording with topic-specific contrasts, worked examples, and sharper teaching distinctions

### CC-2
- add concrete failure scenarios and decision examples
- make config/data-system explanations show what a reviewer would actually inspect or decide

### CC-3
- add tensor shapes, formulas, traces, and debugging steps
- remove generic transformer scaffold prose that can be reused across unrelated architecture topics

### CC-4
- add runtime artifacts, diagnostic signals, and real failure modes
- make runtime-system notes point to concrete operational evidence instead of abstract review posture language

### CC-5
- reduce bilingual Q&A template reuse
- improve natural bilingual explanation quality and require stronger topic-specific examples on both language sides

### CC-6
- rewrite `source_category_tools` to actually count, group, and report source categories
- require code snippets to do the named job rather than wrapping a generic numeric-summary pattern

## 5. Recommended Next Step
Recommended next step:
- D19.1 create batch_05 repair-aware small generation, not full `6000`-file generation

Why this is preferred:
- a smaller batch gives faster feedback on whether the anti-template constraints are actually working
- it avoids scaling a broken prompt pattern into another large rewrite burden
- it creates a cleaner validation loop between generation, review, and promotion readiness

## 6. Suggested Scale
Suggested first repair-aware scale:
- `6` workers × `100` files = `600` files first
- then validate again

Follow-up rule:
- do not expand to another large generation wave until the smaller repair-aware batch shows materially improved originality, topic specificity, and promotion readiness

## 7. What D19 Should Optimize For
D19 should optimize for:
- topic-specific educational value
- lower scaffold reuse
- stronger practical usefulness
- more concrete examples and diagnostics
- better file-to-file distinction within each worker family

D19 should not optimize for:
- raw file count alone
- another broad blind batch
- promotion speed over quality
- cosmetic variation that still preserves the same hidden scaffold

## 8. Decision Summary
D19 decision summary:
- repair-aware generation is required
- batch_04 should remain draft-only
- the next useful artifact is a small repair-aware batch_05, not a formal promotion attempt
