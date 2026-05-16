# draft_status: candidate
# topic_id: COD-009
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC-6
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only

"""Encode/decode roundtrip example with a tiny hand-built vocabulary."""


class TinyTokenizer:
    def __init__(self) -> None:
        self.token_to_id = {"hello": 0, "world": 1, "<unk>": 2}
        self.id_to_token = {index: token for token, index in self.token_to_id.items()}

    def encode(self, text: str) -> list[int]:
        return [self.token_to_id.get(piece, self.token_to_id["<unk>"]) for piece in text.split()]

    def decode(self, token_ids: list[int]) -> str:
        return " ".join(self.id_to_token.get(token_id, "<unk>") for token_id in token_ids)


def main() -> None:
    tokenizer = TinyTokenizer()
    token_ids = tokenizer.encode("hello world unknown")
    decoded = tokenizer.decode(token_ids)

    print(f"encoded: {token_ids}")
    print(f"decoded: {decoded}")
    assert token_ids == [0, 1, 2]
    assert decoded == "hello world <unk>"


if __name__ == "__main__":
    main()
