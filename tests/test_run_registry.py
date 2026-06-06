from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from educode.run_registry import (  # noqa: E402
    RunRecord,
    append_record,
    import_summary_file,
    load_registry,
    query_records,
)


class RunRegistryTests(unittest.TestCase):
    def sample_summary_path(self, root: Path) -> Path:
        summary_path = root / "experiment" / "results_imported_modal_streaming" / "summary.json"
        summary_path.parent.mkdir(parents=True)
        summary_path.write_text(
            json.dumps(
                {
                    "run_id": "run-001",
                    "run_name": "fineweb_edu_5gb_300m_50step_public16k_seq1024_sdpa_profile",
                    "config_path": "configs/a100/fineweb_edu_5gb_300m_50step_public16k_seq1024_sdpa_profile.json",
                    "output_dir": "experiments/a100/fineweb_edu_5gb_300m_50step_public16k_seq1024_sdpa_profile",
                    "success": True,
                    "max_steps": 50,
                    "batch_size": 4,
                    "sequence_length": 1024,
                    "gradient_accumulation_steps": 4,
                    "runtime_device": "cuda",
                    "runtime_dtype": "bf16",
                    "data_loading_mode": "streaming",
                    "final_train_loss": 1.45032,
                    "final_val_loss": 9.930368,
                    "approximate_tokens_per_sec": 41430.475003,
                    "last_gpu_memory_allocated_gib": 2.649026,
                    "last_gpu_memory_reserved_gib": 8.412109,
                    "declared_model_features": {"attention_backend": "sdpa"},
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        return summary_path

    def test_imports_existing_summary_metadata_without_mutating_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            summary_path = self.sample_summary_path(root)
            before = summary_path.read_text(encoding="utf-8")

            record = import_summary_file(summary_path, repo_root=root)

            self.assertEqual(record.run_id, "run-001")
            self.assertEqual(record.context_length, 1024)
            self.assertEqual(record.batch_size, 4)
            self.assertEqual(record.attention_backend, "sdpa")
            self.assertEqual(record.run_type, "profile")
            self.assertEqual(summary_path.read_text(encoding="utf-8"), before)

    def test_registry_can_append_load_and_query_records(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            registry_path = Path(temp_dir) / "run_registry.jsonl"
            profile = RunRecord(
                run_id="profile-001",
                run_name="seq1024_sdpa_profile",
                run_type="profile",
                artifact_dir="experiments/a100/profile",
                summary_path="experiments/a100/profile/results_imported_modal_streaming/summary.json",
                success=True,
                context_length=1024,
                batch_size=4,
                grad_accum=4,
                max_steps=50,
                attention_backend="sdpa",
            )
            training = RunRecord(
                run_id="train-001",
                run_name="seq512_train",
                run_type="training",
                artifact_dir="experiments/a100/train",
                summary_path="experiments/a100/train/results_imported_modal_streaming/summary.json",
                success=True,
                context_length=512,
                batch_size=8,
                grad_accum=4,
                max_steps=3000,
                attention_backend="sdpa",
            )

            append_record(registry_path, profile)
            append_record(registry_path, training)
            records = load_registry(registry_path)
            matches = query_records(records, run_type="profile", attention_backend="sdpa", context_length=1024)

            self.assertEqual(len(records), 2)
            self.assertEqual([record.run_id for record in matches], ["profile-001"])

    def test_bad_registry_entry_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            RunRecord(
                run_id="",
                run_name="bad",
                run_type="profile",
                artifact_dir="experiments/a100/bad",
                summary_path="experiments/a100/bad/summary.json",
                success=True,
                context_length=0,
                batch_size=4,
                grad_accum=4,
                max_steps=50,
                attention_backend="sdpa",
            )


if __name__ == "__main__":
    unittest.main()
