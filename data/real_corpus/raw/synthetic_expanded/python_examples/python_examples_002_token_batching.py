def batch_tokens(token_ids: list[int], context_length: int) -> list[list[int]]:
    batches: list[list[int]] = []
    for start in range(0, len(token_ids) - context_length + 1, context_length):
        window = token_ids[start : start + context_length]
        if len(window) == context_length:
            batches.append(window)
    return batches


if __name__ == "__main__":
    fake_tokens = list(range(32))
    windows = batch_tokens(fake_tokens, context_length=8)
    print("Synthetic batching example")
    print(f"window count: {len(windows)}")
    print(f"first window: {windows[0]}")

# This example shows fixed-size slicing only.
# It does not run training or touch model code.
