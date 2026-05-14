def training_loop_outline(max_steps: int) -> None:
    print("step | action")
    for step in range(1, max_steps + 1):
        print(f"{step} | load batch -> forward -> loss -> backward -> optimizer step")


if __name__ == "__main__":
    print("Synthetic training loop outline")
    training_loop_outline(max_steps=3)
    print("This file is a teaching example only.")
    print("It does not allocate a model, optimizer, or GPU tensors.")
