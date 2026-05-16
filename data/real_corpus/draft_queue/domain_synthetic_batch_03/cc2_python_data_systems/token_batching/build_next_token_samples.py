# draft_status: candidate
# topic_id: PDS-008
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC2
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only

from typing import Iterable


def build_next_token_samples(token_ids: Iterable[int], block_size: int) -> list[tuple[list[int], list[int]]]:
    tokens = list(token_ids)
    if block_size < 2:
        raise ValueError("block_size must be at least 2")
    samples: list[tuple[list[int], list[int]]] = []
    step = block_size
    for start in range(0, len(tokens) - block_size, step):
        window = tokens[start : start + block_size + 1]
        if len(window) < block_size + 1:
            continue
        inputs = window[:-1]
        targets = window[1:]
        samples.append((inputs, targets))
    return samples


def main() -> None:
    tokens = [10, 11, 12, 13, 14, 15, 16]
    for inputs, targets in build_next_token_samples(tokens, block_size=3):
        print("inputs=", inputs, "targets=", targets)


if __name__ == "__main__":
    main()
