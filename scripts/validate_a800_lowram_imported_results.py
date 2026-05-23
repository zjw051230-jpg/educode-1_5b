from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXPECTED_PARAMETER_COUNT = 336106496
EXPECTED_TOKENIZER_VOCAB_SIZE = 16384
EXPECTED_BATCH_SIZE = 1
EXPECTED_GRADIENT_ACCUMULATION_STEPS = 1

RUN_SPECS = [
    {
        "label": "MVP-14",
        "output_dir": PROJECT_ROOT / "experiments" / "a100" / "fineweb_edu_500mb_300m_1000step_public16k_execute",
        "import_dir_name": "results_imported_lowram",
        "expected_max_steps": 1000,
        "expected_metrics_rows": 1000,
        "expected_validation_rows_min": 10,
        "expected_validation_rows_exact": 10,
    },
    {
        "label": "MVP-15",
        "output_dir": PROJECT_ROOT / "experiments" / "a100" / "fineweb_edu_500mb_300m_3000step_public16k_execute",
        "import_dir_name": "results_imported_lowram",
        "expected_max_steps": 3000,
        "expected_metrics_rows": 3000,
        "expected_validation_rows_min": 10,
        "expected_validation_rows_exact": None,
    },
]

REQUIRED_IMPORTED_FILES = [
    "summary.json",
    "summary.md",
    "metrics.jsonl",
    "validation_metrics.jsonl",
    "run_config.json",
    "run_metadata.json",
    "post_run_artifact_validation_summary.json",
]


def repo_relative_path(path: Path) -> str:
    try:
        return path.relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def count_jsonl_rows(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open("r", encoding="utf-8") as handle:
        return sum(1 for line in handle if line.strip())


def require(condition: bool, message: str, blockers: list[str]) -> None:
    if not condition:
        blockers.append(message)


def validate_run(spec: dict[str, Any]) -> dict[str, Any]:
    import_dir = spec["output_dir"] / spec["import_dir_name"]
    summary_path = import_dir / "summary.json"
    metrics_path = import_dir / "metrics.jsonl"
    validation_metrics_path = import_dir / "validation_metrics.jsonl"
    post_run_validation_path = import_dir / "post_run_artifact_validation_summary.json"
    import_validation_path = import_dir / "import_validation_summary.json"
    blockers: list[str] = []

    for filename in REQUIRED_IMPORTED_FILES:
        require((import_dir / filename).exists(), f"missing imported file: {filename}", blockers)

    summary: dict[str, Any] = load_json(summary_path) if summary_path.exists() else {}
    post_run_validation: dict[str, Any] = load_json(post_run_validation_path) if post_run_validation_path.exists() else {}
    metrics_rows_actual = count_jsonl_rows(metrics_path)
    validation_rows_actual = count_jsonl_rows(validation_metrics_path)

    if summary:
        expected_max_steps = int(spec["expected_max_steps"])
        expected_metrics_rows = int(spec["expected_metrics_rows"])
        expected_validation_rows_min = int(spec["expected_validation_rows_min"])
        expected_validation_rows_exact = spec["expected_validation_rows_exact"]

        require(summary.get("success") is True, "summary.success must be true", blockers)
        require(summary.get("runtime_device") == "cuda", "runtime_device must be cuda", blockers)
        require(summary.get("runtime_dtype") == "bf16", "runtime_dtype must be bf16", blockers)
        require(summary.get("exact_parameter_count") == EXPECTED_PARAMETER_COUNT, "exact_parameter_count must be 336106496", blockers)
        require(summary.get("batch_size") == EXPECTED_BATCH_SIZE, "batch_size must be 1 for low-RAM fallback", blockers)
        require(
            summary.get("gradient_accumulation_steps") == EXPECTED_GRADIENT_ACCUMULATION_STEPS,
            "gradient_accumulation_steps must be 1 for low-RAM fallback",
            blockers,
        )
        require(summary.get("max_steps") == expected_max_steps, f"max_steps must be {expected_max_steps}", blockers)
        require(summary.get("metrics_rows") == expected_metrics_rows, f"metrics_rows must be {expected_metrics_rows}", blockers)
        require(metrics_rows_actual == summary.get("metrics_rows"), "metrics.jsonl actual rows must equal summary metrics_rows", blockers)
        require(
            validation_rows_actual == summary.get("validation_rows"),
            "validation_metrics.jsonl actual rows must equal summary validation_rows",
            blockers,
        )
        require(summary.get("validation_rows", 0) >= expected_validation_rows_min, "validation_rows must be at least 10", blockers)
        if expected_validation_rows_exact is not None:
            require(
                summary.get("validation_rows") == expected_validation_rows_exact,
                f"validation_rows must be {expected_validation_rows_exact}",
                blockers,
            )
        require(summary.get("loss_all_finite") is True, "loss_all_finite must be true", blockers)
        require(summary.get("val_loss_all_finite") is True, "val_loss_all_finite must be true", blockers)
        require(summary.get("grad_all_finite") is True, "grad_all_finite must be true", blockers)
        require(summary.get("checkpoint_reload_match") is True, "checkpoint_reload_match must be true", blockers)
        require(summary.get("tokenizer_vocab_size") == EXPECTED_TOKENIZER_VOCAB_SIZE, "tokenizer_vocab_size must be 16384", blockers)
        require(
            summary.get("post_run_artifact_validation", {}).get("passed") is True,
            "summary.post_run_artifact_validation.passed must be true",
            blockers,
        )

    if post_run_validation:
        require(post_run_validation.get("status") == "success", "post_run_artifact_validation_summary.status must be success", blockers)
        require(post_run_validation.get("blocker_count") == 0, "post_run artifact validation blocker_count must be 0", blockers)
        require(post_run_validation.get("ready_for_review") is True, "post_run artifact validation ready_for_review must be true", blockers)

    result = {
        "validation_status": "passed" if not blockers else "failed",
        "label": spec["label"],
        "import_dir": repo_relative_path(import_dir),
        "summary_path": repo_relative_path(summary_path),
        "metrics_path": repo_relative_path(metrics_path),
        "validation_metrics_path": repo_relative_path(validation_metrics_path),
        "post_run_artifact_validation_summary_path": repo_relative_path(post_run_validation_path),
        "run_id": summary.get("run_id") if summary else None,
        "run_name": summary.get("run_name") if summary else None,
        "runtime_device": summary.get("runtime_device") if summary else None,
        "runtime_dtype": summary.get("runtime_dtype") if summary else None,
        "exact_parameter_count": summary.get("exact_parameter_count") if summary else None,
        "max_steps": summary.get("max_steps") if summary else None,
        "batch_size": summary.get("batch_size") if summary else None,
        "gradient_accumulation_steps": summary.get("gradient_accumulation_steps") if summary else None,
        "tokens_seen": summary.get("tokens_seen") if summary else None,
        "first_train_loss": summary.get("first_train_loss") if summary else None,
        "final_train_loss": summary.get("final_train_loss") if summary else None,
        "final_val_loss": summary.get("final_val_loss") if summary else None,
        "metrics_rows_summary": summary.get("metrics_rows") if summary else None,
        "metrics_rows_actual": metrics_rows_actual,
        "validation_rows_summary": summary.get("validation_rows") if summary else None,
        "validation_rows_actual": validation_rows_actual,
        "loss_all_finite": summary.get("loss_all_finite") if summary else None,
        "val_loss_all_finite": summary.get("val_loss_all_finite") if summary else None,
        "grad_all_finite": summary.get("grad_all_finite") if summary else None,
        "checkpoint_reload_match": summary.get("checkpoint_reload_match") if summary else None,
        "post_run_artifact_validation_passed": summary.get("post_run_artifact_validation", {}).get("passed") if summary else None,
        "post_run_artifact_validation_status": post_run_validation.get("status") if post_run_validation else None,
        "blockers": blockers,
        "blocker_count": len(blockers),
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }
    write_json(import_validation_path, result)
    return result


def main() -> int:
    results = [validate_run(spec) for spec in RUN_SPECS]
    total_blockers = sum(int(result["blocker_count"]) for result in results)
    for result in results:
        print(f"{result['label']} validation_status={result['validation_status']}")
        print(f"{result['label']} blockers={result['blocker_count']}")
        print(f"{result['label']} max_steps={result['max_steps']}")
        print(f"{result['label']} metrics_rows_actual={result['metrics_rows_actual']}")
        print(f"{result['label']} validation_rows_actual={result['validation_rows_actual']}")
        print(f"{result['label']} final_train_loss={result['final_train_loss']}")
        print(f"{result['label']} final_val_loss={result['final_val_loss']}")
    print(f"total_blockers={total_blockers}")
    return 0 if total_blockers == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
