from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class PagedBlockTable:
    block_size: int
    table: dict[int, list[int]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.block_size <= 0:
            raise ValueError("block_size must be positive")

    def allocate(self, sequence_id: int, token_count: int) -> list[int]:
        if token_count < 0:
            raise ValueError("token_count must be non-negative")
        block_count = (token_count + self.block_size - 1) // self.block_size
        current_max = max((block for blocks in self.table.values() for block in blocks), default=-1)
        blocks = list(range(current_max + 1, current_max + 1 + block_count))
        self.table[sequence_id] = blocks
        return blocks

    def lookup(self, sequence_id: int) -> list[int]:
        return list(self.table.get(sequence_id, []))

    def release(self, sequence_id: int) -> None:
        self.table.pop(sequence_id, None)
