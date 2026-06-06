from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from educode.compression import CompressionPlan, summarize_compression_plan  # noqa: E402
from educode.distillation import (  # noqa: E402
    DistillationConfig,
    TeacherLogitsProvider,
    distillation_kl_loss,
    validate_logits_pair,
)


class DistillationLossTests(unittest.TestCase):
    def test_kl_loss_is_finite_on_synthetic_logits(self) -> None:
        config = DistillationConfig(temperature=2.0, alpha=0.7)
        student = [[1.0, 0.0, -1.0], [0.2, 0.1, 0.0]]
        teacher = [[1.5, 0.1, -0.8], [0.3, 0.2, -0.1]]

        loss = distillation_kl_loss(student, teacher, config)

        self.assertTrue(math.isfinite(loss))
        self.assertGreaterEqual(loss, 0.0)

    def test_bad_temperature_config_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            DistillationConfig(temperature=0.0)

    def test_teacher_student_shape_mismatch_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            validate_logits_pair([[1.0, 2.0]], [[1.0, 2.0, 3.0]])

    def test_teacher_logits_provider_is_interface_only(self) -> None:
        provider = TeacherLogitsProvider()

        with self.assertRaises(NotImplementedError):
            provider.logits_for_token_ids([1, 2, 3])

    def test_compression_plan_summary_is_metadata_only(self) -> None:
        plan = CompressionPlan(strategy="magnitude_pruning", target_sparsity=0.1, notes="future CPU/GPU audit")

        summary = summarize_compression_plan(plan)

        self.assertEqual(summary["strategy"], "magnitude_pruning")
        self.assertEqual(summary["target_sparsity"], 0.1)
        self.assertFalse(summary["model_mutated"])


if __name__ == "__main__":
    unittest.main()
