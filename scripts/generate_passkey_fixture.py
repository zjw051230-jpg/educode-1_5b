from __future__ import annotations

import argparse
import json
import random


def make_passkey_example(*, prefix_tokens: int = 32, suffix_tokens: int = 32, seed: int = 1337) -> dict[str, object]:
    if prefix_tokens < 0 or suffix_tokens < 0:
        raise ValueError("prefix_tokens and suffix_tokens must be non-negative")
    rng = random.Random(seed)
    passkey = f"{rng.randrange(0, 999999):06d}"
    prefix = " ".join(f"filler{idx}" for idx in range(prefix_tokens))
    suffix = " ".join(f"context{idx}" for idx in range(suffix_tokens))
    prompt = f"{prefix} The pass key is {passkey}. {suffix} What is the pass key?"
    return {
        "prompt": prompt.strip(),
        "answer": passkey,
        "prefix_tokens": prefix_tokens,
        "suffix_tokens": suffix_tokens,
        "task": "passkey_retrieval_synthetic_fixture",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a tiny synthetic passkey retrieval fixture.")
    parser.add_argument("--prefix-tokens", type=int, default=32)
    parser.add_argument("--suffix-tokens", type=int, default=32)
    parser.add_argument("--seed", type=int, default=1337)
    args = parser.parse_args()
    print(json.dumps(make_passkey_example(prefix_tokens=args.prefix_tokens, suffix_tokens=args.suffix_tokens, seed=args.seed), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
