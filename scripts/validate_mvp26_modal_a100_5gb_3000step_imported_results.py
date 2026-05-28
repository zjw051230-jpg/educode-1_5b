from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
IMPORT_DIR = (
    PROJECT_ROOT
    / "experiments"
    / "a100"
    / "fineweb_edu_5gb_300m_3000step_public16k_execute"
    / "results_imported_modal_streaming"
)

SUMMARY_PATH = IMPORT_DIR / "summary.json"
METRICS_PATH = IMPORT_DIR / "metrics.jsonl"
VALIDATION_METRICS_PATH = IMPORT_DIR / "validation_metrics.jsonl"
RUN_CONFIG_PATH = IMPORT_DIR / "run_config.json"
RUN_METADATA_PATH = IMPORT_DIR / "run_metadata.json"
POST_RUN_VALIDATION_PATH = IMPORT_DIR / "post_run_artifact_validation_summary.json"
IMPORT_VALIDATION_SUMMARY_PATH = IMPORT_DIR / "import_validation_summary.json"

EXPECTED_MODE = "train_5gb_3000"
EXPECTED_CONFIG_PATH = "configs/a100/fineweb_edu_5gb_300m_3000step_public16k_execute.json"
EXPECTED_RESULT_PACKAGE = "/vol/results/mvp26_a100_5gb_3000step_public16k_streaming_results.tar.gz"
EXPECTED_FILES = {
    "summary.json",
    "summary.md",
    "metrics.jsonl",
    "validation_metrics.jsonl",
    "run_config.json",
    "run_metadata.json",
    "post_run_artifact_validation_summary.json",
}
FORBIDDEN_NAME_TOKENS = (
    "checkpoint",
    "raw.jsonl",
    "processed",
    "splits",
    ".tar.gz",
)


class ImportValidationError(Exception):
    pass


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ImportValidationError(f"{path} did not contain a JSON object")
    return data


def count_jsonl_rows(path: Path) -> int:
    with path.open("r", encoding="utf-8") as handle:
        return sum(1 for line in handle if line.strip())


def add_check(blockers: list[str], condition: bool, message: str) -> None:
    if not condition:
        blockers.append(message)


def check_equal(blockers: list[str], label: str, actual: Any, expected: Any) -> None:
    add_check(blockers, actual == expected, f"{label}: expected {expected!r}, got {actual!r}")


def check_close(blockers: list[str], label: str, actual: Any, expected: float, tolerance: float = 1e-6) -> None:
    add_check(
        blockers,
        isinstance(actual, (int, float)) and abs(float(actual) - expected) <= tolerance,
        f"{label}: expected {expected!r}, got {actual!r}",
    )


def validate_imported_results() -> dict[str, Any]:
    blockers: list[str] = []

    add_check(blockers, IMPORT_DIR.exists(), f"import directory missing: {IMPORT_DIR}")
    if not IMPORT_DIR.exists():
        summary = build_summary(blockers, {}, {}, {}, 0, 0)
        write_summary(summary)
        return summary

    imported_files = sorted(path.name for path in IMPORT_DIR.iterdir() if path.is_file())
    missing_files = sorted(EXPECTED_FILES - set(imported_files))
    add_check(blockers, not missing_files, f"missing expected imported files: {missing_files}")

    forbidden_paths = []
    for path in IMPORT_DIR.rglob("*"):
        relative = path.relative_to(IMPORT_DIR).as_posix()
        if relative == IMPORT_VALIDATION_SUMMARY_PATH.name:
            continue
        lowered = relative.lower()
        if any(token in lowered for token in FORBIDDEN_NAME_TOKENS):
            forbidden_paths.append(relative)
    add_check(blockers, not forbidden_paths, f"forbidden imported artifacts found: {forbidden_paths}")

    required_paths = [
        SUMMARY_PATH,
        METRICS_PATH,
        VALIDATION_METRICS_PATH,
        RUN_CONFIG_PATH,
        RUN_METADATA_PATH,
        POST_RUN_VALIDATION_PATH,
    ]
    for path in required_paths:
        add_check(blockers, path.exists(), f"required file missing: {path.relative_to(PROJECT_ROOT).as_posix()}")

    if any(not path.exists() for path in required_paths):
        summary = build_summary(blockers, {}, {}, {}, 0, 0)
        write_summary(summary)
        return summary

    summary_json = load_json(SUMMARY_PATH)
    run_metadata = load_json(RUN_METADATA_PATH)
    post_run_validation = load_json(POST_RUN_VALIDATION_PATH)

    check_equal(blockers, "summary.success", summary_json.get("success"), True)
    check_equal(blockers, "inferred training_status", "success" if summary_json.get("success") else "failed", "success")
    check_equal(blockers, "inferred mode", EXPECTED_MODE, EXPECTED_MODE)
    check_equal(blockers, "summary.config_path", summary_json.get("config_path"), EXPECTED_CONFIG_PATH)
    check_equal(blockers, "summary.run_name", summary_json.get("run_name"), "fineweb_edu_5gb_300m_3000step_public16k_execute")
    check_equal(blockers, "summary.runtime_device", summary_json.get("runtime_device"), "cuda")
    check_equal(blockers, "summary.runtime_dtype", summary_json.get("runtime_dtype"), "bf16")
    check_equal(blockers, "summary.exact_parameter_count", summary_json.get("exact_parameter_count"), 336_106_496)
    check_equal(blockers, "summary.max_steps", summary_json.get("max_steps"), 3000)
    check_equal(blockers, "summary.batch_size", summary_json.get("batch_size"), 8)
    check_equal(blockers, "summary.gradient_accumulation_steps", summary_json.get("gradient_accumulation_steps"), 4)
    check_equal(blockers, "summary.data_loading_mode", summary_json.get("data_loading_mode"), "streaming")
    check_equal(blockers, "summary.train_sampling_policy", summary_json.get("train_sampling_policy"), "shuffle_buffer")
    check_equal(blockers, "summary.val_sampling_policy", summary_json.get("val_sampling_policy"), "shuffle_buffer")
    check_equal(blockers, "summary.val_shuffle_seed", summary_json.get("val_shuffle_seed"), 7331)
    check_equal(blockers, "summary.val_shuffle_buffer_size", summary_json.get("val_shuffle_buffer_size"), 64)
    check_equal(blockers, "summary.validation_max_blocks_per_document", summary_json.get("validation_max_blocks_per_document"), 8)
    add_check(
        blockers,
        isinstance(summary_json.get("validation_unique_doc_count"), int)
        and summary_json.get("validation_unique_doc_count") > 1,
        f"summary.validation_unique_doc_count must be > 1, got {summary_json.get('validation_unique_doc_count')!r}",
    )
    check_equal(blockers, "summary.validation_batches_evaluated", summary_json.get("validation_batches_evaluated"), 10)
    check_equal(blockers, "summary.validation_tokens_evaluated", summary_json.get("validation_tokens_evaluated"), 40_960)
    check_equal(blockers, "summary.validation_prefix_only_risk", summary_json.get("validation_prefix_only_risk"), False)
    check_equal(blockers, "summary.metrics_rows", summary_json.get("metrics_rows"), 3000)
    check_equal(blockers, "summary.validation_rows", summary_json.get("validation_rows"), 10)
    check_equal(blockers, "summary.tokens_seen", summary_json.get("tokens_seen"), 49_152_000)
    check_close(blockers, "summary.final_train_loss", summary_json.get("final_train_loss"), 3.029707)
    check_close(blockers, "summary.final_val_loss", summary_json.get("final_val_loss"), 8.341638)
    check_equal(blockers, "summary.loss_all_finite", summary_json.get("loss_all_finite"), True)
    check_equal(blockers, "summary.val_loss_all_finite", summary_json.get("val_loss_all_finite"), True)
    check_equal(blockers, "summary.grad_all_finite", summary_json.get("grad_all_finite"), True)
    check_equal(blockers, "summary.checkpoint_reload_match", summary_json.get("checkpoint_reload_match"), True)
    add_check(blockers, bool(summary_json.get("checkpoint_path")), "summary.checkpoint_path must be present")
    check_equal(
        blockers,
        "summary.post_run_artifact_validation.passed",
        summary_json.get("post_run_artifact_validation", {}).get("passed")
        if isinstance(summary_json.get("post_run_artifact_validation"), dict)
        else None,
        True,
    )

    check_equal(blockers, "post_run.status", post_run_validation.get("status"), "success")
    check_equal(blockers, "post_run.ready_for_review", post_run_validation.get("ready_for_review"), True)
    check_equal(blockers, "post_run.blocker_count", post_run_validation.get("blocker_count"), 0)
    check_equal(blockers, "post_run.loss_all_finite", post_run_validation.get("loss_all_finite"), True)
    check_equal(blockers, "post_run.val_loss_all_finite", post_run_validation.get("val_loss_all_finite"), True)
    check_equal(blockers, "post_run.grad_all_finite", post_run_validation.get("grad_all_finite"), True)
    check_equal(blockers, "post_run.checkpoint_reload_match", post_run_validation.get("checkpoint_reload_match"), True)

    check_equal(blockers, "run_metadata.status", run_metadata.get("status"), "success")
    check_equal(blockers, "run_metadata.hostname", run_metadata.get("hostname"), "modal")
    add_check(blockers, "A100" in str(run_metadata.get("gpu_name", "")), f"run_metadata.gpu_name must include A100, got {run_metadata.get('gpu_name')!r}")
    add_check(blockers, str(run_metadata.get("git_commit", "")).startswith("f703e07"), f"run_metadata.git_commit must start with f703e07, got {run_metadata.get('git_commit')!r}")

    metrics_rows_actual = count_jsonl_rows(METRICS_PATH)
    validation_rows_actual = count_jsonl_rows(VALIDATION_METRICS_PATH)
    check_equal(blockers, "metrics.jsonl row count", metrics_rows_actual, 3000)
    check_equal(blockers, "validation_metrics.jsonl row count", validation_rows_actual, 10)

    summary = build_summary(
        blockers,
        summary_json,
        run_metadata,
        post_run_validation,
        metrics_rows_actual,
        validation_rows_actual,
    )
    write_summary(summary)
    return summary


def build_summary(
    blockers: list[str],
    summary_json: dict[str, Any],
    run_metadata: dict[str, Any],
    post_run_validation: dict[str, Any],
    metrics_rows_actual: int,
    validation_rows_actual: int,
) -> dict[str, Any]:
    return {
        "validation_status": "passed" if not blockers else "failed",
        "import_dir": IMPORT_DIR.relative_to(PROJECT_ROOT).as_posix(),
        "mode": EXPECTED_MODE,
        "training_status": "success" if summary_json.get("success") else None,
        "produced_checkpoint": bool(summary_json.get("checkpoint_path")),
        "result_package": EXPECTED_RESULT_PACKAGE,
        "summary_path": SUMMARY_PATH.relative_to(PROJECT_ROOT).as_posix(),
        "metrics_path": METRICS_PATH.relative_to(PROJECT_ROOT).as_posix(),
        "validation_metrics_path": VALIDATION_METRICS_PATH.relative_to(PROJECT_ROOT).as_posix(),
        "run_config_path": RUN_CONFIG_PATH.relative_to(PROJECT_ROOT).as_posix(),
        "run_metadata_path": RUN_METADATA_PATH.relative_to(PROJECT_ROOT).as_posix(),
        "post_run_artifact_validation_summary_path": POST_RUN_VALIDATION_PATH.relative_to(PROJECT_ROOT).as_posix(),
        "run_id": summary_json.get("run_id"),
        "run_name": summary_json.get("run_name"),
        "config_path": summary_json.get("config_path"),
        "backend_gpu": f"Modal / {run_metadata.get('gpu_name')}" if run_metadata.get("gpu_name") else None,
        "git_commit": run_metadata.get("git_commit"),
        "max_steps": summary_json.get("max_steps"),
        "metrics_rows_summary": summary_json.get("metrics_rows"),
        "metrics_rows_actual": metrics_rows_actual,
        "validation_rows_summary": summary_json.get("validation_rows"),
        "validation_rows_actual": validation_rows_actual,
        "final_train_loss": summary_json.get("final_train_loss"),
        "final_validation_loss": summary_json.get("final_val_loss"),
        "tokens_seen": summary_json.get("tokens_seen"),
        "elapsed_seconds": summary_json.get("elapsed_seconds"),
        "approximate_tokens_per_sec": summary_json.get("approximate_tokens_per_sec"),
        "train_sampling_policy": summary_json.get("train_sampling_policy"),
        "validation_sampling_policy": summary_json.get("val_sampling_policy"),
        "validation_unique_doc_count": summary_json.get("validation_unique_doc_count"),
        "validation_batches_evaluated": summary_json.get("validation_batches_evaluated"),
        "validation_tokens_evaluated": summary_json.get("validation_tokens_evaluated"),
        "validation_prefix_only_risk": summary_json.get("validation_prefix_only_risk"),
        "checkpoint_reload_match": summary_json.get("checkpoint_reload_match"),
        "post_run_artifact_validation_passed": summary_json.get("post_run_artifact_validation", {}).get("passed")
        if isinstance(summary_json.get("post_run_artifact_validation"), dict)
        else None,
        "post_run_blocker_count": post_run_validation.get("blocker_count"),
        "blockers": blockers,
        "blocker_count": len(blockers),
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }


def write_summary(summary: dict[str, Any]) -> None:
    IMPORT_VALIDATION_SUMMARY_PATH.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    summary = validate_imported_results()
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0 if summary["validation_status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
