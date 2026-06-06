import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.educode.distributed_config import DistributedConfig  # noqa: E402


class DistributedConfigTests(unittest.TestCase):
    def test_single_gpu_config_valid(self):
        config = DistributedConfig(strategy="single_gpu", world_size=1)

        self.assertEqual(config.validate()["status"], "valid")

    def test_experimental_strategies_require_ack(self):
        with self.assertRaises(ValueError):
            DistributedConfig(strategy="fsdp", world_size=2)

        config = DistributedConfig(
            strategy="zero", world_size=2, zero_stage=2, experimental_ack=True
        )
        self.assertEqual(config.validate()["status"], "valid")

    def test_parallelism_bad_config_rejected(self):
        with self.assertRaises(ValueError):
            DistributedConfig(strategy="single_gpu", world_size=2)
        with self.assertRaises(ValueError):
            DistributedConfig(
                strategy="tensor_parallel",
                world_size=4,
                tensor_parallel_size=3,
                experimental_ack=True,
            )
        with self.assertRaises(ValueError):
            DistributedConfig(
                strategy="single_gpu",
                world_size=1,
                sequence_parallel=True,
            )


if __name__ == "__main__":
    unittest.main()
