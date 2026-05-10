from __future__ import annotations


def make_next_token_samples(token_ids: list[int], sequence_length: int) -> list[tuple[list[int], list[int]]]:
    if not isinstance(token_ids, list):
        raise TypeError("token_ids must be a list[int]")
    if any(not isinstance(token_id, int) for token_id in token_ids):
        raise TypeError("token_ids must be a list[int]")
    if not isinstance(sequence_length, int):
        raise TypeError("sequence_length must be an int")
    if sequence_length <= 0:
        raise ValueError("sequence_length must be greater than 0")

    num_samples = len(token_ids) - sequence_length
    if num_samples <= 0:
        return []

    samples: list[tuple[list[int], list[int]]] = []
    for i in range(num_samples):
        x = token_ids[i : i + sequence_length]
        y = token_ids[i + 1 : i + sequence_length + 1]
        if len(x) == sequence_length and len(y) == sequence_length:
            samples.append((x, y))

    return samples


def batch_samples(
    samples: list[tuple[list[int], list[int]]], batch_size: int
) -> list[tuple[list[list[int]], list[list[int]]]]:
    if not isinstance(samples, list):
        raise TypeError("samples must be a list")
    if not isinstance(batch_size, int):
        raise TypeError("batch_size must be an int")
    if batch_size <= 0:
        raise ValueError("batch_size must be greater than 0")

    normalized_samples: list[tuple[list[int], list[int]]] = []
    sequence_length: int | None = None

    for sample in samples:
        if not isinstance(sample, tuple) or len(sample) != 2:
            raise TypeError("each sample must be a tuple of (x, y)")

        x, y = sample
        if not isinstance(x, list) or not isinstance(y, list):
            raise TypeError("each sample must contain list[int] values")
        if any(not isinstance(token_id, int) for token_id in x):
            raise TypeError("x must be a list[int]")
        if any(not isinstance(token_id, int) for token_id in y):
            raise TypeError("y must be a list[int]")
        if len(x) != len(y):
            raise ValueError("x and y must have the same length")

        if sequence_length is None:
            sequence_length = len(x)
        elif len(x) != sequence_length:
            raise ValueError("all samples must have the same sequence length")

        normalized_samples.append((x, y))

    batches: list[tuple[list[list[int]], list[list[int]]]] = []
    for i in range(0, len(normalized_samples), batch_size):
        batch = normalized_samples[i : i + batch_size]
        if len(batch) != batch_size:
            continue

        batch_x = [x for x, _ in batch]
        batch_y = [y for _, y in batch]
        batches.append((batch_x, batch_y))

    return batches


def dataset_stats(
    samples: list[tuple[list[int], list[int]]],
    batches: list[tuple[list[list[int]], list[list[int]]]],
) -> dict:
    if not isinstance(samples, list):
        raise TypeError("samples must be a list")
    if not isinstance(batches, list):
        raise TypeError("batches must be a list")

    sequence_length = len(samples[0][0]) if samples else None
    batch_size = len(batches[0][0]) if batches else None
    first_x_preview = samples[0][0][:8] if samples else []
    first_y_preview = samples[0][1][:8] if samples else []

    return {
        "num_samples": len(samples),
        "num_batches": len(batches),
        "sequence_length": sequence_length,
        "batch_size": batch_size,
        "first_x_preview": first_x_preview,
        "first_y_preview": first_y_preview,
    }
