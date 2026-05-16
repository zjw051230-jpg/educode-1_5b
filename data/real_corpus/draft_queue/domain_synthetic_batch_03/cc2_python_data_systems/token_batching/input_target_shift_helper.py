# draft_status: candidate
# topic_id: PDS-014
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC2
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only


def shift_for_next_token(sequence: list[int]) -> tuple[list[int], list[int]]:
    if len(sequence) < 2:
        raise ValueError("sequence must contain at least two tokens")
    inputs = sequence[:-1]
    targets = sequence[1:]
    return inputs, targets


def pretty_print_shift(sequence: list[int]) -> None:
    inputs, targets = shift_for_next_token(sequence)
    print("sequence:", sequence)
    print("inputs:  ", inputs)
    print("targets: ", targets)


def main() -> None:
    pretty_print_shift([101, 205, 309, 412])


if __name__ == "__main__":
    main()
