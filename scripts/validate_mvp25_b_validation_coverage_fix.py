from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_PATH = PROJECT_ROOT / "scripts"
for path in (PROJECT_ROOT, SCRIPTS_PATH):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from run_a100_300m_fineweb_edu_10step_training import build_split_sampling_settings
from streaming_lm_batch_iterator import create_streaming_batch_iterator


class FakeEncoding:
    def __init__(self, ids: list[int]) -> None:
        self.ids = ids


class FakeTokenizer:
    def encode(self, text: str) -> FakeEncoding:
        return FakeEncoding([int(part) for part in text.split()])


def approved_record(text: str) -> dict[str, Any]:
    return {
        "text": text,
        "source_category": "public_pretraining_corpus",
        "license": "odc-by",
        "allowed_for_training": True,
    }


def write_fixture(path: Path) -> None:
    records = []
    for doc_index in range(12):
        start = doc_index * 100
        tokens = " ".join(str(start + offset) for offset in range(12))
        records.append(approved_record(tokens))
    path.write_text("".join(json.dumps(record) + "\n" for record in records), encoding="utf-8")


def run_validation() -> dict[str, Any]:
    config = {
        "run": {"seed": 336},
        "sampling": {
            "policy": "shuffle_buffer",
            "shuffle_seed": 1337,
            "shuffle_buffer_size": 4,
        },
        "validation_sampling": {
            "policy": "shuffle_buffer",
            "shuffle_seed": 7331,
            "shuffle_buffer_size": 4,
            "max_blocks_per_document": 1,
        },
    }
    blockers: list[str] = []

    with tempfile.TemporaryDirectory() as temp_dir:
        jsonl_path = Path(temp_dir) / "validation.jsonl"
        write_fixture(jsonl_path)
        val_settings = build_split_sampling_settings(config, split_name="val")
        batch_iter, stats = create_streaming_batch_iterator(
            split_name="val",
            split_path=jsonl_path,
            tokenizer=FakeTokenizer(),
            sequence_length=4,
            batch_size=2,
            required_batches=3,
            eos_token_id=None,
            **val_settings,
        )
        batches = []
        try:
            for _ in range(3):
                batches.append(next(batch_iter))
        finally:
            close = getattr(batch_iter, "close", None)
            if close is not None:
                close()

    probe = stats.to_dict()
    unique_doc_count = probe.get("unique_doc_count")
    batches_evaluated = len(batches)
    tokens_evaluated = batches_evaluated * 2 * 4
    val_sampling_policy = probe.get("sampling_policy")
    validation_prefix_only_risk = bool(val_sampling_policy == "sequential_prefix" or not isinstance(unique_doc_count, int) or unique_doc_count <= 1)

    if val_sampling_policy != "shuffle_buffer":
        blockers.append(f"val_sampling_policy expected shuffle_buffer, got {val_sampling_policy!r}")
    if probe.get("shuffle_seed") != 7331:
        blockers.append(f"val shuffle seed expected 7331, got {probe.get('shuffle_seed')!r}")
    if probe.get("shuffle_buffer_size") != 4:
        blockers.append(f"val shuffle buffer size expected 4, got {probe.get('shuffle_buffer_size')!r}")
    if unique_doc_count is None or unique_doc_count <= 1:
        blockers.append(f"validation_unique_doc_count must be greater than 1, got {unique_doc_count!r}")
    if batches_evaluated != 3:
        blockers.append(f"validation_batches_evaluated expected 3, got {batches_evaluated}")
    if tokens_evaluated != 24:
        blockers.append(f"validation_tokens_evaluated expected 24, got {tokens_evaluated}")
    if validation_prefix_only_risk:
        blockers.append("validation_prefix_only_risk should be false after the coverage fix")

    return {
        "validation_status": "passed" if not blockers else "failed",
        "validation_unique_doc_count": unique_doc_count,
        "validation_batches_evaluated": batches_evaluated,
        "validation_tokens_evaluated": tokens_evaluated,
        "val_sampling_policy": val_sampling_policy,
        "val_shuffle_seed": probe.get("shuffle_seed"),
        "val_shuffle_buffer_size": probe.get("shuffle_buffer_size"),
        "validation_prefix_only_risk": validation_prefix_only_risk,
        "blockers": blockers,
        "blocker_count": len(blockers),
    }


def main() -> int:
    result = run_validation()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["validation_status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
