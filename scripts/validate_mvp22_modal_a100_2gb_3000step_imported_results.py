from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
IMPORT_DIR = (
    PROJECT_ROOT
    / "experiments"
    / "a100"
    / "fineweb_edu_2gb_300m_3000step_public16k_execute"
    / "results_imported_modal_streaming"
)
OUTPUT_PATH = IMPORT_DIR / "import_validation_summary.json"

EXPECTED_EXACT_PARAMETER_COUNT = 336106496
EXPECTED_MAX_STEPS = 3000
EXPECTED_BATCH_SIZE = 8
EXPECTED_GRADIENT_ACCUMULATION_STEPS = 4
EXPECTED_TOKENIZER_VOCAB_SIZE = 16384


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def count_jsonl_rows(path: Path) -> int:
    with path.open("r", encoding="utf-8") as handle:
        return sum(1 for line in handle if line.strip())


def require(condition: bool, message: str, blockers: list[str]) -> None:
    if not condition:
        blockers.append(message)


def validate_imported_results() -> dict[str, Any]:
    blockers: list[str] = []
    required_files = [
        "summary.json",
        "summary.md",
        "metrics.jsonl",
        "validation_metrics.jsonl",
        "run_config.json",
        "run_metadata.json",
        "post_run_artifact_validation_summary.json",
    ]
    for filename in required_files:
        require((IMPORT_DIR / filename).exists(), f"missing imported file: {filename}", blockers)

    if blockers:
        return build_result({}, {}, 0, 0, blockers)

    summary = load_json(IMPORT_DIR / "summary.json")
    post_run_validation = load_json(IMPORT_DIR / "post_run_artifact_validation_summary.json")
    metrics_rows_actual = count_jsonl_rows(IMPORT_DIR / "metrics.jsonl")
    validation_rows_actual = count_jsonl_rows(IMPORT_DIR / "validation_metrics.jsonl")

    require(summary.get("success") is True, "summary success must be true", blockers)
    require(summary.get("runtime_device") == "cuda", "runtime_device must be cuda", blockers)
    require(summary.get("runtime_dtype") == "bf16", "runtime_dtype must be bf16", blockers)
    require(
        summary.get("exact_parameter_count") == EXPECTED_EXACT_PARAMETER_COUNT,
        f"exact_parameter_count must be {EXPECTED_EXACT_PARAMETER_COUNT}",
        blockers,
    )
    require(summary.get("max_steps") == EXPECTED_MAX_STEPS, f"max_steps must be {EXPECTED_MAX_STEPS}", blockers)
    require(summary.get("batch_size") == EXPECTED_BATCH_SIZE, f"batch_size must be {EXPECTED_BATCH_SIZE}", blockers)
    require(
        summary.get("gradient_accumulation_steps") == EXPECTED_GRADIENT_ACCUMULATION_STEPS,
        f"gradient_accumulation_steps must be {EXPECTED_GRADIENT_ACCUMULATION_STEPS}",
        blockers,
    )
    require(summary.get("data_loading_mode") == "streaming", "data_loading_mode must be streaming", blockers)
    require(
        summary.get("tokenizer_vocab_size") == EXPECTED_TOKENIZER_VOCAB_SIZE,
        f"tokenizer_vocab_size must be {EXPECTED_TOKENIZER_VOCAB_SIZE}",
        blockers,
    )
    require(summary.get("metrics_rows") == EXPECTED_MAX_STEPS, f"metrics_rows must be {EXPECTED_MAX_STEPS}", blockers)
    require(
        validation_rows_actual == summary.get("validation_rows"),
        "validation_metrics.jsonl row count must match summary validation_rows",
        blockers,
    )
    require(
        metrics_rows_actual == summary.get("metrics_rows"),
        "metrics.jsonl row count must match summary metrics_rows",
        blockers,
    )
    require(summary.get("loss_all_finite") is True, "loss_all_finite must be true", blockers)
    require(summary.get("val_loss_all_finite") is True, "val_loss_all_finite must be true", blockers)
    require(summary.get("grad_all_finite") is True, "grad_all_finite must be true", blockers)
    require(summary.get("checkpoint_reload_match") is True, "checkpoint_reload_match must be true", blockers)

    embedded_validation = summary.get("post_run_artifact_validation")
    require(isinstance(embedded_validation, dict), "summary post_run_artifact_validation must be present", blockers)
    if isinstance(embedded_validation, dict):
        require(
            embedded_validation.get("passed") is True,
            "summary post_run_artifact_validation.passed must be true",
            blockers,
        )
    require(
        post_run_validation.get("status") == "success",
        "post_run_artifact_validation_summary status must be success",
        blockers,
    )
    require(
        post_run_validation.get("blocker_count") == 0,
        "post_run_artifact_validation_summary blocker_count must be 0",
        blockers,
    )
    require(
        post_run_validation.get("metrics_rows_actual") == summary.get("metrics_rows"),
        "post_run_artifact_validation_summary metrics rows must match summary",
        blockers,
    )
    require(
        post_run_validation.get("validation_rows_actual") == summary.get("validation_rows"),
        "post_run_artifact_validation_summary validation rows must match summary",
        blockers,
    )

    return build_result(summary, post_run_validation, metrics_rows_actual, validation_rows_actual, blockers)


def build_result(
    summary: dict[str, Any],
    post_run_validation: dict[str, Any],
    metrics_rows_actual: int,
    validation_rows_actual: int,
    blockers: list[str],
) -> dict[str, Any]:
    return {
        "validation_status": "passed" if not blockers else "failed",
        "blockers": blockers,
        "blocker_count": len(blockers),
        "import_dir": IMPORT_DIR.relative_to(PROJECT_ROOT).as_posix(),
        "run_id": summary.get("run_id"),
        "runtime_device": summary.get("runtime_device"),
        "runtime_dtype": summary.get("runtime_dtype"),
        "exact_parameter_count": summary.get("exact_parameter_count"),
        "max_steps": summary.get("max_steps"),
        "batch_size": summary.get("batch_size"),
        "gradient_accumulation_steps": summary.get("gradient_accumulation_steps"),
        "data_loading_mode": summary.get("data_loading_mode"),
        "tokenizer_vocab_size": summary.get("tokenizer_vocab_size"),
        "metrics_rows_summary": summary.get("metrics_rows"),
        "metrics_rows_actual": metrics_rows_actual,
        "validation_rows_summary": summary.get("validation_rows"),
        "validation_rows_actual": validation_rows_actual,
        "loss_all_finite": summary.get("loss_all_finite"),
        "val_loss_all_finite": summary.get("val_loss_all_finite"),
        "grad_all_finite": summary.get("grad_all_finite"),
        "checkpoint_reload_match": summary.get("checkpoint_reload_match"),
        "post_run_artifact_validation_passed": summary.get("post_run_artifact_validation", {}).get("passed"),
        "post_run_artifact_validation_summary_status": post_run_validation.get("status"),
        "post_run_artifact_validation_summary_blocker_count": post_run_validation.get("blocker_count"),
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }


def main() -> int:
    result = validate_imported_results()
    OUTPUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"validation_status={result['validation_status']}")
    print(f"blockers={result['blocker_count']}")
    print(f"import_validation_summary_path={OUTPUT_PATH.relative_to(PROJECT_ROOT).as_posix()}")
    return 0 if result["validation_status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
