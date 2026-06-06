from __future__ import annotations

from dataclasses import dataclass

from src.educode.dedup import _tokens


@dataclass(frozen=True)
class QualityConfig:
    low_information_unique_token_threshold: int = 3

    def __post_init__(self) -> None:
        if self.low_information_unique_token_threshold < 0:
            raise ValueError("low information threshold must be non-negative")


def quality_metrics(text: str, config: QualityConfig) -> dict:
    if not text.strip():
        raise ValueError("text must be non-empty")
    lines = [line for line in text.splitlines() if line.strip()]
    tokens = _tokens(text)
    unique = set(tokens)
    control_chars = sum(1 for char in text if ord(char) < 32 and char not in "\n\r\t")
    return {
        "char_count": len(text),
        "doc_length": len(tokens),
        "line_count": len(lines),
        "max_line_length": max(len(line) for line in lines),
        "mean_line_length": sum(len(line) for line in lines) / len(lines),
        "control_char_ratio": control_chars / len(text),
        "unique_token_count": len(unique),
        "repetition_ratio": 1.0 - (len(unique) / len(tokens)) if tokens else 0.0,
        "low_information": len(unique) <= config.low_information_unique_token_threshold,
    }
