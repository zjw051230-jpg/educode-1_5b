# RAG Retrieval Skeleton

This branch adds a local retrieval and RAG context-building skeleton for future educational/code knowledge augmentation. It does not connect to an external vector database, download corpora, call network services, or load a model checkpoint.

## Scope

- `DocumentChunk` schema with document id, chunk id, text, and optional metadata.
- Token-overlap retriever for tiny local fixtures.
- Embedding retriever placeholder for future integration.
- Retrieval evaluator with simple hit-rate reporting.
- Prompt context builder that preserves doc ids, chunk ids, ranks, and scores as citations.

## Safety Boundaries

- No external vector DB.
- No network calls.
- No GPU, Modal, training, profiling, or checkpoint loading.
- No raw or prepared data is required.

## Validation

```powershell
.\.venv\Scripts\python.exe -m py_compile src\educode\retrieval.py src\educode\rag.py scripts\validate_rag_retrieval.py tests\test_rag_retrieval.py
.\.venv\Scripts\python.exe scripts\validate_rag_retrieval.py
.\.venv\Scripts\python.exe tests\test_rag_retrieval.py
git diff --check
```

Future real retrieval work should add dataset provenance, chunking policy, citation formatting review, and quality evaluation before being wired into inference.
