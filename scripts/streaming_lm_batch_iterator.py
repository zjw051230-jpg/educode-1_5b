from __future__ import annotations

import json
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

EXPECTED_SOURCE_CATEGORY = "public_pretraining_corpus"
EXPECTED_LICENSE = "odc-by"

TokenBlock = tuple[list[int], list[int]]
Batch = tuple[list[list[int]], list[list[int]]]


class EncodingLike(Protocol):
    ids: list[int]


class TokenizerLike(Protocol):
    def encode(self, text: str) -> EncodingLike:
        ...


@dataclass
class StreamingBatchStats:
    split_name: str
    required_batches: int
    sequence_length: int
    batch_size: int
    records_seen: int = 0
    docs_used: int = 0
    empty_text_count: int = 0
    token_ids_streamed: int = 0
    blocks_yielded: int = 0
    batches_yielded: int = 0
    cycle_restarts: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "split_name": self.split_name,
            "records_seen": self.records_seen,
            "docs_used": self.docs_used,
            "empty_text_count": self.empty_text_count,
            "token_ids_streamed": self.token_ids_streamed,
            "blocks_yielded": self.blocks_yielded,
            "available_batches": self.batches_yielded,
            "required_batches": self.required_batches,
            "used_batches": self.batches_yielded,
            "sequence_length": self.sequence_length,
            "batch_size": self.batch_size,
            "cycle_restarts": self.cycle_restarts,
            "streaming_mode": True,
            "host_ram_efficient_batching": True,
            "batch_precompute_disabled": True,
        }


def iter_jsonl_texts(
    path: Path,
    *,
    split_name: str = "data",
    expected_source_category: str = EXPECTED_SOURCE_CATEGORY,
    expected_license: str = EXPECTED_LICENSE,
    stats: StreamingBatchStats | None = None,
) -> Iterator[str]:
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue

            if stats is not None:
                stats.records_seen += 1

            record = json.loads(line)
            text = record.get("text")
            source_category = record.get("source_category")
            if source_category != expected_source_category:
                raise ValueError(
                    f"{split_name} line {line_number} expected source_category {expected_source_category!r} "
                    f"but found {source_category!r}"
                )

            license_name = record.get("license")
            if license_name != expected_license:
                raise ValueError(
                    f"{split_name} line {line_number} expected license {expected_license!r} but found {license_name!r}"
                )

            if record.get("allowed_for_training") is not True:
                raise ValueError(f"{split_name} line {line_number} is not approved for training")

            if not isinstance(text, str) or not text.strip():
                if stats is not None:
                    stats.empty_text_count += 1
                continue

            if stats is not None:
                stats.docs_used += 1
            yield text


def iter_token_blocks(
    text_iter: Iterator[str],
    tokenizer: TokenizerLike,
    sequence_length: int,
    eos_token_id: int | None,
    *,
    stats: StreamingBatchStats | None = None,
) -> Iterator[TokenBlock]:
    if sequence_length <= 0:
        raise ValueError("sequence_length must be positive")

    buffer: list[int] = []
    for text in text_iter:
        encoded_ids = tokenizer.encode(text).ids
        for token_id in encoded_ids:
            buffer.append(int(token_id))
            if stats is not None:
                stats.token_ids_streamed += 1
            while len(buffer) >= sequence_length + 1:
                x = buffer[:sequence_length]
                y = buffer[1 : sequence_length + 1]
                if stats is not None:
                    stats.blocks_yielded += 1
                yield x, y
                del buffer[0]

        if eos_token_id is not None:
            buffer.append(eos_token_id)
            if stats is not None:
                stats.token_ids_streamed += 1
            while len(buffer) >= sequence_length + 1:
                x = buffer[:sequence_length]
                y = buffer[1 : sequence_length + 1]
                if stats is not None:
                    stats.blocks_yielded += 1
                yield x, y
                del buffer[0]


def iter_batches(
    token_block_iter: Iterator[TokenBlock],
    batch_size: int,
    *,
    stats: StreamingBatchStats | None = None,
) -> Iterator[Batch]:
    if batch_size <= 0:
        raise ValueError("batch_size must be positive")

    batch_x: list[list[int]] = []
    batch_y: list[list[int]] = []
    for x, y in token_block_iter:
        batch_x.append(x)
        batch_y.append(y)
        if len(batch_x) == batch_size:
            if stats is not None:
                stats.batches_yielded += 1
            yield batch_x, batch_y
            batch_x = []
            batch_y = []


def cycle_batches(
    batch_factory: Callable[[], Iterator[Batch]],
    max_batches: int,
    *,
    stats: StreamingBatchStats | None = None,
) -> Iterator[Batch]:
    if max_batches <= 0:
        return

    yielded = 0
    while yielded < max_batches:
        produced_this_cycle = 0
        for batch in batch_factory():
            yield batch
            yielded += 1
            produced_this_cycle += 1
            if yielded >= max_batches:
                return
        if produced_this_cycle == 0:
            raise ValueError("streaming batch factory produced no full batches")
        if stats is not None:
            stats.cycle_restarts += 1


def create_streaming_batch_iterator(
    *,
    split_name: str,
    split_path: Path,
    tokenizer: TokenizerLike,
    sequence_length: int,
    batch_size: int,
    required_batches: int,
    eos_token_id: int | None,
) -> tuple[Iterator[Batch], StreamingBatchStats]:
    stats = StreamingBatchStats(
        split_name=split_name,
        required_batches=required_batches,
        sequence_length=sequence_length,
        batch_size=batch_size,
    )

    def batch_factory() -> Iterator[Batch]:
        return iter_batches(
            iter_token_blocks(
                iter_jsonl_texts(split_path, split_name=split_name, stats=stats),
                tokenizer,
                sequence_length,
                eos_token_id,
                stats=stats,
            ),
            batch_size,
            stats=stats,
        )

    return cycle_batches(batch_factory, required_batches, stats=stats), stats
