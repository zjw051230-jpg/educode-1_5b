---
draft_status: candidate
topic_id: PDS-015
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC2
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
---

# Why Repo-Root Config Resolution Matters

## Concept
Config resolution decides where the program looks for its configuration file. Resolving from the repo root can make examples more predictable across different working directories.

## Explanation
A frequent beginner problem is running the same script from two different directories and getting two different outcomes. One run finds `configs/train.yaml`; the other claims the file does not exist. The code may be correct, but the path assumption is fragile.

Repo-root resolution makes the assumption explicit. Instead of depending on the caller’s current directory, the script computes paths relative to a known project anchor. That improves reproducibility for educational examples because the reader sees one clear convention.

This does not mean every path in a system should be absolute. It means the code should have one stable reference point for locating shared project assets.

## Minimal Example
A loader might:
1. discover the repo root once
2. join `configs/` with a requested filename
3. validate that the resulting path exists before parsing

The important part is consistency, not sophistication.

## Common Pitfalls
- Mixing caller-relative and repo-relative paths in one script.
- Hardcoding machine-specific absolute paths.
- Letting the config parser fail with a vague file-not-found message.
- Assuming notebooks and scripts share the same working directory behavior.

## Review Notes
For draft educational material, repo-root resolution is often easier to explain than environment-dependent lookup rules. It keeps examples portable without introducing external tooling.
