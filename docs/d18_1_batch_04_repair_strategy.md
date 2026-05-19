# D18.1 Batch 04 Repair Strategy

## 1. Purpose
This document records the decision framework that should follow the D18.1 targeted human sampling review for batch_04.

## 2. If Sampling Confirms Obvious Template Concentration
If the sampled files show that templated openings, repeated internal lines, or boilerplate-heavy markdown scaffolds dominate the risky workers:
- do not directly promote the full `6000`-file batch
- keep the cleaner `quality_pass` subset in candidate status only
- create rewrite-family planning for `needs_edit` records
- apply stronger future generation constraints to high-template workers before asking for new draft families

Recommended interpretation:
- `CC-2` and `CC-3` should remain blocked on rewrite-family planning
- markdown-heavy `CC-5` and `CC-6` should be narrowed to the cleaner subset until the markdown scaffolds are revised

## 3. If Sampling Quality Is Broadly Acceptable
If the sampled files show that many drafts remain distinct, useful, and repair-light despite the automated notes:
- D18.2 may create a promotion-candidate subset
- do not promote all `6000` files at once
- instead propose a smaller bounded subset, such as `500`-`1000` files, after explicit human review outcomes are recorded

The goal is to validate promotion criteria on a controlled subset before any larger decision is made.

## 4. If Sampling Quality Is Weak
If the sampling review shows that the risky workers are genuinely too formulaic or too low-value:
- D18.2 should enter a repair pass
- do not promote the batch
- use the review notes to define rewrite clusters by worker, subcategory, and failure family

This means the next useful artifact is not a promotion pack but a repair-planning pack.

## 5. Immediate Guidance
Until D18.1 human review is complete:
- all files remain draft-only candidates
- all files remain `approved_for_training: false`
- no promotion decision should be treated as implicit or automatic
