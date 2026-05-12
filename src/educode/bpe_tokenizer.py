from __future__ import annotations

from pathlib import Path

from tokenizers import Tokenizer


class BPETokenizer:
    def __init__(self, tokenizer_path: str | Path) -> None:
        path = Path(tokenizer_path)
        if not path.exists():
            raise FileNotFoundError(f"tokenizer file not found: {path}")

        self.tokenizer_path = path
        self.tokenizer = Tokenizer.from_file(str(path))
        self.vocab_size = self.tokenizer.get_vocab_size()
        self.pad_token_id = self.tokenizer.token_to_id("<pad>")
        self.bos_token_id = self.tokenizer.token_to_id("<bos>")
        self.eos_token_id = self.tokenizer.token_to_id("<eos>")
        self.unk_token_id = self.tokenizer.token_to_id("<unk>")

    def encode(self, text: str) -> list[int]:
        if not isinstance(text, str):
            raise TypeError("text must be a str")
        return self.tokenizer.encode(text).ids

    def decode(self, token_ids: list[int]) -> str:
        if not isinstance(token_ids, list):
            raise TypeError("token_ids must be a list[int]")
        if any(not isinstance(token_id, int) for token_id in token_ids):
            raise TypeError("token_ids must be a list[int]")
        if any(token_id < 0 for token_id in token_ids):
            raise ValueError("token_ids must be non-negative")
        return self.tokenizer.decode(token_ids)

    def round_trip_ok(self, text: str) -> bool:
        return self.decode(self.encode(text)) == text

    def get_vocab_size(self) -> int:
        return self.vocab_size
