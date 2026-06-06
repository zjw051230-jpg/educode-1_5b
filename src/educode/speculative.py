from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class DraftProposer(Protocol):
    def propose(self, prefix: list[int], max_tokens: int) -> list[int]:
        ...


@dataclass
class NgramProposer:
    ngram_size: int = 2
    fallback_token_id: int = 0

    def propose(self, prefix: list[int], max_tokens: int) -> list[int]:
        if max_tokens <= 0:
            raise ValueError("max_tokens must be positive")
        if len(prefix) >= self.ngram_size:
            pattern = prefix[-self.ngram_size :]
        else:
            pattern = [self.fallback_token_id]
        result: list[int] = []
        while len(result) < max_tokens:
            result.extend(pattern)
        return result[:max_tokens]


def speculative_decode_skeleton(prefix: list[int], proposer: DraftProposer, max_draft_tokens: int) -> dict[str, object]:
    draft = proposer.propose(prefix, max_draft_tokens)
    return {
        "accepted_tokens": [],
        "draft_tokens": draft,
        "requires_target_model_verification": True,
    }
