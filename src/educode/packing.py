from __future__ import annotations


def _validate_lengths(document_lengths: list[int], context_length: int) -> None:
    if context_length <= 0:
        raise ValueError("context_length must be positive")
    for length in document_lengths:
        if length <= 0:
            raise ValueError("document lengths must be positive")
        if length > context_length:
            raise ValueError("document length exceeds context_length")


def pack_document_lengths(
    document_lengths: list[int], context_length: int, separator_tokens: int = 0
) -> list[list[int]]:
    if separator_tokens < 0:
        raise ValueError("separator_tokens must be non-negative")
    _validate_lengths(document_lengths, context_length)
    packs: list[list[int]] = []
    current: list[int] = []
    current_tokens = 0
    for length in document_lengths:
        extra_separator = separator_tokens if current else 0
        needed = length + extra_separator
        if current and current_tokens + needed > context_length:
            packs.append(current)
            current = [length]
            current_tokens = length
        else:
            current.append(length)
            current_tokens += needed
    if current:
        packs.append(current)
    return packs


def token_utilization(packs: list[list[int]], context_length: int) -> dict:
    if context_length <= 0:
        raise ValueError("context_length must be positive")
    used_tokens = sum(sum(pack) for pack in packs)
    capacity_tokens = len(packs) * context_length
    padding_tokens = capacity_tokens - used_tokens
    return {
        "pack_count": len(packs),
        "used_tokens": used_tokens,
        "capacity_tokens": capacity_tokens,
        "padding_tokens": padding_tokens,
        "utilization_ratio": used_tokens / capacity_tokens if capacity_tokens else 0.0,
    }


def estimate_padding_waste(document_lengths: list[int], context_length: int) -> dict:
    packs = pack_document_lengths(document_lengths, context_length)
    packed = token_utilization(packs, context_length)
    unpacked_capacity = len(document_lengths) * context_length
    used_tokens = sum(document_lengths)
    return {
        "document_count": len(document_lengths),
        "unpacked_padding_tokens": unpacked_capacity - used_tokens,
        "packed_padding_tokens": packed["padding_tokens"],
        "padding_tokens_saved": (unpacked_capacity - used_tokens) - packed["padding_tokens"],
        "packed_utilization_ratio": packed["utilization_ratio"],
    }
