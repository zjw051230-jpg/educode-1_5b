from __future__ import annotations

from pathlib import Path
import sys

from tokenizers import Tokenizer

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TOKENIZER_PATH = PROJECT_ROOT / "tokenizers" / "educode_bpe_toy_512" / "tokenizer.json"
SAMPLES = [
    "hello world",
    "你好，世界",
    "Python code: print('hello')",
    "Transformer models predict the next token.",
    "loss = F.cross_entropy(logits, targets)",
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

    print("Inspection results:")
    for text in SAMPLES:
        encoding = tokenizer.encode(text)
        decoded = tokenizer.decode(encoding.ids)
        print("---")
        print(f"input text: {text}")
        print(f"token ids: {encoding.ids}")
        print(f"tokens: {encoding.tokens}")
        print(f"decoded text: {decoded}")
        print(f"round_trip_exact: {decoded == text}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
