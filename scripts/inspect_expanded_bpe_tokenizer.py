from __future__ import annotations

import sys
from pathlib import Path

from tokenizers import Tokenizer

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TOKENIZER_PATH = PROJECT_ROOT / "tokenizers" / "educode_bpe_expanded_8k" / "tokenizer.json"
SAMPLES = [
    "hello world",
    "你好，世界",
    "Python code: print('hello')",
    "Transformer models predict the next token.",
    "loss = F.cross_entropy(logits, targets)",
    "A100 2.15B seq512 optimizer profile",
    "Emoji test 😊",
]
SPECIAL_TOKENS = ["<pad>", "<bos>", "<eos>", "<unk>"]


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

    if not TOKENIZER_PATH.exists():
        print(f"Missing tokenizer artifact: {TOKENIZER_PATH}")
        return 1

    tokenizer = Tokenizer.from_file(str(TOKENIZER_PATH))
    print(f"Tokenizer path: {TOKENIZER_PATH}")
    print(f"Tokenizer vocab size: {tokenizer.get_vocab_size()}")
    print("Special token ids:")
    for token in SPECIAL_TOKENS:
        print(f"- {token}: {tokenizer.token_to_id(token)}")

    all_round_trip_exact = True
    failed_inputs: list[str] = []

    print("Inspection results:")
    for text in SAMPLES:
        encoding = tokenizer.encode(text)
        decoded = tokenizer.decode(encoding.ids)
        round_trip_exact = decoded == text
        if not round_trip_exact:
            all_round_trip_exact = False
            failed_inputs.append(text)

        print("---")
        print(f"input: {text}")
        print(f"token ids: {encoding.ids}")
        print(f"tokens: {encoding.tokens}")
        print(f"decoded: {decoded}")
        print(f"round_trip_exact: {round_trip_exact}")

    print("---")
    print(f"all_round_trip_exact: {all_round_trip_exact}")
    print(f"failed_input_count: {len(failed_inputs)}")
    if failed_inputs:
        print("failed_inputs:")
        for text in failed_inputs:
            print(f"- {text}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
