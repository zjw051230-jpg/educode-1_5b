from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_a800_public16k_run_artifacts.py"
def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


def run_validator(output_dir: Path) -> tuple[int, str, dict[str, Any] | None]:
    completed = subprocess.run(
        [sys.executable, str(VALIDATOR_PATH), "--output-dir", str(output_dir)],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        encoding="utf-8",
    )
    summary_path = output_dir / "post_run_artifact_validation_summary.json"
    summary = load_json(summary_path) if summary_path.exists() else None
    return completed.returncode, completed.stdout + completed.stderr, summary


def make_profile_fixture(output_dir: Path, *, metrics_rows: int = 50, max_steps: int = 50) -> None:
    run_name = "fineweb_edu_5gb_300m_50step_public16k_sdpa_profile"
    checkpoint_path = output_dir / "checkpoints" / f"checkpoint_step_{max_steps:04d}.pt"
    summary = {
        "run_id": f"synthetic_{run_name}",
        "run_name": run_name,
        "output_dir": output_dir.as_posix(),
        "runtime_device": "cuda",
        "runtime_dtype": "bf16",
        "max_steps": max_steps,
        "eval_interval": 50,
        "batch_size": 8,
        "sequence_length": 512,
        "data_loading_mode": "streaming",
        "tokenizer_vocab_size": 16384,
        "exact_parameter_count": 336106496,
        "first_train_loss": 9.869211,
        "final_train_loss": 4.271052,
        "final_val_loss": 8.776379,
        "loss_all_finite": True,
        "val_loss_all_finite": True,
        "grad_all_finite": True,
        "metrics_rows": metrics_rows,
        "validation_rows": 1,
        "expected_validation_rows": 1,
        "checkpoint_path": checkpoint_path.as_posix(),
        "checkpoint_path_starts_with_output_dir": True,
        "checkpoint_reload_match": True,
        "success": True,
    }
    run_config = {
        "status": "profiling_ready_not_run",
        "run": {
            "run_name": run_name,
            "output_dir": output_dir.as_posix(),
        },
        "training": {
            "max_steps": max_steps,
            "eval_interval": 50,
            "batch_size": 8,
            "gradient_accumulation_steps": 4,
            "sequence_length": 512,
        },
        "profiling": {
            "enabled": True,
            "profile_mode": "bounded_sdpa_profile",
            "attention_backend": "sdpa",
            "record_tokens_per_sec": True,
            "record_memory": True,
            "record_mfu": True,
        },
    }
    metadata = {
        "status": "success",
        "gpu_name": "NVIDIA A100-SXM4-40GB",
        "git_commit": "synthetic",
    }
    metrics = [
        {
            "step": step,
            "tokens_seen": step * 16384,
            "train_loss": 9.0 / step,
            "val_loss": None,
            "tokens_per_sec": 48000.0,
            "elapsed_seconds": 0.35 * step,
            "gpu_memory_allocated_gib": 2.7,
            "gpu_memory_reserved_gib": 8.5,
            "mfu": None,
        }
        for step in range(1, metrics_rows + 1)
    ]
    validation_metrics = [{"step": 50, "tokens_seen": 819200, "val_loss": 8.776379}]

    write_json(output_dir / "summary.json", summary)
    write_json(output_dir / "run_config.json", run_config)
    write_json(output_dir / "run_metadata.json", metadata)
    write_jsonl(output_dir / "metrics.jsonl", metrics)
    write_jsonl(output_dir / "validation_metrics.jsonl", validation_metrics)


def make_training_fixture(output_dir: Path) -> None:
    run_name = "fineweb_edu_5gb_300m_3000step_public16k_execute"
    checkpoint_path = output_dir / "checkpoints" / "checkpoint_step_3000.pt"
    summary = {
        "run_id": f"synthetic_{run_name}",
        "run_name": run_name,
        "output_dir": output_dir.as_posix(),
        "runtime_device": "cuda",
        "runtime_dtype": "bf16",
        "max_steps": 3000,
        "eval_interval": 300,
        "batch_size": 8,
        "sequence_length": 512,
        "data_loading_mode": "streaming",
        "tokenizer_vocab_size": 16384,
        "exact_parameter_count": 336106496,
        "first_train_loss": 9.869211,
        "final_train_loss": 3.029707,
        "final_val_loss": 8.341638,
        "loss_all_finite": True,
        "val_loss_all_finite": True,
        "grad_all_finite": True,
        "metrics_rows": 3000,
        "validation_rows": 10,
        "expected_validation_rows": 10,
        "checkpoint_path": checkpoint_path.as_posix(),
        "checkpoint_path_starts_with_output_dir": True,
        "checkpoint_reload_match": True,
        "success": True,
    }
    run_config = {
        "status": "preflight_ready_not_run",
        "run": {
            "run_name": run_name,
            "output_dir": output_dir.as_posix(),
        },
        "training": {
            "max_steps": 3000,
            "eval_interval": 300,
            "batch_size": 8,
            "gradient_accumulation_steps": 4,
            "sequence_length": 512,
        },
        "profiling": {
            "enabled": True,
            "attention_backend": "sdpa",
            "record_tokens_per_sec": True,
            "record_memory": True,
            "record_mfu": True,
        },
    }
    metadata = {
        "status": "success",
        "gpu_name": "NVIDIA A100-SXM4-40GB",
        "git_commit": "synthetic",
    }
    metrics = [{"step": step, "train_loss": 9.0 / step} for step in range(1, 3001)]
    validation_metrics = [{"step": step, "val_loss": 9.0 - (step / 1000.0)} for step in range(300, 3001, 300)]

    write_json(output_dir / "summary.json", summary)
    write_json(output_dir / "run_config.json", run_config)
    write_json(output_dir / "run_metadata.json", metadata)
    write_jsonl(output_dir / "metrics.jsonl", metrics)
    write_jsonl(output_dir / "validation_metrics.jsonl", validation_metrics)


def main() -> int:
    blockers: list[str] = []

    profile_artifact_validation_passed = False
    training_artifact_validation_still_passed = False
    bad_profile_rejected = False
    profile_output = ""
    training_output = ""
    bad_output = ""

    with tempfile.TemporaryDirectory(prefix="mvp28_profile_artifact_") as temp_dir:
        profile_dir = Path(temp_dir) / "profile"
        make_profile_fixture(profile_dir)
        profile_returncode, profile_output, profile_summary = run_validator(profile_dir)
        profile_artifact_validation_passed = (
            profile_returncode == 0
            and profile_summary is not None
            and profile_summary.get("status") == "success"
            and profile_summary.get("artifact_validation_gate_type") == "bounded_sdpa_profile"
            and profile_summary.get("metrics_rows_actual") == 50
            and profile_summary.get("validation_rows_actual") == 1
        )
        if not profile_artifact_validation_passed:
            blockers.append("synthetic 50-step bounded SDPA profile artifact did not pass validation")

        training_dir = Path(temp_dir) / "training_3000"
        make_training_fixture(training_dir)
        training_returncode, training_output, training_summary = run_validator(training_dir)
        training_artifact_validation_still_passed = (
            training_returncode == 0
            and training_summary is not None
            and training_summary.get("status") == "success"
            and training_summary.get("artifact_validation_gate_type") == "training_execution"
            and training_summary.get("metrics_rows_actual") == 3000
            and training_summary.get("validation_rows_actual") == 10
        )
        if not training_artifact_validation_still_passed:
            blockers.append("5GB 3000-step training artifact validation no longer passes training_execution gate")

        bad_profile_dir = Path(temp_dir) / "bad_profile"
        make_profile_fixture(bad_profile_dir, metrics_rows=49, max_steps=50)
        bad_returncode, bad_output, bad_summary = run_validator(bad_profile_dir)
        bad_profile_rejected = (
            bad_returncode != 0
            and bad_summary is not None
            and bad_summary.get("status") == "failed"
            and bad_summary.get("artifact_validation_gate_type") == "bounded_sdpa_profile"
            and bad_summary.get("blocker_count", 0) > 0
        )
        if not bad_profile_rejected:
            blockers.append("synthetic bad bounded profile artifact was not rejected")

    result = {
        "validation_status": "passed" if not blockers else "failed",
        "blocker_count": len(blockers),
        "profile_artifact_validation_passed": profile_artifact_validation_passed,
        "training_artifact_validation_still_passed": training_artifact_validation_still_passed,
        "bad_profile_rejected": bad_profile_rejected,
        "blockers": blockers,
        "profile_validator_output_excerpt": profile_output.splitlines()[-8:],
        "training_validator_output_excerpt": training_output.splitlines()[-8:],
        "bad_profile_validator_output_excerpt": bad_output.splitlines()[-8:],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not blockers else 1


if __name__ == "__main__":
    raise SystemExit(main())
