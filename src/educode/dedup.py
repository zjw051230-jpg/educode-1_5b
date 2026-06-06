from __future__ import annotations

import re
from itertools import combinations


TOKEN_RE = re.compile(r"\w+", re.UNICODE)


def _tokens(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text)]


def detect_exact_duplicates(texts: list[str]) -> list[tuple[int, int]]:
    seen: dict[str, int] = {}
    duplicates = []
    for index, text in enumerate(texts):
        key = text.strip()
        if key in seen:
            duplicates.append((seen[key], index))
        else:
            seen[key] = index
    return duplicates


def shingles(text: str, k: int) -> set[tuple[str, ...]]:
    if k <= 0:
        raise ValueError("k must be positive")
    tokens = _tokens(text)
    if len(tokens) < k:
        return {tuple(tokens)} if tokens else set()
    return {tuple(tokens[i : i + k]) for i in range(len(tokens) - k + 1)}


def shingle_jaccard(a: str, b: str, k: int) -> float:
    left = shingles(a, k)
    right = shingles(b, k)
    if not left and not right:
        return 1.0
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def detect_near_duplicates(texts: list[str], threshold: float, k: int) -> list[tuple[int, int]]:
    if not 0 <= threshold <= 1:
        raise ValueError("threshold must be between 0 and 1")
    pairs = []
    for i, j in combinations(range(len(texts)), 2):
        if shingle_jaccard(texts[i], texts[j], k) >= threshold:
            pairs.append((i, j))
    return pairs


def minhash_feasibility() -> dict:
    return {
        "status": "placeholder",
        "implemented": False,
        "reason": "MinHash is planned for larger sampled batches after review.",
    }
