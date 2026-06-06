from __future__ import annotations

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from educode.rag import build_prompt_context  # noqa: E402
from educode.retrieval import (  # noqa: E402
    DocumentChunk,
    RetrievalConfig,
    TokenOverlapRetriever,
    evaluate_retrieval,
)


class RagRetrievalTests(unittest.TestCase):
    def chunks(self) -> list[DocumentChunk]:
        return [
            DocumentChunk(doc_id="python-loops", chunk_id="c1", text="Python for loops iterate over lists."),
            DocumentChunk(doc_id="cuda-memory", chunk_id="c2", text="A100 memory profiling tracks allocated CUDA memory."),
            DocumentChunk(doc_id="bpe", chunk_id="c3", text="BPE tokenizers merge frequent byte pairs."),
        ]

    def test_small_fixture_retrieval_prefers_token_overlap(self) -> None:
        retriever = TokenOverlapRetriever(self.chunks(), RetrievalConfig(top_k=2))

        results = retriever.search("How do Python loops work?")

        self.assertEqual(results[0].chunk.doc_id, "python-loops")
        self.assertGreater(results[0].score, 0)

    def test_context_builder_preserves_citations_and_doc_ids(self) -> None:
        retriever = TokenOverlapRetriever(self.chunks(), RetrievalConfig(top_k=1))
        results = retriever.search("CUDA memory")

        context = build_prompt_context(results)

        self.assertIn("[1] doc_id=cuda-memory chunk_id=c2", context)
        self.assertIn("A100 memory profiling", context)

    def test_empty_query_returns_no_results(self) -> None:
        retriever = TokenOverlapRetriever(self.chunks(), RetrievalConfig(top_k=2))

        self.assertEqual(retriever.search("   "), [])

    def test_bad_retrieval_config_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            RetrievalConfig(top_k=0)

    def test_retrieval_evaluator_reports_hit_rate(self) -> None:
        retriever = TokenOverlapRetriever(self.chunks(), RetrievalConfig(top_k=1))

        report = evaluate_retrieval(
            retriever,
            [{"query": "byte pair tokenizer", "expected_doc_id": "bpe"}],
        )

        self.assertEqual(report["query_count"], 1)
        self.assertEqual(report["hit_count"], 1)
        self.assertEqual(report["hit_rate"], 1.0)


if __name__ == "__main__":
    unittest.main()
