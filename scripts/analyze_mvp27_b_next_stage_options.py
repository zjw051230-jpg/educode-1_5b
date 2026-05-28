from __future__ import annotations

import json
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MVP27_A_SUMMARY = (
    PROJECT_ROOT
    / "experiments"
    / "a100"
    / "fineweb_edu_5gb_300m_3000step_public16k_execute"
    / "results_imported_modal_streaming"
    / "mvp27_a_analysis_summary.json"
)


OPTIONS: list[dict[str, Any]] = [
    {
        "id": "D",
        "name": "SDPA / FlashAttention profiling",
        "recommended_mvp": "MVP-28",
        "technical_value": 5,
        "resume_value": 5,
        "risk": 2,
        "cost": 2,
        "requires_gpu": True,
        "requires_new_code": True,
        "depends_on_5gb_3000": True,
        "cost_category": "low-to-medium",
        "rationale": "Adds CS336-style systems depth and can be bounded with profiling/preflight rather than long training.",
    },
    {
        "id": "C",
        "name": "context length 512 -> 1024",
        "recommended_mvp": "MVP-29",
        "technical_value": 5,
        "resume_value": 4,
        "risk": 3,
        "cost": 3,
        "requires_gpu": True,
        "requires_new_code": False,
        "depends_on_5gb_3000": True,
        "cost_category": "medium",
        "rationale": "Tests memory and throughput consequences of a more realistic context length after profiling baseline is prepared.",
    },
    {
        "id": "A",
        "name": "5GB 5000-step continuation",
        "recommended_mvp": "MVP-30 candidate",
        "technical_value": 3,
        "resume_value": 3,
        "risk": 2,
        "cost": 3,
        "requires_gpu": True,
        "requires_new_code": False,
        "depends_on_5gb_3000": True,
        "cost_category": "medium",
        "rationale": "Direct continuation is low risk, but adds less technical range than profiling or context work.",
    },
    {
        "id": "B",
        "name": "AdamW vs Muon optimizer experiment",
        "recommended_mvp": "MVP-30 candidate",
        "technical_value": 4,
        "resume_value": 5,
        "risk": 4,
        "cost": 3,
        "requires_gpu": False,
        "requires_new_code": True,
        "depends_on_5gb_3000": False,
        "cost_category": "low before training",
        "rationale": "Strong technical point, but needs implementation and local validation before any larger run.",
    },
    {
        "id": "E",
        "name": "B200 300M/1B scale plan",
        "recommended_mvp": "later planning",
        "technical_value": 4,
        "resume_value": 4,
        "risk": 4,
        "cost": 5,
        "requires_gpu": False,
        "requires_new_code": False,
        "depends_on_5gb_3000": True,
        "cost_category": "planning low, execution high",
        "rationale": "Important for the 1.5B route, but should wait for stronger A100 systems/profiling baselines.",
    },
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def option_score(option: dict[str, Any]) -> int:
    return int(option["technical_value"]) + int(option["resume_value"]) - int(option["risk"]) - int(option["cost"])


def analyze() -> dict[str, Any]:
    blockers: list[str] = []
    if not MVP27_A_SUMMARY.exists():
        blockers.append(f"missing MVP-27.A analysis summary: {MVP27_A_SUMMARY.relative_to(PROJECT_ROOT).as_posix()}")
        mvp27_a = {}
    else:
        mvp27_a = load_json(MVP27_A_SUMMARY)

    if mvp27_a.get("analysis_status") != "passed":
        blockers.append(f"MVP-27.A analysis must be passed, got {mvp27_a.get('analysis_status')!r}")
    if mvp27_a.get("validation_prefix_only_risk") is not False:
        blockers.append("MVP-27.A validation_prefix_only_risk must be false before route selection")
    if not isinstance(mvp27_a.get("validation_unique_doc_count"), int) or mvp27_a.get("validation_unique_doc_count") <= 1:
        blockers.append("MVP-27.A validation_unique_doc_count must be greater than 1")

    ranked_options = sorted(
        (
            {
                "rank": 0,
                "id": option["id"],
                "name": option["name"],
                "score": option_score(option),
                "recommended_mvp": option["recommended_mvp"],
                "requires_gpu": option["requires_gpu"],
                "requires_new_code": option["requires_new_code"],
                "estimated_cost_category": option["cost_category"],
                "rationale": option["rationale"],
            }
            for option in OPTIONS
        ),
        key=lambda row: (-row["score"], row["id"]),
    )
    for index, option in enumerate(ranked_options, start=1):
        option["rank"] = index

    result = {
        "analysis_status": "passed" if not blockers else "failed",
        "blocker_count": len(blockers),
        "blockers": blockers,
        "recommended_next_mvp": "MVP-28: SDPA / FlashAttention profiling plan + preflight",
        "recommended_mvp_29": "MVP-29: context length 512 -> 1024 memory/preflight",
        "recommended_mvp_30": "MVP-30: choose between 5GB 5000-step continuation and AdamW vs Muon",
        "ranked_options": ranked_options,
        "direct_10000step_recommended": False,
        "reason_not_10000step": (
            "The 3000-step run improved loss and validation coverage, but it is still one bounded run. "
            "A direct 10000-step spend would add steps without first improving systems profiling, context-length evidence, "
            "or optimizer comparison depth."
        ),
        "next_step_requires_gpu": True,
        "next_step_estimated_cost_category": "low-to-medium; profiling/preflight should be bounded and cheaper than long training",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def main() -> int:
    result = analyze()
    return 0 if result["analysis_status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
