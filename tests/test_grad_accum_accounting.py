import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.educode.grad_accum import training_tokens_accounting  # noqa: E402


class GradAccumAccountingTests(unittest.TestCase):
    def test_global_batch_and_tokens_seen(self):
        report = training_tokens_accounting(
            micro_batch_size=4,
            grad_accum_steps=8,
            sequence_length=1024,
            world_size=2,
            max_steps=10,
        )

        self.assertEqual(report["global_batch_size"], 64)
        self.assertEqual(report["tokens_per_optimizer_step"], 65536)
        self.assertEqual(report["tokens_seen"], 655360)

    def test_bad_accounting_config_rejected(self):
        with self.assertRaises(ValueError):
            training_tokens_accounting(0, 1, 1024, 1, 10)


if __name__ == "__main__":
    unittest.main()
