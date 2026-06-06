from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = REPO_ROOT / "docs"
MATRIX_JSON_PATH = DOCS_DIR / "profiling_matrix.json"
MATRIX_MD_PATH = DOCS_DIR / "profiling_matrix.md"
CANDIDATES_MD_PATH = DOCS_DIR / "next_experiment_candidates.md"

SOURCES = {
    "5gb_3000step_training": REPO_ROOT
    / "experiments"
    / "a100"
    / "fineweb_edu_5gb_300m_3000step_public16k_execute"
    / "results_imported_modal_streaming"
    / "summary.json",
    "seq512_sdpa_50step_profile": REPO_ROOT
    / "experiments"
    / "a100"
    / "fineweb_edu_5gb_300m_50step_public16k_sdpa_profile"
    / "results_imported_modal_streaming"
    / "mvp28_a_sdpa_profile_analysis_summary.json",
    "seq1024_bs4_10step_memory_preflight": REPO_ROOT
    / "experiments"
    / "a100"
    / "fineweb_edu_5gb_300m_10step_public16k_seq1024_sdpa_memory_preflight"
    / "results_imported_modal_streaming"
    / "mvp29_a_seq1024_memory_preflight_analysis_summary.json",
    "seq1024_bs4_50step_sdpa_profile": REPO_ROOT
    / "experiments"
    / "a100"
    / "fineweb_edu_5gb_300m_50step_public16k_seq1024_sdpa_profile"
    / "results_imported_modal_streaming"
    / "mvp30_a_seq1024_sdpa_profile_analysis_summary.json",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def rounded(value: Any) -> Any:
    return round(float(value), 6) if isinstance(value, (int, float)) else value


def rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def row_from_training_summary(summary: dict[str, Any], source_path: Path) -> dict[str, Any]:
    return {
        "id": "5gb_3000step_training",
        "status": "completed_imported",
        "kind": "training",
        "hardware": "Modal A100-40GB",
        "context_length": summary.get("sequence_length"),
        "batch_size": summary.get("batch_size"),
        "grad_accum": summary.get("gradient_accumulation_steps"),
        "max_steps": summary.get("max_steps"),
        "attention_backend": summary.get("declared_model_features", {}).get("attention_backend"),
        "summary_tokens_per_sec": rounded(summary.get("approximate_tokens_per_sec")),
        "mean_step_tokens_per_sec": None,
        "average_step_time_seconds": None,
        "peak_allocated_memory_gib": rounded(summary.get("last_gpu_memory_allocated_gib")),
        "peak_reserved_memory_gib": rounded(summary.get("last_gpu_memory_reserved_gib")),
        "final_train_loss": rounded(summary.get("final_train_loss")),
        "final_validation_loss": rounded(summary.get("final_val_loss")),
        "oom": False,
        "evidence_level": "quality-trend-and-systems",
        "source": rel(source_path),
        "notes": "Longer 5GB training reference; not a profiling-only row.",
    }


def row_from_analysis(row_id: str, kind: str, analysis: dict[str, Any], source_path: Path) -> dict[str, Any]:
    return {
        "id": row_id,
        "status": "completed_imported",
        "kind": kind,
        "hardware": "Modal A100-40GB",
        "context_length": analysis.get("context_length", 512 if row_id.startswith("seq512") else None),
        "batch_size": analysis.get("batch_size", 8 if row_id.startswith("seq512") else None),
        "grad_accum": analysis.get("grad_accum", 4),
        "max_steps": analysis.get("max_steps"),
        "attention_backend": analysis.get("attention_backend"),
        "summary_tokens_per_sec": rounded(analysis.get("summary_tokens_per_sec")),
        "mean_step_tokens_per_sec": rounded(analysis.get("mean_step_tokens_per_sec")),
        "average_step_time_seconds": rounded(analysis.get("average_step_time_seconds")),
        "peak_allocated_memory_gib": rounded(
            analysis.get("peak_allocated_memory_gib", analysis.get("peak_gpu_memory_allocated_gib"))
        ),
        "peak_reserved_memory_gib": rounded(
            analysis.get("peak_reserved_memory_gib", analysis.get("peak_gpu_memory_reserved_gib"))
        ),
        "final_train_loss": rounded(analysis.get("final_train_loss")),
        "final_validation_loss": rounded(analysis.get("final_validation_loss")),
        "oom": bool(analysis.get("oom_detected", False)),
        "evidence_level": "systems-profile" if kind == "profiling" else "memory-preflight",
        "source": rel(source_path),
        "notes": analysis.get("interpretation") or analysis.get("profiling_result_interpretation"),
    }


def planned_candidates() -> list[dict[str, Any]]:
    return [
        {
            "rank": 1,
            "id": "seq1024_batch_size_8_memory_preflight",
            "status": "planned_cost_gate_required",
            "why": "Tests the main unresolved memory question after seq1024 batch_size=4 passed 50-step profiling.",
            "requires_modal_gpu": True,
            "next_step": "Write a plan/config gate first; do not execute without explicit cost approval.",
        },
        {
            "rank": 2,
            "id": "naive_attention_baseline",
            "status": "planned_local_prep_first",
            "why": "Needed before claiming SDPA is faster than a manual baseline.",
            "requires_modal_gpu": False,
            "next_step": "Prepare backend abstraction and small synthetic CPU tests.",
        },
        {
            "rank": 3,
            "id": "flashattention_feasibility",
            "status": "planned_local_prep_first",
            "why": "Clarifies dependency and optional backend boundaries before any GPU comparison.",
            "requires_modal_gpu": False,
            "next_step": "Add availability guard; do not install or require flash_attn in this step.",
        },
        {
            "rank": 4,
            "id": "5gb_5000step_training",
            "status": "deferred_cost_gate_required",
            "why": "Could extend quality trend, but profiling and memory questions should be closed first.",
            "requires_modal_gpu": True,
            "next_step": "Plan only after explicit cost gate and route decision.",
        },
        {
            "rank": 5,
            "id": "adamw_vs_muon",
            "status": "planned_local_prep_first",
            "why": "Requires optimizer registry and guarded Muon implementation before any training comparison.",
            "requires_modal_gpu": False,
            "next_step": "Prepare optimizer registry; do not run training in this phase.",
        },
    ]


def build_matrix() -> dict[str, Any]:
    blockers: list[str] = []
    for source_id, path in SOURCES.items():
        if not path.exists():
            blockers.append(f"missing source for {source_id}: {rel(path)}")

    rows: list[dict[str, Any]] = []
    if not blockers:
        rows.append(row_from_training_summary(load_json(SOURCES["5gb_3000step_training"]), SOURCES["5gb_3000step_training"]))
        rows.append(
            row_from_analysis(
                "seq512_sdpa_50step_profile",
                "profiling",
                load_json(SOURCES["seq512_sdpa_50step_profile"]),
                SOURCES["seq512_sdpa_50step_profile"],
            )
        )
        rows.append(
            row_from_analysis(
                "seq1024_bs4_10step_memory_preflight",
                "memory_preflight",
                load_json(SOURCES["seq1024_bs4_10step_memory_preflight"]),
                SOURCES["seq1024_bs4_10step_memory_preflight"],
            )
        )
        rows.append(
            row_from_analysis(
                "seq1024_bs4_50step_sdpa_profile",
                "profiling",
                load_json(SOURCES["seq1024_bs4_50step_sdpa_profile"]),
                SOURCES["seq1024_bs4_50step_sdpa_profile"],
            )
        )

    return {
        "matrix_status": "passed" if not blockers else "failed",
        "blocker_count": len(blockers),
        "blockers": blockers,
        "generated_artifacts": [
            rel(MATRIX_JSON_PATH),
            rel(MATRIX_MD_PATH),
            rel(CANDIDATES_MD_PATH),
        ],
        "modal_gpu_training_executed": False,
        "tarballs_read": False,
        "rows": rows,
        "candidates": planned_candidates(),
    }


def table_cell(value: Any) -> str:
    if value is None:
        return "N/A"
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def write_markdown(matrix: dict[str, Any]) -> None:
    lines = [
        "# Profiling Matrix",
        "",
        "This file is generated from committed small JSON summaries. It does not read tarballs, checkpoints, raw data, or prepared data.",
        "",
        "## Design Goal",
        "",
        "Keep completed systems evidence and near-term experiment candidates in one reviewable place. The matrix helps decide the next local-prep or cost-gated GPU step without treating short profiling runs as quality evidence.",
        "",
        "## Current Scope",
        "",
        "- Read existing small imported summaries for the 5GB 3000-step run and SDPA profiling/preflight runs.",
        "- Emit a committed JSON matrix and Markdown summary.",
        "- Rank near-term candidates by systems value and risk.",
        "",
        "## Non-goals",
        "",
        "- No Modal execution.",
        "- No GPU execution.",
        "- No training, profiling, or preflight run.",
        "- No tarball, checkpoint, raw-data, or prepared-data reads.",
        "",
        "## Local Validation",
        "",
        "```powershell",
        ".\\.venv\\Scripts\\python.exe -m py_compile scripts\\build_profiling_matrix.py",
        ".\\.venv\\Scripts\\python.exe scripts\\build_profiling_matrix.py",
        "git diff --check",
        "```",
        "",
        "## GPU/Modal Gate",
        "",
        "Future GPU commands are documented as candidates only. They require an explicit user cost gate before execution.",
        "",
        "## Completed Evidence",
        "",
        "| id | kind | context | batch | steps | backend | summary tokens/sec | avg step time | peak reserved GiB | status |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in matrix["rows"]:
        lines.append(
            "| "
            + " | ".join(
                table_cell(row.get(key))
                for key in (
                    "id",
                    "kind",
                    "context_length",
                    "batch_size",
                    "max_steps",
                    "attention_backend",
                    "summary_tokens_per_sec",
                    "average_step_time_seconds",
                    "peak_reserved_memory_gib",
                    "status",
                )
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Boundaries",
            "",
            "- Completed profiling rows are systems evidence, not model-quality evidence.",
            "- SDPA has not been compared against naive attention or FlashAttention yet.",
            "- Future GPU/Modal runs require explicit cost approval.",
            "- Raw result tarballs and checkpoints are intentionally excluded.",
            "",
        ]
    )
    MATRIX_MD_PATH.write_text("\n".join(lines), encoding="utf-8")

    candidate_lines = [
        "# Next Experiment Candidates",
        "",
        "This ranking is a planning aid only. It does not authorize any Modal, GPU, or training run.",
        "",
        "| rank | candidate | status | requires Modal/GPU | why | next step |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for candidate in matrix["candidates"]:
        candidate_lines.append(
            "| "
            + " | ".join(
                table_cell(candidate.get(key))
                for key in ("rank", "id", "status", "requires_modal_gpu", "why", "next_step")
            )
            + " |"
        )
    candidate_lines.extend(
        [
            "",
            "Recommended next branch: `feature/attention-backend-prep` for backend abstraction and local-only checks.",
            "",
        ]
    )
    CANDIDATES_MD_PATH.write_text("\n".join(candidate_lines), encoding="utf-8")


def main() -> int:
    matrix = build_matrix()
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    MATRIX_JSON_PATH.write_text(json.dumps(matrix, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(matrix)
    print(json.dumps(matrix, ensure_ascii=False, indent=2))
    return 0 if matrix["matrix_status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
