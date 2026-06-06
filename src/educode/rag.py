from __future__ import annotations

from educode.retrieval import RetrievalResult


def build_prompt_context(results: list[RetrievalResult], *, max_chars: int = 4000) -> str:
    if max_chars <= 0:
        raise ValueError("max_chars must be positive")
    sections: list[str] = []
    used_chars = 0
    for index, result in enumerate(results, start=1):
        header = f"[{index}] doc_id={result.chunk.doc_id} chunk_id={result.chunk.chunk_id} score={result.score:.4f}"
        body = result.chunk.text.strip()
        section = f"{header}\n{body}"
        remaining = max_chars - used_chars
        if remaining <= 0:
            break
        if len(section) > remaining:
            section = section[:remaining].rstrip()
        sections.append(section)
        used_chars += len(section)
    return "\n\n".join(sections)
