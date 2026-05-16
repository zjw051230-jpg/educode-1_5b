# draft_status: candidate
# topic_id: BIL-006
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC5
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only

from typing import Callable, Iterable, List, Dict


def count_token_lengths(samples: Iterable[str], encode: Callable[[str], List[int]]) -> List[Dict[str, int]]:
    """Return simple token-count diagnostics for bilingual text samples."""
    rows = []
    for idx, text in enumerate(samples):
        token_ids = encode(text)
        rows.append(
            {
                "sample_index": idx,
                "char_count": len(text),
                "token_count": len(token_ids),
                "has_cjk": int(any("一" <= ch <= "鿿" for ch in text)),
                "has_ascii": int(any(ord(ch) < 128 for ch in text)),
            }
        )
    return rows


if __name__ == "__main__":
    demo_samples = [
        "解释 tokenizer merge 的作用。",
        "Explain why validation loss may rise.",
        "中英混合 sample for A100 profiling.",
    ]

    fake_encode = lambda text: [ord(ch) % 97 for ch in text if ch.strip()]

    for row in count_token_lengths(demo_samples, fake_encode):
        print(row)

# Educational notes:
# - This helper compares character count and token count without assuming a real tokenizer dependency.
# - In draft review, large swings across similar bilingual prompts can signal spacing or encoding inconsistencies.
# - The demo encoder is synthetic and only illustrates the logging pattern.
