from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class DistillationConfig:
    temperature: float = 2.0
    alpha: float = 0.5

    def __post_init__(self) -> None:
        if self.temperature <= 0:
            raise ValueError("temperature must be positive")
        if not 0.0 <= self.alpha <= 1.0:
            raise ValueError("alpha must be between 0 and 1")


class TeacherLogitsProvider:
    def logits_for_token_ids(self, token_ids: Sequence[int]) -> list[list[float]]:
        raise NotImplementedError("teacher checkpoint integration is intentionally not implemented")


def validate_logits_pair(
    student_logits: Sequence[Sequence[float]],
    teacher_logits: Sequence[Sequence[float]],
) -> None:
    if len(student_logits) != len(teacher_logits):
        raise ValueError("student and teacher batch sizes must match")
    if not student_logits:
        raise ValueError("logits must be non-empty")
    for row_index, (student_row, teacher_row) in enumerate(zip(student_logits, teacher_logits)):
        if len(student_row) != len(teacher_row):
            raise ValueError(f"logit width mismatch at row {row_index}")
        if not student_row:
            raise ValueError(f"logit row {row_index} must be non-empty")


def log_softmax(row: Sequence[float], temperature: float) -> list[float]:
    scaled = [float(value) / temperature for value in row]
    max_value = max(scaled)
    log_denominator = max_value + math.log(sum(math.exp(value - max_value) for value in scaled))
    return [value - log_denominator for value in scaled]


def distillation_kl_loss(
    student_logits: Sequence[Sequence[float]],
    teacher_logits: Sequence[Sequence[float]],
    config: DistillationConfig | None = None,
) -> float:
    config = config or DistillationConfig()
    validate_logits_pair(student_logits, teacher_logits)

    total = 0.0
    for student_row, teacher_row in zip(student_logits, teacher_logits):
        student_log_probs = log_softmax(student_row, config.temperature)
        teacher_log_probs = log_softmax(teacher_row, config.temperature)
        row_kl = 0.0
        for teacher_log_prob, student_log_prob in zip(teacher_log_probs, student_log_probs):
            teacher_prob = math.exp(teacher_log_prob)
            row_kl += teacher_prob * (teacher_log_prob - student_log_prob)
        total += row_kl
    return config.alpha * (config.temperature**2) * total / len(student_logits)
