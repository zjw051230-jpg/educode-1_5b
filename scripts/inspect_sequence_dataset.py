from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = PROJECT_ROOT / "src"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from educode.byte_tokenizer import ByteTokenizer
from educode.sequence_dataset import batch_samples, dataset_stats, make_next_token_samples
from educode.toy_data import get_toy_corpus, join_corpus


def safe_decode(token_ids: list[int]) -> str:
    return bytes(token_ids).decode("utf-8", errors="replace")


def main() -> int:
    tokenizer = ByteTokenizer()
    text = join_corpus(get_toy_corpus())
    token_ids = tokenizer.encode(text)

    sequence_length = 16
    batch_size = 4

    samples = make_next_token_samples(token_ids, sequence_length)
    batches = batch_samples(samples, batch_size)
    stats = dataset_stats(samples, batches)

    first_x, first_y = samples[0] if samples else ([], [])
    first_batch_x, first_batch_y = batches[0] if batches else ([], [])

    print(f"token count: {len(token_ids)}")
    print(f"sequence_length: {sequence_length}")
    print(f"num_samples: {stats['num_samples']}")
    print(f"batch_size: {batch_size}")
    print(f"num_batches: {stats['num_batches']}")
    print(f"first x: {first_x}")
    print(f"first y: {first_y}")
    print(f"first x decoded: {safe_decode(first_x)}")
    print(f"first y decoded: {safe_decode(first_y)}")
    print(f"single x length: {len(first_x)}")
    print(f"single y length: {len(first_y)}")
    print(f"batch_x size: {len(first_batch_x)}")
    print(f"batch_y size: {len(first_batch_y)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
