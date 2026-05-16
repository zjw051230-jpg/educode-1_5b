# draft_status: candidate
# topic_id: BIL-010
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC5
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only

from typing import Dict, List


def make_bilingual_example(question_zh: str, answer_zh: str, question_en: str, answer_en: str) -> Dict[str, List[str]]:
    """Build a tiny paired bilingual QA schema for educational drafts."""
    return {
        "question": [question_zh, question_en],
        "answer": [answer_zh, answer_en],
        "languages": ["zh", "en"],
    }


def validate_lengths(example: Dict[str, List[str]]) -> Dict[str, int]:
    return {
        "question_items": len(example["question"]),
        "answer_items": len(example["answer"]),
        "language_items": len(example["languages"]),
    }


if __name__ == "__main__":
    example = make_bilingual_example(
        "为什么验证 loss 会抖动？",
        "因为小验证集和短窗口会放大波动。",
        "Why can validation loss wobble?",
        "Small validation sets and short windows magnify noise.",
    )
    print(example)
    print(validate_lengths(example))

# Educational notes:
# - The schema stays intentionally small so a reviewer can inspect alignment by eye.
# - Paired fields are useful when you want Chinese and English to discuss the same concept without forcing identical wording.
# - This is a draft example schema, not a dataset contract for production training.
