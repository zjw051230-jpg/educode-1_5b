from __future__ import annotations

import random


def assign_splits(document_ids: list[str], seed: int = 1337) -> dict[str, str]:
    rng = random.Random(seed)
    shuffled = list(document_ids)
    rng.shuffle(shuffled)

    val_count = max(1, round(len(shuffled) * 0.1))
    val_ids = set(shuffled[:val_count])

    result: dict[str, str] = {}
    for document_id in shuffled:
        result[document_id] = "val" if document_id in val_ids else "train"
    return result


def main() -> None:
    ids = [f"doc_{index:03d}" for index in range(1, 11)]
    print(assign_splits(ids))


if __name__ == "__main__":
    main()
