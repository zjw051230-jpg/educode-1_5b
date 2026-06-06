from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from src.educode.eval_metrics import exact_match_score, multiple_choice_accuracy


@dataclass(frozen=True)
class BenchmarkTask:
    name: str
    task_type: str
    examples: list[dict]

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("task name must be non-empty")
        if self.task_type not in {"exact_match", "multiple_choice", "perplexity"}:
            raise ValueError("unsupported task_type")
        if not self.examples:
            raise ValueError("examples must be non-empty")


class EvaluatorRegistry:
    def __init__(self) -> None:
        self._evaluators: dict[str, Callable] = {}

    def register(self, name: str, evaluator: Callable) -> None:
        if not name.strip():
            raise ValueError("evaluator name must be non-empty")
        self._evaluators[name] = evaluator

    def get(self, name: str) -> Callable:
        if name not in self._evaluators:
            raise KeyError(name)
        return self._evaluators[name]

    def names(self) -> list[str]:
        return sorted(self._evaluators)


def run_benchmark_task(task: BenchmarkTask) -> dict:
    scores = []
    for example in task.examples:
        if task.task_type == "exact_match":
            scores.append(exact_match_score(example["prediction"], example["target"]))
        elif task.task_type == "multiple_choice":
            scores.append(multiple_choice_accuracy(example["scores"], example["target_index"]))
        else:
            if "perplexity" not in example:
                raise ValueError("perplexity task examples require precomputed perplexity")
            scores.append(float(example["perplexity"]))
    aggregate = sum(scores) / len(scores)
    return {
        "task_name": task.name,
        "task_type": task.task_type,
        "example_count": len(task.examples),
        "score": aggregate,
        "checkpoint_loaded": False,
        "modal_gpu_training_run": False,
    }
