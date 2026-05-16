# draft_status: candidate
# topic_id: COD-010
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC-6
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only

"""Special token listing example for tokenizer smoke review."""


def list_special_tokens(token_map: dict[str, int]) -> list[tuple[str, int]]:
    ordered = sorted(token_map.items(), key=lambda item: item[1])
    for name, token_id in ordered:
        print(f"{name} -> {token_id}")
    return ordered


if __name__ == "__main__":
    special_tokens = {
        "<pad>": 0,
        "<eos>": 1,
        "<bos>": 2,
        "<unk>": 3,
    }
    listed = list_special_tokens(special_tokens)
    assert listed[0] == ("<pad>", 0)
