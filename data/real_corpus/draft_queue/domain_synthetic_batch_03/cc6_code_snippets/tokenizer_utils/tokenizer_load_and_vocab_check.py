# draft_status: candidate
# topic_id: COD-008
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC-6
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only

"""Tokenizer load and vocab check using a tiny fake tokenizer object."""

from dataclasses import dataclass


@dataclass
class FakeTokenizer:
    vocab_size: int
    pad_token_id: int
    eos_token_id: int


def summarize_tokenizer(tokenizer: FakeTokenizer) -> dict[str, int]:
    summary = {
        "vocab_size": tokenizer.vocab_size,
        "pad_token_id": tokenizer.pad_token_id,
        "eos_token_id": tokenizer.eos_token_id,
    }
    print(summary)
    assert tokenizer.vocab_size > max(tokenizer.pad_token_id, tokenizer.eos_token_id)
    return summary


if __name__ == "__main__":
    fake = FakeTokenizer(vocab_size=128, pad_token_id=0, eos_token_id=1)
    summarize_tokenizer(fake)
