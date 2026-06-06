import sys
import unittest
from pathlib import Path

import torch

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.educode.eval_benchmarks import (  # noqa: E402
    BenchmarkTask,
    EvaluatorRegistry,
    run_benchmark_task,
)
from src.educode.eval_metrics import exact_match_score, perplexity_from_logits  # noqa: E402


class EvalBenchmarkHarnessTests(unittest.TestCase):
    def test_synthetic_exact_match_task(self):
        task = BenchmarkTask(
            name="toy-em",
            task_type="exact_match",
            examples=[{"prediction": "Answer", "target": "answer"}],
        )
        result = run_benchmark_task(task)

        self.assertEqual(result["score"], 1.0)
        self.assertEqual(result["example_count"], 1)

    def test_synthetic_multiple_choice_task(self):
        task = BenchmarkTask(
            name="toy-mc",
            task_type="multiple_choice",
            examples=[{"scores": [0.1, 0.9], "target_index": 1}],
        )
        result = run_benchmark_task(task)

        self.assertEqual(result["score"], 1.0)

    def test_perplexity_placeholder_finite(self):
        logits = torch.tensor([[[2.0, 0.1], [0.2, 2.1]]])
        targets = torch.tensor([[0, 1]])

        value = perplexity_from_logits(logits, targets)

        self.assertGreater(value, 0)
        self.assertTrue(torch.isfinite(torch.tensor(value)))

    def test_bad_task_config_rejected_and_registry(self):
        with self.assertRaises(ValueError):
            BenchmarkTask(name="", task_type="exact_match", examples=[])

        registry = EvaluatorRegistry()
        registry.register("exact_match", exact_match_score)
        self.assertIn("exact_match", registry.names())


if __name__ == "__main__":
    unittest.main()
