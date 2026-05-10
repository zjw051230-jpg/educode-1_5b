from __future__ import annotations


class ByteTokenizer:
    def __init__(self) -> None:
        self.vocab_size = 256

    def encode(self, text: str) -> list[int]:
        if not isinstance(text, str):
            raise TypeError("text must be a str")
        return list(text.encode("utf-8"))

    def decode(self, token_ids: list[int]) -> str:
        if not isinstance(token_ids, list):
            raise TypeError("token_ids must be a list")

        for token_id in token_ids:
            if not isinstance(token_id, int):
                raise TypeError("each token id must be an int")
            if token_id < 0 or token_id > 255:
                raise ValueError("each token id must be in range 0-255")

        return bytes(token_ids).decode("utf-8")

    def round_trip_ok(self, text: str) -> bool:
        return self.decode(self.encode(text)) == text
