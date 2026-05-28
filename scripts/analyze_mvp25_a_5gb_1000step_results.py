from __future__ import annotations

import json
from pathlib import Path
from statistics import mean, pstdev
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
IMPORT_DIR = (
    PROJECT_ROOT
    / "experiments"
    / "a100"
    / "fineweb_edu_5gb_300m_1000step_public16k_execute"
    / "results_imported_modal_streaming"
)

REQUIRED_FILES = {
    "summary.json": IMPORT_DIR / "summary.json",
    "summary.md": IMPORT_DIR / "summary.md",
    "metrics.jsonl": IMPORT_DIR / "metrics.jsonl",
    "validation_metrics.jsonl": IMPORT_DIR / "validation_metrics.jsonl",
    "run_config.json": IMPORT_DIR / "run_config.json",
    "run_metadata.json": IMPORT_DIR / "run_metadata.json",
    "post_run_artifact_validation_summary.json": IMPORT_DIR / "post_run_artifact_validation_summary.json",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"expected JSON object in {path}")
    return data


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            row = json.loads(line)
            if not isinstance(row, dict):
                raise ValueError(f"expected JSON object at {path}:{line_number}")
            rows.append(row)
    return rows


def numeric_values(rows: list[dict[str, Any]], key: str) -> list[float]:
    values: list[float] = []
    for row in rows:
        value = row.get(key)
        if isinstance(value, (int, float)):
            values.append(float(value))
    return values


def loss_slope(values: list[float]) -> str:
    if len(values) < 2:
        return "insufficient_data"
    if values[-1] < values[0]:
        return "down"
    if values[-1] > values[0]:
        return "up"
    return "flat"


def required_files_status() -> dict[str, bool]:
    return {name: path.exists() for name, path in REQUIRED_FILES.items()}


def analyze() -> dict[str, Any]:
    required_status = required_files_status()
    missing_files = [name for name, exists in required_status.items() if not exists]
    if missing_files:
        return {
            "analysis_status": "failed",
            "import_dir": IMPORT_DIR.relative_to(PROJECT_ROOT).as_posix(),
            "required_files_exist": required_status,
            "missing_files": missing_files,
        }

    summary = load_json(REQUIRED_FILES["summary.json"])
    run_config = load_json(REQUIRED_FILES["run_config.json"])
    run_metadata = load_json(REQUIRED_FILES["run_metadata.json"])
    post_run_validation = load_json(REQUIRED_FILES["post_run_artifact_validation_summary.json"])
    train_rows = load_jsonl(REQUIRED_FILES["metrics.jsonl"])
    validation_rows = load_jsonl(REQUIRED_FILES["validation_metrics.jsonl"])

    train_losses = numeric_values(train_rows, "train_loss")
    validation_losses = numeric_values(validation_rows, "val_loss")
    validation_range = max(validation_losses) - min(validation_losses) if validation_losses else None
    validation_stddev = pstdev(validation_losses) if len(validation_losses) > 1 else 0.0 if validation_losses else None

    expected_train_rows = summary.get("metrics_rows")
    expected_validation_rows = summary.get("validation_rows")
    analysis_passed = (
        len(train_rows) == expected_train_rows == 1000
        and len(validation_rows) == expected_validation_rows == 10
        and bool(train_losses)
        and bool(validation_losses)
        and summary.get("success") is True
        and post_run_validation.get("status") == "success"
        and post_run_validation.get("blocker_count") == 0
    )

    return {
        "analysis_status": "passed" if analysis_passed else "failed",
        "import_dir": IMPORT_DIR.relative_to(PROJECT_ROOT).as_posix(),
        "required_files_exist": required_status,
        "missing_files": [],
        "run_id": summary.get("run_id"),
        "run_name": summary.get("run_name"),
        "run_metadata_status": run_metadata.get("status"),
        "gpu_name": run_metadata.get("gpu_name"),
        "train_metrics_row_count": len(train_rows),
        "validation_row_count": len(validation_rows),
        "expected_train_metrics_row_count": expected_train_rows,
        "expected_validation_row_count": expected_validation_rows,
        "first_train_loss": train_losses[0] if train_losses else None,
        "last_train_loss": train_losses[-1] if train_losses else None,
        "summary_first_train_loss": summary.get("first_train_loss"),
        "summary_final_train_loss": summary.get("final_train_loss"),
        "first_validation_loss": validation_losses[0] if validation_losses else None,
        "last_validation_loss": validation_losses[-1] if validation_losses else None,
        "summary_final_validation_loss": summary.get("final_val_loss"),
        "min_train_loss": min(train_losses) if train_losses else None,
        "min_validation_loss": min(validation_losses) if validation_losses else None,
        "max_validation_loss": max(validation_losses) if validation_losses else None,
        "mean_validation_loss": mean(validation_losses) if validation_losses else None,
        "validation_loss_range": validation_range,
        "validation_loss_population_stddev": validation_stddev,
        "train_loss_direction_first_to_last": loss_slope(train_losses),
        "validation_loss_direction_first_to_last": loss_slope(validation_losses),
        "sampling_policy": summary.get("sampling_policy"),
        "train_sampling_policy": summary.get("train_sampling_policy"),
        "val_sampling_policy": summary.get("val_sampling_policy"),
        "shuffle_seed": summary.get("shuffle_seed"),
        "shuffle_buffer_size": summary.get("shuffle_buffer_size"),
        "bounded_prefix_batches_only": summary.get("bounded_prefix_batches_only"),
        "run_config_sampling": run_config.get("sampling"),
        "data_loading_mode": summary.get("data_loading_mode"),
        "scheduler_policy": summary.get("scheduler_policy"),
        "learning_rate_mode": summary.get("learning_rate_mode"),
        "post_run_artifact_validation_status": post_run_validation.get("status"),
        "post_run_artifact_validation_blocker_count": post_run_validation.get("blocker_count"),
    }


def main() -> int:
    result = analyze()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["analysis_status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
