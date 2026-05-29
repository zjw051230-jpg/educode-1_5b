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
    / "fineweb_edu_5gb_300m_10step_public16k_seq1024_sdpa_memory_preflight"
    / "results_imported_modal_streaming"
)
VALIDATION_SUMMARY_PATH = IMPORT_DIR / "import_validation_summary.json"
EXPECTED_RUN_NAME = "fineweb_edu_5gb_300m_10step_public16k_seq1024_sdpa_memory_preflight"
EXPECTED_MODE = "preflight_5gb_10step_seq1024_sdpa_memory"
EXPECTED_FINAL_TRAIN_LOSS = 2.392136
EXPECTED_FINAL_VALIDATION_LOSS = 9.044042
EXPECTED_RESULT_PACKAGE = "/vol/results/mvp29_a100_5gb_10step_seq1024_sdpa_memory_preflight_results.tar.gz"
REQUIRED_FILES = (
    "summary.json",
    "summary.md",
    "metrics.jsonl",
    "validation_metrics.jsonl",
    "run_config.json",
    "run_metadata.json",
    "post_run_artifact_validation_summary.json",
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if stripped:
                payload = json.loads(stripped)
                if isinstance(payload, dict):
                    rows.append(payload)
    return rows


def finite_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def close_enough(actual: Any, expected: float, tolerance: float = 1e-6) -> bool:
    return finite_number(actual) and abs(float(actual) - expected) <= tolerance


def rounded(value: float | None) -> float | None:
    return round(value, 6) if value is not None and math.isfinite(value) else None


def infer_mode(run_name: Any) -> str | None:
    if run_name == EXPECTED_RUN_NAME:
        return EXPECTED_MODE
    return None


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

    training = run_config.get("training", {}) if isinstance(run_config.get("training"), dict) else {}
    profiling = run_config.get("profiling", {}) if isinstance(run_config.get("profiling"), dict) else {}
    declared_features = (
        summary.get("declared_model_features", {})
        if isinstance(summary.get("declared_model_features"), dict)
        else {}
    )
    mode = infer_mode(summary.get("run_name"))
    final_validation_loss = summary.get("final_val_loss", summary.get("final_validation_loss"))
    attention_backend = profiling.get("attention_backend") or declared_features.get("attention_backend")

    if summary.get("success") is not True:
        blockers.append("summary.success must be true")
    if run_metadata.get("status") != "success":
        blockers.append("run_metadata.status must be success")
    if mode != EXPECTED_MODE:
        blockers.append(f"mode expected {EXPECTED_MODE}, inferred {mode!r}")
    if summary.get("sequence_length") != 1024:
        blockers.append(f"context_length expected 1024, got {summary.get('sequence_length')!r}")
    if summary.get("batch_size") != 4:
        blockers.append(f"batch_size expected 4, got {summary.get('batch_size')!r}")
    if summary.get("gradient_accumulation_steps") != 4:
        blockers.append(f"grad_accum expected 4, got {summary.get('gradient_accumulation_steps')!r}")
    if attention_backend != "sdpa":
        blockers.append(f"attention_backend expected sdpa, got {attention_backend!r}")
    if summary.get("max_steps") != 10:
        blockers.append(f"max_steps expected 10, got {summary.get('max_steps')!r}")
    if len(metrics) != 10:
        blockers.append(f"metrics.jsonl row count expected 10, got {len(metrics)}")
    if len(validation_metrics) != 1:
        blockers.append(f"validation_metrics.jsonl row count expected 1, got {len(validation_metrics)}")
    if not close_enough(summary.get("final_train_loss"), EXPECTED_FINAL_TRAIN_LOSS):
        blockers.append(f"final_train_loss expected {EXPECTED_FINAL_TRAIN_LOSS}, got {summary.get('final_train_loss')!r}")
    if not close_enough(final_validation_loss, EXPECTED_FINAL_VALIDATION_LOSS):
        blockers.append(f"final_validation_loss expected {EXPECTED_FINAL_VALIDATION_LOSS}, got {final_validation_loss!r}")
    if post_run.get("blocker_count") != 0 or post_run.get("status") != "success":
        blockers.append("post-run artifact validation must pass with blocker_count=0")
    if post_run.get("artifact_validation_gate_type") != "bounded_seq1024_sdpa_memory_preflight":
        blockers.append("post-run artifact validation must use bounded_seq1024_sdpa_memory_preflight gate")
    if profiling.get("expected_result_package") != EXPECTED_RESULT_PACKAGE:
        blockers.append("run_config profiling.expected_result_package mismatch")

    checkpoint_like_files = [
        path.relative_to(IMPORT_DIR).as_posix()
        for path in IMPORT_DIR.rglob("*")
        if path.is_file() and path.suffix.lower() in {".pt", ".pth", ".ckpt", ".safetensors"}
    ]
    if checkpoint_like_files:
        blockers.append(f"imported artifact must not include checkpoint files: {checkpoint_like_files}")

    oom_detected = any("oom" in str(item).lower() or "out of memory" in str(item).lower() for item in post_run.get("blockers", []))
    if oom_detected:
        blockers.append("OOM detected in post-run blockers")

    tokens_per_sec_values = [float(row["tokens_per_sec"]) for row in metrics if finite_number(row.get("tokens_per_sec"))]
    step_time_values = [float(row["elapsed_seconds"]) for row in metrics if finite_number(row.get("elapsed_seconds"))]
    allocated_values = [
        float(row["gpu_memory_allocated_gib"]) for row in metrics if finite_number(row.get("gpu_memory_allocated_gib"))
    ]
    reserved_values = [
        float(row["gpu_memory_reserved_gib"]) for row in metrics if finite_number(row.get("gpu_memory_reserved_gib"))
    ]
    mfu_values = [float(row["mfu"]) for row in metrics if finite_number(row.get("mfu"))]

    if not tokens_per_sec_values:
        caveats.append("metrics.jsonl has no finite tokens_per_sec values")
    if not step_time_values:
        caveats.append("metrics.jsonl has no finite elapsed_seconds values")
    if not allocated_values or not reserved_values:
        caveats.append("metrics.jsonl has incomplete GPU memory values")
    if not mfu_values:
        caveats.append("mfu values are absent or null in metrics.jsonl")

    result = {
        "validation_status": "passed" if not blockers else "failed",
        "blocker_count": len(blockers),
        "blockers": blockers,
        "caveat_count": len(caveats),
        "caveats": caveats,
        "mode": mode,
        "training_status": run_metadata.get("status"),
        "context_length": summary.get("sequence_length"),
        "batch_size": summary.get("batch_size"),
        "grad_accum": summary.get("gradient_accumulation_steps"),
        "attention_backend": attention_backend,
        "max_steps": summary.get("max_steps"),
        "metrics_rows": len(metrics),
        "validation_metrics_rows": len(validation_metrics),
        "final_train_loss": summary.get("final_train_loss"),
        "final_validation_loss": final_validation_loss,
        "post_run_blocker_count": post_run.get("blocker_count"),
        "oom_detected": oom_detected,
        "checkpoint_imported": bool(checkpoint_like_files),
        "summary_tokens_per_sec": rounded(float(summary["approximate_tokens_per_sec"]))
        if finite_number(summary.get("approximate_tokens_per_sec"))
        else None,
        "mean_step_tokens_per_sec": rounded(mean(tokens_per_sec_values)) if tokens_per_sec_values else None,
        "average_step_time_seconds": rounded(mean(step_time_values)) if step_time_values else None,
        "peak_gpu_memory_allocated_gib": rounded(max(allocated_values)) if allocated_values else None,
        "peak_gpu_memory_reserved_gib": rounded(max(reserved_values)) if reserved_values else None,
        "mfu_available": bool(mfu_values),
        "mfu_value": rounded(mean(mfu_values)) if mfu_values else None,
        "run_metadata_gpu_name": run_metadata.get("gpu_name"),
        "run_metadata_git_commit": run_metadata.get("git_commit"),
    }
    VALIDATION_SUMMARY_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not blockers else 1


if __name__ == "__main__":
    raise SystemExit(main())
