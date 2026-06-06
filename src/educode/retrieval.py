from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Iterable, Protocol


def tokenize(text: str) -> set[str]:
    return {piece.lower() for piece in re.findall(r"[A-Za-z0-9_]+", text)}


@dataclass(frozen=True)
class DocumentChunk:
    doc_id: str
    chunk_id: str
    text: str
    metadata: dict[str, str] | None = None

    def __post_init__(self) -> None:
        if not self.doc_id.strip():
            raise ValueError("doc_id is required")
        if not self.chunk_id.strip():
            raise ValueError("chunk_id is required")
        if not self.text.strip():
            raise ValueError("text is required")


@dataclass(frozen=True)
class RetrievalConfig:
    top_k: int = 3
    min_score: float = 0.0

    def __post_init__(self) -> None:
        if self.top_k <= 0:
            raise ValueError("top_k must be positive")
        if self.min_score < 0:
            raise ValueError("min_score must be non-negative")


@dataclass(frozen=True)
class RetrievalResult:
    chunk: DocumentChunk
    score: float
    rank: int


class Retriever(Protocol):
    def search(self, query: str) -> list[RetrievalResult]:
        ...


class EmbeddingRetrieverPlaceholder:
    def search(self, query: str) -> list[RetrievalResult]:
        raise NotImplementedError("embedding retrieval is a future integration point")


class TokenOverlapRetriever:
    def __init__(self, chunks: Iterable[DocumentChunk], config: RetrievalConfig | None = None) -> None:
        self.config = config or RetrievalConfig()
        self.chunks = list(chunks)
        self._chunk_tokens = [(chunk, tokenize(chunk.text)) for chunk in self.chunks]

    def search(self, query: str) -> list[RetrievalResult]:
        query_tokens = tokenize(query)
        if not query_tokens:
            return []

        scored: list[tuple[DocumentChunk, float]] = []
        for chunk, chunk_tokens in self._chunk_tokens:
            if not chunk_tokens:
                continue
            overlap = len(query_tokens & chunk_tokens)
            if overlap == 0:
                continue
            score = overlap / math.sqrt(len(query_tokens) * len(chunk_tokens))
            if score >= self.config.min_score:
                scored.append((chunk, score))

        scored.sort(key=lambda item: (-item[1], item[0].doc_id, item[0].chunk_id))
        return [
            RetrievalResult(chunk=chunk, score=score, rank=index + 1)
            for index, (chunk, score) in enumerate(scored[: self.config.top_k])
        ]


def evaluate_retrieval(retriever: Retriever, cases: Iterable[dict[str, str]]) -> dict[str, object]:
    evaluated = []
    hit_count = 0
    for case in cases:
        query = case["query"]
        expected_doc_id = case["expected_doc_id"]
        results = retriever.search(query)
        result_doc_ids = [result.chunk.doc_id for result in results]
        hit = expected_doc_id in result_doc_ids
        hit_count += int(hit)
        evaluated.append(
            {
                "query": query,
                "expected_doc_id": expected_doc_id,
                "result_doc_ids": result_doc_ids,
                "hit": hit,
            }
        )
    query_count = len(evaluated)
    return {
        "query_count": query_count,
        "hit_count": hit_count,
        "hit_rate": hit_count / query_count if query_count else 0.0,
        "cases": evaluated,
    }
