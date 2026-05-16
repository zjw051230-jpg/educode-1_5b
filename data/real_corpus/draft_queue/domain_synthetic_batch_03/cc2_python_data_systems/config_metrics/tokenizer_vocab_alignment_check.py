# draft_status: candidate
# topic_id: PDS-016
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC2
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only


def check_vocab_alignment(tokenizer_vocab_size: int, model_vocab_size: int) -> str:
    if tokenizer_vocab_size <= 0 or model_vocab_size <= 0:
        raise ValueError("vocab sizes must be positive")
    if tokenizer_vocab_size == model_vocab_size:
        return "aligned"
    difference = model_vocab_size - tokenizer_vocab_size
    if difference > 0:
        return f"model vocab is larger by {difference}"
    return f"tokenizer vocab is larger by {abs(difference)}"


def main() -> None:
    result = check_vocab_alignment(tokenizer_vocab_size=32000, model_vocab_size=32000)
    print(result)


if __name__ == "__main__":
    main()
