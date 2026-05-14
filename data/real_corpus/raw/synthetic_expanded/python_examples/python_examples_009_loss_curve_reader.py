from __future__ import annotations

import json
from pathlib import Path


def read_train_losses(path: Path) -> list[float]:
    losses: list[float] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            record = json.loads(line)
            value = record.get("train_loss")
            if isinstance(value, (int, float)):
                losses.append(float(value))
    return losses


def summarize_losses(losses: list[float]) -> dict[str, float]:
    return {
        "first": losses[0],
        "final": losses[-1],
        "min": min(losses),
        "max": max(losses),
    }


def main() -> None:
    demo_path = Path("metrics_example.jsonl")
    if demo_path.exists():
        print(summarize_losses(read_train_losses(demo_path)))


if __name__ == "__main__":
    main()
