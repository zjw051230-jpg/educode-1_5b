import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.plan_distributed_launch import (  # noqa: E402
    LaunchPlan,
    build_launch_command,
    check_fsdp_zero_feasibility,
)


class DistributedLaunchPlannerTests(unittest.TestCase):
    def test_generated_torchrun_command_is_string_only(self):
        plan = LaunchPlan(strategy="fsdp", nodes=1, gpus_per_node=2, config_path="config.json")
        command = build_launch_command(plan)

        self.assertIsInstance(command, str)
        self.assertIn("torchrun", command)
        self.assertIn("--nproc_per_node 2", command)

    def test_invalid_strategy_and_zero_stage_rejected(self):
        with self.assertRaises(ValueError):
            LaunchPlan(strategy="unknown", nodes=1, gpus_per_node=1, config_path="x")
        with self.assertRaises(ValueError):
            LaunchPlan(strategy="zero", nodes=1, gpus_per_node=2, config_path="x", zero_stage=4)

    def test_tp_sp_incompatibility_rejected(self):
        with self.assertRaises(ValueError):
            LaunchPlan(
                strategy="megatron",
                nodes=1,
                gpus_per_node=4,
                config_path="x",
                tensor_parallel_size=1,
                sequence_parallel=True,
            )

    def test_feasibility_checker_reports_no_execution(self):
        report = check_fsdp_zero_feasibility("zero", zero_stage=2, world_size=4)

        self.assertEqual(report["status"], "feasible_with_gate")
        self.assertFalse(report["command_executed"])
        self.assertTrue(report["future_gpu_modal_gate_required"])


if __name__ == "__main__":
    unittest.main()
