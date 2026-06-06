import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.educode.distributed_config import DistributedConfig  # noqa: E402
from src.educode.memory_estimator import estimate_training_memory_gib  # noqa: E402


class MemoryEstimatorTests(unittest.TestCase):
    def test_memory_estimator_is_finite_and_deterministic(self):
        config = DistributedConfig(strategy="single_gpu", world_size=1)

        first = estimate_training_memory_gib(
            parameter_count=300_000_000,
            batch_size=4,
            sequence_length=1024,
            hidden_size=1024,
            num_layers=24,
            dtype_bytes=2,
            distributed=config,
        )
        second = estimate_training_memory_gib(
            parameter_count=300_000_000,
            batch_size=4,
            sequence_length=1024,
            hidden_size=1024,
            num_layers=24,
            dtype_bytes=2,
            distributed=config,
        )

        self.assertEqual(first, second)
        self.assertGreater(first["total_estimated_gib"], 0)
        self.assertGreater(first["optimizer_state_gib"], first["parameter_gib"])

    def test_fsdp_reduces_parameter_shard_estimate(self):
        single = estimate_training_memory_gib(
            100_000_000, 2, 512, 768, 12, 2, DistributedConfig()
        )
        fsdp = estimate_training_memory_gib(
            100_000_000,
            2,
            512,
            768,
            12,
            2,
            DistributedConfig(strategy="fsdp", world_size=4, experimental_ack=True),
        )

        self.assertLess(fsdp["parameter_gib"], single["parameter_gib"])


if __name__ == "__main__":
    unittest.main()
