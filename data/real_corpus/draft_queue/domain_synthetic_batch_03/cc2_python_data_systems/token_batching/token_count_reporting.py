# draft_status: candidate
# topic_id: PDS-011
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC2
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only

from collections.abc import Iterable


def count_tokens_per_example(batch: Iterable[list[int]]) -> dict[str, float]:
    lengths = [len(example) for example in batch]
    if not lengths:
        return {"count": 0.0, "min": 0.0, "max": 0.0, "mean": 0.0}
    return {
        "count": float(len(lengths)),
        "min": float(min(lengths)),
        "max": float(max(lengths)),
        "mean": sum(lengths) / len(lengths),
    }


def main() -> None:
    batch = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
    stats = count_tokens_per_example(batch)
    for key, value in stats.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
