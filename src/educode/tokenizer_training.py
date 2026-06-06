from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

REQUIRED_SPECIAL_TOKENS = ("<|endoftext|>", "<|pad|>", "<|unk|>")


def validate_special_tokens(tokens: Sequence[str]) -> tuple[str, ...]:
    token_tuple = tuple(tokens)
    if len(set(token_tuple)) != len(token_tuple):
        raise ValueError("special tokens must be unique")
    missing = [token for token in REQUIRED_SPECIAL_TOKENS if token not in token_tuple]
    if missing:
        raise ValueError(f"missing required special tokens: {missing}")
    return token_tuple


@dataclass(frozen=True)
class TokenizerTrainingConfig:
    vocab_size: int
    min_frequency: int = 2
    sample_limit: int = 1000
    algorithm: str = "byte_level_bpe"
    special_tokens: tuple[str, ...] = REQUIRED_SPECIAL_TOKENS

    def __post_init__(self) -> None:
        if self.algorithm not in {"byte_level_bpe", "unigram_placeholder"}:
            raise ValueError(f"unsupported tokenizer algorithm: {self.algorithm}")
        if self.vocab_size < 16:
            raise ValueError("vocab_size must be at least 16 for feasibility planning")
        if self.min_frequency <= 0:
            raise ValueError("min_frequency must be positive")
        if self.sample_limit <= 0:
            raise ValueError("sample_limit must be positive")
        validate_special_tokens(self.special_tokens)


class ToyByteTokenizer:
    def __init__(self, special_tokens: Sequence[str] = REQUIRED_SPECIAL_TOKENS) -> None:
        self.special_tokens = validate_special_tokens(special_tokens)
        self.special_to_id = {token: index for index, token in enumerate(self.special_tokens)}
        self.byte_offset = len(self.special_tokens)
        self.unk_token = "<|unk|>"

    @property
    def vocab_size(self) -> int:
        return self.byte_offset + 256

    def encode(self, text: str) -> list[int]:
        return [self.byte_offset + value for value in text.encode("utf-8")]

    def decode(self, token_ids: Sequence[int]) -> str:
        byte_values = []
        for token_id in token_ids:
            if token_id < self.byte_offset:
                continue
            value = token_id - self.byte_offset
            if not 0 <= value <= 255:
                value = ord("?")
            byte_values.append(value)
        return bytes(byte_values).decode("utf-8", errors="replace")


def vocab_stats(tokenizer: ToyByteTokenizer) -> dict[str, object]:
    return {
        "vocab_size": tokenizer.vocab_size,
        "special_token_count": len(tokenizer.special_tokens),
        "special_tokens": list(tokenizer.special_tokens),
        "unk_token": tokenizer.unk_token,
        "byte_token_count": 256,
        "trained_on_real_data": False,
    }
