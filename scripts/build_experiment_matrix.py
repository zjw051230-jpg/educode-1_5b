from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = REPO_ROOT / "docs"

MATRIX_JSON_PATH = DOCS_DIR / "experiment_matrix.json"
MATRIX_MD_PATH = DOCS_DIR / "experiment_matrix.md"
NEXT_CANDIDATES_PATH = DOCS_DIR / "next_experiment_candidates.md"


@dataclass(frozen=True)
class CompletedExperimentSource:
    experiment_id: str
    category: str
    summary_path: Path
    description: str


COMPLETED_SOURCES = [
    CompletedExperimentSource(
        experiment_id="mvp27_5gb_3000step_training",
        category="training",
        summary_path=Path(
            "experiments/a100/fineweb_edu_5gb_300m_3000step_public16k_execute/"
            "results_imported_modal_streaming/mvp27_a_analysis_summary.json"
        ),
        description="FineWeb-Edu 5GB 3000-step A100 training analysis",
    ),
    CompletedExperimentSource(
        experiment_id="mvp28_seq512_sdpa_50step_profile",
        category="profiling",
        summary_path=Path(
            "experiments/a100/fineweb_edu_5gb_300m_50step_public16k_sdpa_profile/"
            "results_imported_modal_streaming/mvp28_a_sdpa_profile_analysis_summary.json"
        ),
        description="A100 seq512 batch_size=8 SDPA 50-step profile",
    ),
    CompletedExperimentSource(
        experiment_id="mvp29_seq1024_bs4_10step_memory_preflight",
        category="memory_preflight",
        summary_path=Path(
            "experiments/a100/fineweb_edu_5gb_300m_10step_public16k_seq1024_sdpa_memory_preflight/"
            "results_imported_modal_streaming/mvp29_a_seq1024_memory_preflight_analysis_summary.json"
        ),
        description="A100 seq1024 batch_size=4 SDPA 10-step memory preflight",
    ),
    CompletedExperimentSource(
        experiment_id="mvp30_seq1024_bs4_50step_sdpa_profile",
        category="profiling",
        summary_path=Path(
            "experiments/a100/fineweb_edu_5gb_300m_50step_public16k_seq1024_sdpa_profile/"
            "results_imported_modal_streaming/mvp30_a_seq1024_sdpa_profile_analysis_summary.json"
        ),
        description="A100 seq1024 batch_size=4 SDPA 50-step profile",
    ),
]

PLANNED_CANDIDATES = [
    {
        "experiment_id": "mvp31_seq1024_bs8_memory_preflight",
        "category": "memory_preflight",
        "status": "planned_requires_gpu",
        "priority": 1,
        "requires_gpu": True,
        "requires_modal": True,
        "cost_gate": "required before A100 run",
        "rationale": "Tests whether seq1024 can safely return to batch_size=8 after bs4 no-OOM evidence.",
    },
    {
        "experiment_id": "naive_attention_baseline",
        "category": "attention_backend",
        "status": "planned_local_then_gpu",
        "priority": 2,
        "requires_gpu": False,
        "requires_modal": False,
        "cost_gate": "GPU confirmation needed only for measured profiling",
        "rationale": "Creates a correctness and profiling comparison point for SDPA without claiming speedup yet.",
    },
    {
        "experiment_id": "flashattention_feasibility",
        "category": "attention_backend",
        "status": "planned_local_feasibility",
        "priority": 3,
        "requires_gpu": False,
        "requires_modal": False,
        "cost_gate": "GPU confirmation needed only after dependency feasibility passes",
        "rationale": "Checks optional FlashAttention2 path and install/runtime risks before any A100 comparison.",
    },
    {
        "experiment_id": "adamw_vs_muon_optimizer_prep",
        "category": "optimizer",
        "status": "planned_local_prep",
        "priority": 4,
        "requires_gpu": False,
        "requires_modal": False,
        "cost_gate": "GPU confirmation needed for future training comparison",
        "rationale": "Adds optimizer registry and guarded Muon experiment path while keeping AdamW default.",
    },
    {
        "experiment_id": "moe_routing_prep",
        "category": "moe",
        "status": "planned_local_prep",
        "priority": 5,
        "requires_gpu": False,
        "requires_modal": False,
        "cost_gate": "GPU confirmation needed only after MoE config is explicitly enabled",
        "rationale": "Prepares routing and expert skeleton without changing dense baseline behavior.",
    },
    {
        "experiment_id": "rope_long_context_prep",
        "category": "position_encoding",
        "status": "planned_local_prep",
        "priority": 6,
        "requires_gpu": False,
        "requires_modal": False,
        "cost_gate": "GPU confirmation needed for future long-context profiling",
        "rationale": "Prepares RoPE/position encoding switch for later long-context experiments.",
    },
    {
        "experiment_id": "mvp_future_5gb_5000step_continuation",
        "category": "training",
        "status": "planned_requires_gpu",
        "priority": 7,
        "requires_gpu": True,
        "requires_modal": True,
        "cost_gate": "required before any longer A100 training",
        "rationale": "Possible quality-trend continuation after systems guardrails mature.",
    },
]


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        loaded = json.load(handle)
    if not isinstance(loaded, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return loaded


def completed_row(source: CompletedExperimentSource, summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "experiment_id": source.experiment_id,
        "category": source.category,
        "status": "completed",
        "description": source.description,
        "summary_path": source.summary_path.as_posix(),
        "analysis_status": summary.get("analysis_status"),
        "blocker_count": summary.get("blocker_count"),
        "context_length": summary.get("context_length"),
        "batch_size": summary.get("batch_size"),
        "max_steps": summary.get("max_steps") or summary.get("metrics_rows"),
        "attention_backend": summary.get("attention_backend"),
        "summary_tokens_per_sec": summary.get("summary_tokens_per_sec"),
        "average_step_time_seconds": summary.get("average_step_time_seconds"),
        "peak_allocated_memory_gib": summary.get("peak_allocated_memory_gib"),
        "peak_reserved_memory_gib": summary.get("peak_reserved_memory_gib"),
        "final_train_loss": summary.get("final_train_loss") or summary.get("last_train_loss"),
        "final_validation_loss": summary.get("final_validation_loss") or summary.get("last_validation_loss"),
        "oom_detected": summary.get("oom_detected"),
        "validation_unique_doc_count": summary.get("validation_unique_doc_count"),
        "validation_prefix_only_risk": summary.get("validation_prefix_only_risk"),
    }


def build_matrix(repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    blockers: list[str] = []
    completed: list[dict[str, Any]] = []

    for source in COMPLETED_SOURCES:
        source_path = repo_root / source.summary_path
        if source.summary_path.suffix.lower() == ".gz":
            blockers.append(f"refusing tarball source: {source.summary_path.as_posix()}")
            continue
        if not source_path.exists():
            blockers.append(f"missing summary: {source.summary_path.as_posix()}")
            continue
        completed.append(completed_row(source, load_json(source_path)))

    matrix = {
        "matrix_status": "passed" if not blockers else "failed",
        "blocker_count": len(blockers),
        "blockers": blockers,
        "source_count": len(COMPLETED_SOURCES),
        "completed_count": len(completed),
        "planned_count": len(PLANNED_CANDIDATES),
        "reads_tarballs": False,
        "runs_gpu": False,
        "runs_modal": False,
        "starts_training": False,
        "completed_experiments": completed,
        "planned_experiments": PLANNED_CANDIDATES,
        "recommended_next": "mvp31_seq1024_bs8_memory_preflight",
    }
    return matrix


def render_markdown_table(rows: list[dict[str, Any]]) -> str:
    header = "| Experiment | Status | Shape | Key metrics | Gate |\n| --- | --- | --- | --- | --- |"
    lines = [header]
    for row in rows:
        shape_parts = [
            f"ctx={row.get('context_length')}" if row.get("context_length") else None,
            f"bs={row.get('batch_size')}" if row.get("batch_size") else None,
            f"steps={row.get('max_steps')}" if row.get("max_steps") else None,
            row.get("attention_backend"),
        ]
        shape = ", ".join(part for part in shape_parts if part) or row.get("category", "")
        key_metrics = []
        if row.get("summary_tokens_per_sec") is not None:
            key_metrics.append(f"{row['summary_tokens_per_sec']} tok/s")
        if row.get("average_step_time_seconds") is not None:
            key_metrics.append(f"{row['average_step_time_seconds']}s step")
        if row.get("peak_reserved_memory_gib") is not None:
            key_metrics.append(f"{row['peak_reserved_memory_gib']} GiB reserved")
        if row.get("final_validation_loss") is not None:
            key_metrics.append(f"val_loss={row['final_validation_loss']}")
        gate = row.get("cost_gate", "none")
        lines.append(
            f"| `{row['experiment_id']}` | {row['status']} | {shape} | {', '.join(key_metrics) or 'n/a'} | {gate} |"
        )
    return "\n".join(lines)


def render_matrix_markdown(matrix: dict[str, Any]) -> str:
    rows = matrix["completed_experiments"] + matrix["planned_experiments"]
    return "\n".join(
        [
            "# Experiment Matrix",
            "",
            "This matrix summarizes completed small imported artifacts and future candidates. It does not read result tarballs, run Modal, use GPU, or start training.",
            "",
            f"- Matrix status: `{matrix['matrix_status']}`",
            f"- Blocker count: `{matrix['blocker_count']}`",
            f"- Completed experiments: `{matrix['completed_count']}`",
            f"- Planned candidates: `{matrix['planned_count']}`",
            f"- Recommended next: `{matrix['recommended_next']}`",
            "",
            render_markdown_table(rows),
            "",
        ]
    )


def render_candidates_markdown(matrix: dict[str, Any]) -> str:
    candidates = sorted(matrix["planned_experiments"], key=lambda row: row["priority"])
    lines = [
        "# Next Experiment Candidates",
        "",
        "These are planning candidates only. Any GPU or Modal run requires a separate cost gate and explicit user confirmation.",
        "",
    ]
    for candidate in candidates:
        lines.extend(
            [
                f"## {candidate['priority']}. {candidate['experiment_id']}",
                "",
                f"- Status: `{candidate['status']}`",
                f"- Category: `{candidate['category']}`",
                f"- Requires GPU: `{candidate['requires_gpu']}`",
                f"- Requires Modal: `{candidate['requires_modal']}`",
                f"- Cost gate: {candidate['cost_gate']}",
                f"- Rationale: {candidate['rationale']}",
                "",
            ]
        )
    return "\n".join(lines)


def write_outputs(matrix: dict[str, Any]) -> None:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    MATRIX_JSON_PATH.write_text(json.dumps(matrix, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    MATRIX_MD_PATH.write_text(render_matrix_markdown(matrix), encoding="utf-8")
    NEXT_CANDIDATES_PATH.write_text(render_candidates_markdown(matrix), encoding="utf-8")


def main() -> int:
    matrix = build_matrix()
    write_outputs(matrix)
    print(json.dumps({k: matrix[k] for k in ("matrix_status", "blocker_count", "completed_count", "planned_count", "recommended_next")}, indent=2, sort_keys=True))
    return 0 if matrix["blocker_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
