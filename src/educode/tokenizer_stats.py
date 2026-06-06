from __future__ import annotations

from collections import Counter
from dataclasses import dataclass


@dataclass(frozen=True)
class TokenizerStatsConfig:
    special_tokens: tuple[str, ...] = ("<bos>", "<eos>", "<pad>", "<unk>")
    unk_token: str | None = "<unk>"


def _simple_tokens(text: str) -> list[str]:
    return text.split()


def analyze_tokenizer_stats(text: str, config: TokenizerStatsConfig) -> dict:
    if not text.strip():
        raise ValueError("text must be non-empty")
    tokens = _simple_tokens(text)
    frequency = Counter(tokens)
    special_count = sum(frequency[token] for token in config.special_tokens)
    unk_count = frequency[config.unk_token] if config.unk_token else 0
    byte_count = len(text.encode("utf-8"))
    token_count = len(tokens)
    return {
        "token_count": token_count,
        "unique_token_count": len(frequency),
        "frequency": dict(sorted(frequency.items())),
        "special_token_count": special_count,
        "special_token_rate": special_count / token_count,
        "unknown_token_count": unk_count,
        "unknown_token_rate": unk_count / token_count,
        "bytes_per_token": byte_count / token_count,
        "compression_ratio_proxy": token_count / byte_count,
    }
