from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from statistics import mean
from typing import Iterable


@dataclass(frozen=True)
class LossDiagnosticReport:
    row_count: int
    losses_all_finite: bool
    non_finite_steps: list[int]
    spike_steps: list[int]
    final_train_loss: float | None
    min_train_loss: float | None
    max_train_loss: float | None
    mean_tokens_per_sec: float | None
    divergence_warning: bool
    validation_rows: int
    final_validation_loss: float | None

    def to_dict(self) -> dict:
        return asdict(self)


def read_metrics_jsonl(path: Path) -> list[dict]:
    rows = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        row = json.loads(line)
        if not isinstance(row, dict):
            raise ValueError(f"metrics row {line_number} is not an object")
        rows.append(row)
    return rows


def _train_loss(row: dict) -> float | None:
    value = row.get("train_loss")
    return value if isinstance(value, (int, float)) else None


def _step(row: dict, fallback: int) -> int:
    value = row.get("step")
    return int(value) if isinstance(value, int) else fallback


def rolling_average(values: Iterable[float], window: int) -> list[float]:
    if window <= 0:
        raise ValueError("window must be positive")
    values = list(values)
    averages = []
    for index in range(len(values)):
        start = max(0, index + 1 - window)
        averages.append(mean(values[start : index + 1]))
    return averages


def detect_loss_spikes(losses: Iterable[float], threshold_ratio: float = 1.5) -> list[int]:
    if threshold_ratio <= 1.0:
        raise ValueError("threshold_ratio must be greater than 1.0")
    losses = list(losses)
    spikes = []
    for index in range(1, len(losses)):
        prev = losses[index - 1]
        current = losses[index]
        if math.isfinite(prev) and math.isfinite(current) and prev > 0:
            if current / prev >= threshold_ratio:
                spikes.append(index)
    return spikes


def diagnose_metrics(
    metrics_rows: list[dict],
    validation_rows: list[dict] | None = None,
    spike_threshold_ratio: float = 1.5,
) -> LossDiagnosticReport:
    validation_rows = validation_rows or []
    train_losses = [_train_loss(row) for row in metrics_rows]
    finite_train_losses = [
        value for value in train_losses if isinstance(value, (int, float)) and math.isfinite(value)
    ]
    non_finite_steps = [
        _step(row, index + 1)
        for index, (row, value) in enumerate(zip(metrics_rows, train_losses))
        if isinstance(value, (int, float)) and not math.isfinite(value)
    ]
    tokens_per_sec = [
        row["tokens_per_sec"]
        for row in metrics_rows
        if isinstance(row.get("tokens_per_sec"), (int, float))
        and math.isfinite(row["tokens_per_sec"])
    ]
    validation_losses = [
        row["val_loss"]
        for row in validation_rows
        if isinstance(row.get("val_loss"), (int, float)) and math.isfinite(row["val_loss"])
    ]
    final_train_loss = finite_train_losses[-1] if finite_train_losses else None
    final_validation_loss = validation_losses[-1] if validation_losses else None
    divergence_warning = (
        final_train_loss is not None
        and final_validation_loss is not None
        and final_validation_loss > final_train_loss * 2.0
    )

    return LossDiagnosticReport(
        row_count=len(metrics_rows),
        losses_all_finite=not non_finite_steps,
        non_finite_steps=non_finite_steps,
        spike_steps=detect_loss_spikes(finite_train_losses, spike_threshold_ratio),
        final_train_loss=final_train_loss,
        min_train_loss=min(finite_train_losses) if finite_train_losses else None,
        max_train_loss=max(finite_train_losses) if finite_train_losses else None,
        mean_tokens_per_sec=mean(tokens_per_sec) if tokens_per_sec else None,
        divergence_warning=divergence_warning,
        validation_rows=len(validation_rows),
        final_validation_loss=final_validation_loss,
    )
