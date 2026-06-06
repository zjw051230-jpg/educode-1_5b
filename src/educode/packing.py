from __future__ import annotations

from dataclasses import dataclass

from src.educode.document_boundaries import build_document_boundaries


@dataclass(frozen=True)
class PackingConfig:
    context_length: int
    allow_cross_document_attention: bool = True

    def __post_init__(self) -> None:
        if self.context_length <= 0:
            raise ValueError("context_length must be positive")


@dataclass(frozen=True)
class PackedSequence:
    documents: list[list[int]]
    tokens: list[int]
    boundaries: list[tuple[int, int]]
    allow_cross_document_attention: bool


def pack_documents(documents: list[list[int]], config: PackingConfig) -> list[PackedSequence]:
    packs: list[list[list[int]]] = []
    current: list[list[int]] = []
    current_len = 0
    for document in documents:
        if not document:
            raise ValueError("documents must be non-empty")
        if len(document) > config.context_length:
            raise ValueError("document exceeds context_length")
        if current and current_len + len(document) > config.context_length:
            packs.append(current)
            current = [document]
            current_len = len(document)
        else:
            current.append(document)
            current_len += len(document)
    if current:
        packs.append(current)
    return [
        PackedSequence(
            documents=pack,
            tokens=[token for document in pack for token in document],
            boundaries=build_document_boundaries(pack),
            allow_cross_document_attention=config.allow_cross_document_attention,
        )
        for pack in packs
    ]


def build_loss_mask(pack: PackedSequence, context_length: int) -> list[int]:
    if context_length < len(pack.tokens):
        raise ValueError("context_length shorter than packed token length")
    return [1] * len(pack.tokens) + [0] * (context_length - len(pack.tokens))


def estimate_padding_waste(documents: list[list[int]], config: PackingConfig) -> dict:
    packs = pack_documents(documents, config)
    used = sum(len(document) for document in documents)
    unpacked_capacity = len(documents) * config.context_length
    packed_capacity = len(packs) * config.context_length
    return {
        "document_count": len(documents),
        "pack_count": len(packs),
        "used_tokens": used,
        "unpacked_padding_tokens": unpacked_capacity - used,
        "packed_padding_tokens": packed_capacity - used,
        "padding_tokens_saved": (unpacked_capacity - used) - (packed_capacity - used),
        "allow_cross_document_attention": config.allow_cross_document_attention,
    }
