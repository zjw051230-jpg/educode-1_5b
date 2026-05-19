# Research Paper Inbox

Use this inbox for user-provided paper source materials and small registry inputs.

Directory roles:
- `raw_papers/`: PDFs or source files supplied by the user; keep Git-ignored by default
- `paper_lists/`: curated paper lists, reading queues, citation lists, or small text manifests

Rules:
- do not treat inbox content as training-approved by default
- do not copy unreviewed paper full text into `data/real_corpus/raw/synthetic_expanded/`
- do not convert long paper passages directly into training text
- preserve provenance for every source item in `metadata/paper_source_registry.jsonl`
