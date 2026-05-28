from __future__ import annotations

import json
import math
from pathlib import Path
from statistics import mean
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
IMPORT_DIR = (
    REPO_ROOT
    / "experiments"
    / "a100"
    / "fineweb_edu_5gb_300m_50step_public16k_sdpa_profile"
    / "results_imported_modal_streaming"
)
REQUIRED_FILES = (
    "summary.json",
    "summary.md",
    "metrics.jsonl",
    "validation_metrics.jsonl",
    "run_config.json",
    "run_metadata.json",
    "post_run_artifact_validation_summary.json",
)
EXPECTED_RUN_NAME = "fineweb_edu_5gb_300m_50step_public16k_sdpa_profile"
EXPECTED_MODE = "profile_5gb_50step_sdpa"
EXPECTED_MAX_STEPS = 50
EXPECTED_FINAL_TRAIN_LOSS = 4.328258
EXPECTED_FINAL_VAL_LOSS = 8.897261


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if not stripped:
                continue
            payload = json.loads(stripped)
            if isinstance(payload, dict):
                rows.append(payload)
    return rows


def finite_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def close_enough(actual: Any, expected: float, tolerance: float = 1e-6) -> bool:
    return finite_number(actual) and abs(float(actual) - expected) <= tolerance


def maybe_round(value: float | None) -> float | None:
    return round(value, 6) if value is not None and math.isfinite(value) else None


def main() -> int:
    blockers: list[str] = []
    caveats: list[str] = []

    for filename in REQUIRED_FILES:
        if not (IMPORT_DIR / filename).exists():
            blockers.append(f"missing required file: {filename}")

    summary = load_json(IMPORT_DIR / "summary.json") if (IMPORT_DIR / "summary.json").exists() else {}
    run_config = load_json(IMPORT_DIR / "run_config.json") if (IMPORT_DIR / "run_config.json").exists() else {}
    run_metadata = load_json(IMPORT_DIR / "run_metadata.json") if (IMPORT_DIR / "run_metadata.json").exists() else {}
    post_run = (
        load_json(IMPORT_DIR / "post_run_artifact_validation_summary.json")
        if (IMPORT_DIR / "post_run_artifact_validation_summary.json").exists()
        else {}
    )
    metrics = load_jsonl(IMPORT_DIR / "metrics.jsonl") if (IMPORT_DIR / "metrics.jsonl").exists() else []
    validation_metrics = (
        load_jsonl(IMPORT_DIR / "validation_metrics.jsonl")
        if (IMPORT_DIR / "validation_metrics.jsonl").exists()
        else []
    )

    profiling = run_config.get("profiling", {}) if isinstance(run_config.get("profiling"), dict) else {}
    declared_features = summary.get("declared_model_features", {}) if isinstance(summary.get("declared_model_features"), dict) else {}
    attention_backend = profiling.get("attention_backend") or declared_features.get("attention_backend")
    mode_name = EXPECTED_MODE if summary.get("run_name") == EXPECTED_RUN_NAME else None

    if summary.get("success") is not True:
        blockers.append("summary.success must be true")
    if run_metadata.get("status") != "success":
        blockers.append("run_metadata.status must be success")
    if mode_name != EXPECTED_MODE:
        blockers.append(f"mode expected {EXPECTED_MODE}, inferred {mode_name!r}")
    if attention_backend != "sdpa":
        blockers.append(f"attention_backend expected sdpa, got {attention_backend!r}")
    if summary.get("max_steps") != EXPECTED_MAX_STEPS:
        blockers.append(f"max_steps expected {EXPECTED_MAX_STEPS}, got {summary.get('max_steps')!r}")
    if len(metrics) != EXPECTED_MAX_STEPS:
        blockers.append(f"metrics.jsonl row count expected 50, got {len(metrics)}")
    if len(validation_metrics) != 1:
        blockers.append(f"validation_metrics.jsonl row count expected 1, got {len(validation_metrics)}")
    if not close_enough(summary.get("final_train_loss"), EXPECTED_FINAL_TRAIN_LOSS):
        blockers.append(f"final_train_loss expected {EXPECTED_FINAL_TRAIN_LOSS}, got {summary.get('final_train_loss')!r}")
    final_val_loss = summary.get("final_val_loss", summary.get("final_validation_loss"))
    if not close_enough(final_val_loss, EXPECTED_FINAL_VAL_LOSS):
        blockers.append(f"final_validation_loss expected {EXPECTED_FINAL_VAL_LOSS}, got {final_val_loss!r}")
    if post_run.get("blocker_count") != 0 or post_run.get("status") != "success":
        blockers.append("post-run artifact validation must pass with blocker_count=0")
    if post_run.get("artifact_validation_gate_type") != "bounded_sdpa_profile":
        blockers.append("post-run artifact validation must use bounded_sdpa_profile gate")
    if summary.get("checkpoint_reload_match") is not True:
        blockers.append("checkpoint_reload_match must be true for produced remote checkpoint behavior")

    checkpoint_like_files = [
        path.relative_to(IMPORT_DIR).as_posix()
        for path in IMPORT_DIR.rglob("*")
        if path.is_file() and path.suffix.lower() in {".pt", ".pth", ".ckpt", ".safetensors"}
    ]
    if checkpoint_like_files:
        blockers.append(f"imported artifact must not include checkpoint files: {checkpoint_like_files}")

    tokens_per_sec_values = [float(row["tokens_per_sec"]) for row in metrics if finite_number(row.get("tokens_per_sec"))]
    elapsed_values = [float(row["elapsed_seconds"]) for row in metrics if finite_number(row.get("elapsed_seconds"))]
    memory_allocated_values = [
        float(row["gpu_memory_allocated_gib"]) for row in metrics if finite_number(row.get("gpu_memory_allocated_gib"))
    ]
    memory_reserved_values = [
        float(row["gpu_memory_reserved_gib"]) for row in metrics if finite_number(row.get("gpu_memory_reserved_gib"))
    ]
    mfu_values = [float(row["mfu"]) for row in metrics if finite_number(row.get("mfu"))]

    if not tokens_per_sec_values:
        caveats.append("metrics.jsonl has no finite tokens_per_sec values")
    if not elapsed_values:
        caveats.append("metrics.jsonl has no finite elapsed_seconds values")
    if not memory_allocated_values and not memory_reserved_values:
        caveats.append("metrics.jsonl has no finite GPU memory values")
    if not mfu_values:
        caveats.append("mfu values are absent or null in metrics.jsonl")

    average_tokens_per_sec = maybe_round(mean(tokens_per_sec_values)) if tokens_per_sec_values else None
    summary_tokens_per_sec = maybe_round(float(summary["approximate_tokens_per_sec"])) if finite_number(summary.get("approximate_tokens_per_sec")) else None
    average_step_time = maybe_round(mean(elapsed_values)) if elapsed_values else None
    peak_gpu_memory_allocated_gib = maybe_round(max(memory_allocated_values)) if memory_allocated_values else None
    peak_gpu_memory_reserved_gib = maybe_round(max(memory_reserved_values)) if memory_reserved_values else None
    average_mfu = maybe_round(mean(mfu_values)) if mfu_values else None

    result = {
        "validation_status": "passed" if not blockers else "failed",
        "blocker_count": len(blockers),
        "blockers": blockers,
        "caveat_count": len(caveats),
        "caveats": caveats,
        "mode": mode_name,
        "run_name": summary.get("run_name"),
        "training_status": run_metadata.get("status"),
        "attention_backend": attention_backend,
        "max_steps": summary.get("max_steps"),
        "metrics_rows": len(metrics),
        "validation_metrics_rows": len(validation_metrics),
        "final_train_loss": summary.get("final_train_loss"),
        "final_validation_loss": final_val_loss,
        "post_run_blocker_count": post_run.get("blocker_count"),
        "produced_checkpoint": summary.get("checkpoint_reload_match") is True,
        "checkpoint_imported": bool(checkpoint_like_files),
        "summary_tokens_per_sec": summary_tokens_per_sec,
        "average_tokens_per_sec": average_tokens_per_sec,
        "average_step_time_seconds": average_step_time,
        "peak_gpu_memory_allocated_gib": peak_gpu_memory_allocated_gib,
        "peak_gpu_memory_reserved_gib": peak_gpu_memory_reserved_gib,
        "average_mfu": average_mfu,
        "run_metadata_gpu_name": run_metadata.get("gpu_name"),
        "run_metadata_git_commit": run_metadata.get("git_commit"),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not blockers else 1


if __name__ == "__main__":
    raise SystemExit(main())
