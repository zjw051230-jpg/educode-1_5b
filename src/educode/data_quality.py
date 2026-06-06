from __future__ import annotations

import re
from itertools import combinations


TOKEN_RE = re.compile(r"\w+", re.UNICODE)


def _tokens(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text)]


def text_quality_metrics(text: str) -> dict:
    if not text.strip():
        raise ValueError("text must be non-empty")
    lines = [line for line in text.splitlines() if line.strip()]
    tokens = _tokens(text)
    unique_tokens = set(tokens)
    ascii_chars = sum(1 for char in text if ord(char) < 128)
    return {
        "char_count": len(text),
        "line_count": len(lines),
        "token_count": len(tokens),
        "unique_token_count": len(unique_tokens),
        "max_line_length": max((len(line) for line in lines), default=0),
        "mean_line_length": sum(len(line) for line in lines) / len(lines) if lines else 0.0,
        "repetition_ratio": 1.0 - (len(unique_tokens) / len(tokens)) if tokens else 0.0,
        "ascii_fraction": ascii_chars / len(text),
    }


def _shingles(text: str, k: int) -> set[tuple[str, ...]]:
    if k <= 0:
        raise ValueError("k must be positive")
    tokens = _tokens(text)
    if len(tokens) < k:
        return {tuple(tokens)} if tokens else set()
    return {tuple(tokens[index : index + k]) for index in range(len(tokens) - k + 1)}


def shingle_jaccard(a: str, b: str, k: int = 5) -> float:
    left = _shingles(a, k)
    right = _shingles(b, k)
    if not left and not right:
        return 1.0
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def detect_near_duplicates(
    texts: list[str], threshold: float = 0.8, k: int = 5
) -> list[tuple[int, int]]:
    if not 0.0 <= threshold <= 1.0:
        raise ValueError("threshold must be between 0 and 1")
    duplicates = []
    for left_index, right_index in combinations(range(len(texts)), 2):
        score = shingle_jaccard(texts[left_index], texts[right_index], k=k)
        if score >= threshold:
            duplicates.append((left_index, right_index))
    return duplicates
