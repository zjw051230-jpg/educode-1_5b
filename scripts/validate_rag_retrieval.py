from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from educode.rag import build_prompt_context
from educode.retrieval import DocumentChunk, RetrievalConfig, TokenOverlapRetriever, evaluate_retrieval


def main() -> int:
    chunks = [
        DocumentChunk(doc_id="python-loops", chunk_id="c1", text="Python for loops iterate over lists."),
        DocumentChunk(doc_id="cuda-memory", chunk_id="c2", text="A100 memory profiling tracks allocated CUDA memory."),
        DocumentChunk(doc_id="bpe", chunk_id="c3", text="BPE tokenizers merge frequent byte pairs."),
    ]
    retriever = TokenOverlapRetriever(chunks, RetrievalConfig(top_k=2))
    results = retriever.search("CUDA memory profiling")
    report = evaluate_retrieval(
        retriever,
        [
            {"query": "CUDA memory", "expected_doc_id": "cuda-memory"},
            {"query": "byte pair tokenizer", "expected_doc_id": "bpe"},
        ],
    )
    payload = {
        "validation_status": "passed" if report["hit_rate"] == 1.0 and results else "failed",
        "query_count": report["query_count"],
        "hit_rate": report["hit_rate"],
        "context_preview": build_prompt_context(results),
        "network_used": False,
        "external_vector_db_used": False,
        "modal_used": False,
        "gpu_used": False,
        "training_started": False,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["validation_status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
