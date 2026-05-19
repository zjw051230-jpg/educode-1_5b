# Research Paper Assistant Corpus

This directory holds source-library inputs, metadata, derived research-assistant artifacts, and review-only draft outputs for the E-line research paper assistant workflow.

Important boundaries:
- raw paper files in `inbox/raw_papers/` are source materials only
- raw paper files do not enter the formal training corpus by default
- `rag_library/` is for retrieval-oriented organization, not automatic training approval
- `derived/` is for project-authored summaries, notes, extraction outputs, and other reviewable transformations
- `draft_queue/` is for candidate assistant-style corpus items that still require explicit review
- only explicitly approved, license-safe, non-replicative artifacts may later be considered for formal corpus promotion
