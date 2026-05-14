from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


def write_metric_row(path: Path, step: int, train_loss: float, val_loss: float | None) -> None:
    record = {
        "step": step,
        "train_loss": train_loss,
        "val_loss": val_loss,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False))
        handle.write("\n")


def main() -> None:
    output_path = Path("metrics_example.jsonl")
    write_metric_row(output_path, step=1, train_loss=6.2, val_loss=None)
    write_metric_row(output_path, step=10, train_loss=5.4, val_loss=7.1)


if __name__ == "__main__":
    main()
