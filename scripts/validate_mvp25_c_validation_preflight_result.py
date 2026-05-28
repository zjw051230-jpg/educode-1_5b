from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
IMPORT_DIR = (
    PROJECT_ROOT
    / "experiments"
    / "a100"
    / "fineweb_edu_5gb_300m_1000step_public16k_execute"
    / "results_imported_modal_validation_coverage_preflight"
)
SUMMARY_PATH = IMPORT_DIR / "validation_coverage_preflight_summary.json"
RECEIPT_PATH = IMPORT_DIR / "modal_preflight_receipt.json"

EXPECTED_MODE = "preflight_5gb_validation_coverage"
EXPECTED_POLICY = "shuffle_buffer"
EXPECTED_SEED = 7331
EXPECTED_BUFFER_SIZE = 64
EXPECTED_MAX_BLOCKS_PER_DOCUMENT = 8
EXPECTED_REQUIRED_COMMIT = "a8c2bb9"


class PreflightValidationError(Exception):
    pass


def resolve_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return PROJECT_ROOT / path


def relative_path(path: Path) -> str:
    try:
        return path.relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def load_json_object(path: Path, blockers: list[str], label: str) -> dict[str, Any]:
    if not path.exists():
        blockers.append(f"{label} missing: {relative_path(path)}")
        return {}
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise PreflightValidationError(f"{label} must contain a JSON object: {relative_path(path)}")
    return data


def add_check(blockers: list[str], condition: bool, message: str) -> None:
    if not condition:
        blockers.append(message)


def check_equal(blockers: list[str], label: str, actual: Any, expected: Any) -> None:
    add_check(blockers, actual == expected, f"{label}: expected {expected!r}, got {actual!r}")


def check_positive_int(blockers: list[str], label: str, value: Any) -> None:
    add_check(blockers, isinstance(value, int) and value > 0, f"{label}: expected positive integer, got {value!r}")


def check_gt_one_int(blockers: list[str], label: str, value: Any) -> None:
    add_check(blockers, isinstance(value, int) and value > 1, f"{label}: expected integer > 1, got {value!r}")


def validate_summary(summary: dict[str, Any], blockers: list[str]) -> None:
    check_equal(blockers, "preflight_status", summary.get("preflight_status"), "passed")
    check_equal(blockers, "mode", summary.get("mode"), EXPECTED_MODE)
    check_equal(blockers, "used_gpu", summary.get("used_gpu"), False)
    check_equal(blockers, "ran_training", summary.get("ran_training"), False)
    check_equal(blockers, "ran_backward", summary.get("ran_backward"), False)
    check_equal(blockers, "ran_optimizer_step", summary.get("ran_optimizer_step"), False)
    check_equal(blockers, "saved_checkpoint", summary.get("saved_checkpoint"), False)
    check_equal(blockers, "val_sampling_policy", summary.get("val_sampling_policy"), EXPECTED_POLICY)
    check_equal(blockers, "val_shuffle_seed", summary.get("val_shuffle_seed"), EXPECTED_SEED)
    check_equal(blockers, "val_shuffle_buffer_size", summary.get("val_shuffle_buffer_size"), EXPECTED_BUFFER_SIZE)
    check_equal(
        blockers,
        "validation_max_blocks_per_document",
        summary.get("validation_max_blocks_per_document"),
        EXPECTED_MAX_BLOCKS_PER_DOCUMENT,
    )
    check_gt_one_int(blockers, "validation_unique_doc_count", summary.get("validation_unique_doc_count"))
    check_positive_int(blockers, "validation_batches_evaluated", summary.get("validation_batches_evaluated"))
    check_positive_int(blockers, "validation_tokens_evaluated", summary.get("validation_tokens_evaluated"))
    check_equal(blockers, "validation_prefix_only_risk", summary.get("validation_prefix_only_risk"), False)
    check_equal(blockers, "blocker_count", summary.get("blocker_count"), 0)
    check_equal(blockers, "blockers", summary.get("blockers"), [])

    val_data_probe = summary.get("val_data_probe")
    if isinstance(val_data_probe, dict):
        check_equal(blockers, "val_data_probe.sampling_policy", val_data_probe.get("sampling_policy"), EXPECTED_POLICY)
        check_equal(blockers, "val_data_probe.shuffle_seed", val_data_probe.get("shuffle_seed"), EXPECTED_SEED)
        check_equal(blockers, "val_data_probe.shuffle_buffer_size", val_data_probe.get("shuffle_buffer_size"), EXPECTED_BUFFER_SIZE)
        check_equal(
            blockers,
            "val_data_probe.max_blocks_per_document",
            val_data_probe.get("max_blocks_per_document"),
            EXPECTED_MAX_BLOCKS_PER_DOCUMENT,
        )
        check_gt_one_int(blockers, "val_data_probe.unique_doc_count", val_data_probe.get("unique_doc_count"))
    else:
        blockers.append("val_data_probe missing or not an object")


def validate_receipt(receipt: dict[str, Any], blockers: list[str]) -> None:
    check_equal(blockers, "receipt.status", receipt.get("status"), "success")
    check_equal(blockers, "receipt.mode", receipt.get("mode"), EXPECTED_MODE)
    check_equal(blockers, "receipt.cpu_only", receipt.get("cpu_only"), True)
    check_equal(blockers, "receipt.gpu_requested", receipt.get("gpu_requested"), None)
    check_equal(blockers, "receipt.ran_training", receipt.get("ran_training"), False)
    check_equal(blockers, "receipt.produced_checkpoint", receipt.get("produced_checkpoint"), False)
    check_equal(blockers, "receipt.required_commit", receipt.get("required_commit"), EXPECTED_REQUIRED_COMMIT)
    check_equal(blockers, "receipt.val_path_exists", receipt.get("val_path_exists"), True)


def validate_preflight_result(summary_path: Path, receipt_path: Path) -> dict[str, Any]:
    blockers: list[str] = []
    summary = load_json_object(summary_path, blockers, "validation coverage preflight summary")
    receipt = load_json_object(receipt_path, blockers, "Modal preflight receipt")

    if summary:
        validate_summary(summary, blockers)
    if receipt:
        validate_receipt(receipt, blockers)

    result = {
        "validation_status": "passed" if not blockers else "failed",
        "summary_path": relative_path(summary_path),
        "receipt_path": relative_path(receipt_path),
        "preflight_status": summary.get("preflight_status"),
        "used_gpu": summary.get("used_gpu"),
        "ran_training": summary.get("ran_training"),
        "ran_backward": summary.get("ran_backward"),
        "ran_optimizer_step": summary.get("ran_optimizer_step"),
        "saved_checkpoint": summary.get("saved_checkpoint"),
        "val_sampling_policy": summary.get("val_sampling_policy"),
        "val_shuffle_seed": summary.get("val_shuffle_seed"),
        "val_shuffle_buffer_size": summary.get("val_shuffle_buffer_size"),
        "validation_max_blocks_per_document": summary.get("validation_max_blocks_per_document"),
        "validation_unique_doc_count": summary.get("validation_unique_doc_count"),
        "validation_batches_evaluated": summary.get("validation_batches_evaluated"),
        "validation_tokens_evaluated": summary.get("validation_tokens_evaluated"),
        "validation_prefix_only_risk": summary.get("validation_prefix_only_risk"),
        "preflight_blocker_count": summary.get("blocker_count"),
        "preflight_blockers": summary.get("blockers"),
        "blockers": blockers,
        "blocker_count": len(blockers),
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }
    validation_summary_path = summary_path.parent / "validation_coverage_preflight_validation_summary.json"
    validation_summary_path.parent.mkdir(parents=True, exist_ok=True)
    validation_summary_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate the MVP-25.C 5GB validation coverage preflight result.")
    parser.add_argument("--summary-path", default=SUMMARY_PATH.relative_to(PROJECT_ROOT).as_posix())
    parser.add_argument("--receipt-path", default=RECEIPT_PATH.relative_to(PROJECT_ROOT).as_posix())
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = validate_preflight_result(resolve_path(args.summary_path), resolve_path(args.receipt_path))
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["validation_status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
