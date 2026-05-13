def next_token_demo(tokens: list[str]) -> str:
    if not tokens:
        return "<empty>"
    return f"predict_after:{tokens[-1]}"


def describe_training_step(step: int, loss: float) -> str:
    return f"step={step} loss={loss:.4f}"


if __name__ == "__main__":
    demo_tokens = ["hello", "world"]
    print(next_token_demo(demo_tokens))
    print(describe_training_step(3, 1.2345))
