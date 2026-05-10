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
from educode.toy_data import corpus_stats, get_toy_corpus, join_corpus


def main() -> int:
    tokenizer = ByteTokenizer()
    corpus = get_toy_corpus()
    text = join_corpus(corpus)
    token_ids = tokenizer.encode(text)
    decoded = tokenizer.decode(token_ids)
    stats = corpus_stats(text, token_ids)

    print(f"number of corpus lines: {len(corpus)}")
    print(f"joined text preview: {text[:120]}")
    print(f"token count: {stats['num_tokens']}")
    print(f"min token id: {stats['min_token_id']}")
    print(f"max token id: {stats['max_token_id']}")
    print(f"unique token id count: {stats['unique_token_ids']}")
    print(f"round_trip_ok: {tokenizer.round_trip_ok(text)}")
    print(f"first 40 token ids: {token_ids[:40]}")
    print(f"decode preview: {decoded[:120]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
