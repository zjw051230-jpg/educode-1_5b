from __future__ import annotations


def build_document_boundaries(documents: list[list[int]]) -> list[tuple[int, int]]:
    boundaries = []
    cursor = 0
    for document in documents:
        if not document:
            raise ValueError("documents must be non-empty")
        end = cursor + len(document)
        boundaries.append((cursor, end))
        cursor = end
    return boundaries
