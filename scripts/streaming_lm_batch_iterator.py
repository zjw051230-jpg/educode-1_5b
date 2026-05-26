from __future__ import annotations

import json
import random
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

EXPECTED_SOURCE_CATEGORY = "public_pretraining_corpus"
EXPECTED_LICENSE = "odc-by"
SEQUENTIAL_PREFIX = "sequential_prefix"
SHUFFLE_BUFFER = "shuffle_buffer"
SUPPORTED_SAMPLING_POLICIES = {SEQUENTIAL_PREFIX, SHUFFLE_BUFFER}

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
    sampling_policy: str = SEQUENTIAL_PREFIX
    shuffle_seed: int | None = None
    shuffle_buffer_size: int = 1
    records_seen: int = 0
    docs_used: int = 0
    empty_text_count: int = 0
    token_ids_streamed: int = 0
    blocks_yielded: int = 0
    batches_yielded: int = 0
    cycle_restarts: int = 0
    documents_buffered_total: int = 0
    max_shuffle_buffer_occupancy: int = 0
    shuffle_buffer_underfilled: bool = False
    bounded_prefix_batches_only: bool = True
    last_shuffle_seed_used: int | None = None

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
            "sampling_policy": self.sampling_policy,
            "shuffle_seed": self.shuffle_seed,
            "shuffle_buffer_size": self.shuffle_buffer_size,
            "documents_buffered_total": self.documents_buffered_total,
            "max_shuffle_buffer_occupancy": self.max_shuffle_buffer_occupancy,
            "shuffle_buffer_underfilled": self.shuffle_buffer_underfilled,
            "bounded_prefix_batches_only": self.bounded_prefix_batches_only,
            "last_shuffle_seed_used": self.last_shuffle_seed_used,
        }


def normalize_sampling_policy(sampling_policy: str | None) -> str:
    if sampling_policy is None:
        return SEQUENTIAL_PREFIX
    policy = str(sampling_policy).strip().lower()
    if policy not in SUPPORTED_SAMPLING_POLICIES:
        raise ValueError(f"unsupported sampling policy: {policy}")
    return policy


def normalize_shuffle_buffer_size(shuffle_buffer_size: int | None) -> int:
    if shuffle_buffer_size is None:
        return 1
    return int(shuffle_buffer_size)


def effective_sampling_policy(sampling_policy: str, shuffle_buffer_size: int) -> str:
    if sampling_policy == SHUFFLE_BUFFER and shuffle_buffer_size > 1:
        return SHUFFLE_BUFFER
    return SEQUENTIAL_PREFIX


def is_bounded_prefix_sampling(sampling_policy: str, shuffle_buffer_size: int) -> bool:
    return effective_sampling_policy(sampling_policy, shuffle_buffer_size) == SEQUENTIAL_PREFIX


def apply_sampling_metadata(
    stats: StreamingBatchStats | None,
    *,
    sampling_policy: str,
    shuffle_seed: int | None,
    shuffle_buffer_size: int,
) -> None:
    if stats is None:
        return
    effective_policy = effective_sampling_policy(sampling_policy, shuffle_buffer_size)
    stats.sampling_policy = effective_policy
    if stats.shuffle_seed is None:
        stats.shuffle_seed = shuffle_seed
    stats.shuffle_buffer_size = shuffle_buffer_size
    stats.bounded_prefix_batches_only = effective_policy == SEQUENTIAL_PREFIX
    stats.last_shuffle_seed_used = shuffle_seed


def iter_shuffle_buffered_texts(
    text_iter: Iterator[str],
    *,
    shuffle_seed: int | None,
    shuffle_buffer_size: int,
    stats: StreamingBatchStats | None = None,
) -> Iterator[str]:
    if shuffle_buffer_size <= 1:
        yield from text_iter
        return

    rng = random.Random(0 if shuffle_seed is None else shuffle_seed)
    buffer: list[str] = []
    documents_buffered_this_iter = 0
    for text in text_iter:
        buffer.append(text)
        documents_buffered_this_iter += 1
        if stats is not None:
            stats.documents_buffered_total += 1
            stats.max_shuffle_buffer_occupancy = max(stats.max_shuffle_buffer_occupancy, len(buffer))
        if len(buffer) >= shuffle_buffer_size:
            yield buffer.pop(rng.randrange(len(buffer)))

    if stats is not None and 0 < documents_buffered_this_iter < shuffle_buffer_size:
        stats.shuffle_buffer_underfilled = True
    while buffer:
        yield buffer.pop(rng.randrange(len(buffer)))


def iter_jsonl_texts(
    path: Path,
    *,
    split_name: str = "data",
    expected_source_category: str = EXPECTED_SOURCE_CATEGORY,
    expected_license: str = EXPECTED_LICENSE,
    sampling_policy: str | None = None,
    shuffle_seed: int | None = None,
    shuffle_buffer_size: int | None = None,
    stats: StreamingBatchStats | None = None,
) -> Iterator[str]:
    normalized_sampling_policy = normalize_sampling_policy(sampling_policy)
    normalized_shuffle_buffer_size = normalize_shuffle_buffer_size(shuffle_buffer_size)
    apply_sampling_metadata(
        stats,
        sampling_policy=normalized_sampling_policy,
        shuffle_seed=shuffle_seed,
        shuffle_buffer_size=normalized_shuffle_buffer_size,
    )

    def validated_texts() -> Iterator[str]:
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

    if effective_sampling_policy(normalized_sampling_policy, normalized_shuffle_buffer_size) == SHUFFLE_BUFFER:
        yield from iter_shuffle_buffered_texts(
            validated_texts(),
            shuffle_seed=shuffle_seed,
            shuffle_buffer_size=normalized_shuffle_buffer_size,
            stats=stats,
        )
    else:
        yield from validated_texts()


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
    sampling_policy: str | None = None,
    shuffle_seed: int | None = None,
    shuffle_buffer_size: int | None = None,
) -> tuple[Iterator[Batch], StreamingBatchStats]:
    normalized_sampling_policy = normalize_sampling_policy(sampling_policy)
    normalized_shuffle_buffer_size = normalize_shuffle_buffer_size(shuffle_buffer_size)
    effective_policy = effective_sampling_policy(normalized_sampling_policy, normalized_shuffle_buffer_size)
    stats = StreamingBatchStats(
        split_name=split_name,
        required_batches=required_batches,
        sequence_length=sequence_length,
        batch_size=batch_size,
        sampling_policy=effective_policy,
        shuffle_seed=shuffle_seed,
        shuffle_buffer_size=normalized_shuffle_buffer_size,
        bounded_prefix_batches_only=effective_policy == SEQUENTIAL_PREFIX,
    )
    cycle_index = 0

    def batch_factory() -> Iterator[Batch]:
        nonlocal cycle_index
        cycle_shuffle_seed = shuffle_seed
        if effective_policy == SHUFFLE_BUFFER and shuffle_seed is not None:
            cycle_shuffle_seed = shuffle_seed + cycle_index
        cycle_index += 1
        return iter_batches(
            iter_token_blocks(
                iter_jsonl_texts(
                    split_path,
                    split_name=split_name,
                    sampling_policy=normalized_sampling_policy,
                    shuffle_seed=cycle_shuffle_seed,
                    shuffle_buffer_size=normalized_shuffle_buffer_size,
                    stats=stats,
                ),
                tokenizer,
                sequence_length,
                eos_token_id,
                stats=stats,
            ),
            batch_size,
            stats=stats,
        )

    return cycle_batches(batch_factory, required_batches, stats=stats), stats
