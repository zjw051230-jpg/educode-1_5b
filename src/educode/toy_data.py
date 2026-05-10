from __future__ import annotations


def get_toy_corpus() -> list[str]:
    return [
        "hello world",
        "你好，世界",
        "12345 and punctuation!?,.;:",
        "Transformer models predict the next token.",
        "Python code: print('hello')",
        "Loss should decrease during training.",
        "CS336 is about language modeling from scratch.",
        "Emoji test 😊",
    ]


def join_corpus(corpus: list[str]) -> str:
    if not isinstance(corpus, list):
        raise TypeError("corpus must be a list[str]")
    if any(not isinstance(item, str) for item in corpus):
        raise TypeError("corpus must be a list[str]")
    return "\n".join(corpus)


def corpus_stats(text: str, token_ids: list[int]) -> dict:
    return {
        "num_characters": len(text),
        "num_bytes": len(text.encode("utf-8")),
        "num_tokens": len(token_ids),
        "unique_token_ids": len(set(token_ids)),
        "min_token_id": min(token_ids) if token_ids else None,
        "max_token_id": max(token_ids) if token_ids else None,
    }
