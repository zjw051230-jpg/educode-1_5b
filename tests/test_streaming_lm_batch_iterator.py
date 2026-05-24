from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
for path in (PROJECT_ROOT, SRC_PATH):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from educode.sequence_dataset import batch_samples, make_next_token_samples
from scripts.streaming_lm_batch_iterator import (
    cycle_batches,
    iter_batches,
    iter_jsonl_texts,
    iter_token_blocks,
)


class FakeEncoding:
    def __init__(self, ids: list[int]) -> None:
        self.ids = ids


class FakeTokenizer:
    def encode(self, text: str) -> FakeEncoding:
        return FakeEncoding([int(part) for part in text.split()])


def write_jsonl(path: Path, records: list[dict[str, object]]) -> None:
    path.write_text("".join(json.dumps(record) + "\n" for record in records), encoding="utf-8")


def approved_record(text: str) -> dict[str, object]:
    return {
        "text": text,
        "source_category": "public_pretraining_corpus",
        "license": "odc-by",
        "allowed_for_training": True,
    }


class StreamingLmBatchIteratorTests(unittest.TestCase):
    def test_iter_jsonl_texts_yields_approved_nonempty_texts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            jsonl_path = Path(temp_dir) / "sample.jsonl"
            write_jsonl(jsonl_path, [approved_record("alpha"), approved_record("   "), approved_record("beta")])

            texts = list(iter_jsonl_texts(jsonl_path))

        self.assertEqual(texts, ["alpha", "beta"])

    def test_iter_jsonl_texts_rejects_unapproved_training_record(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            jsonl_path = Path(temp_dir) / "sample.jsonl"
            blocked = approved_record("blocked")
            blocked["allowed_for_training"] = False
            write_jsonl(jsonl_path, [blocked])

            with self.assertRaisesRegex(ValueError, "not approved for training"):
                list(iter_jsonl_texts(jsonl_path))

    def test_iter_token_blocks_yields_lazy_overlapping_next_token_blocks_with_eos(self) -> None:
        blocks = iter_token_blocks(iter(["1 2 3", "4 5"]), FakeTokenizer(), sequence_length=3, eos_token_id=99)

        self.assertIs(iter(blocks), blocks)
        self.assertEqual(next(blocks), ([1, 2, 3], [2, 3, 99]))
        self.assertEqual(next(blocks), ([2, 3, 99], [3, 99, 4]))

    def test_iter_batches_yields_only_full_lazy_batches(self) -> None:
        block_iter = iter(
            [
                ([1, 2], [2, 3]),
                ([3, 4], [4, 5]),
                ([5, 6], [6, 7]),
            ]
        )
        batches = iter_batches(block_iter, batch_size=2)

        self.assertIs(iter(batches), batches)
        self.assertEqual(list(batches), [([[1, 2], [3, 4]], [[2, 3], [4, 5]])])

    def test_cycle_batches_restarts_factory_deterministically(self) -> None:
        first_batch = ([[1, 2]], [[2, 3]])
        second_batch = ([[3, 4]], [[4, 5]])

        def factory():
            return iter([first_batch, second_batch])

        self.assertEqual(
            list(cycle_batches(factory, max_batches=5)),
            [first_batch, second_batch, first_batch, second_batch, first_batch],
        )

    def test_streaming_first_batches_match_existing_sequence_utilities(self) -> None:
        token_ids = [1, 2, 3, 4, 5, 6, 7, 8]
        expected = batch_samples(make_next_token_samples(token_ids, sequence_length=3), batch_size=2)[:2]
        streaming = iter_batches(
            iter_token_blocks(iter(["1 2 3 4 5 6 7 8"]), FakeTokenizer(), sequence_length=3, eos_token_id=None),
            batch_size=2,
        )

        self.assertEqual([next(streaming), next(streaming)], expected)


if __name__ == "__main__":
    unittest.main()
