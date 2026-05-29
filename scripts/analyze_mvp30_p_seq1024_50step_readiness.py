from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
SEQ1024_ANALYSIS_PATH = (
    REPO_ROOT
    / "experiments"
    / "a100"
    / "fineweb_edu_5gb_300m_10step_public16k_seq1024_sdpa_memory_preflight"
    / "results_imported_modal_streaming"
    / "mvp29_a_seq1024_memory_preflight_analysis_summary.json"
)
SEQ1024_CONFIG_PATH = (
    REPO_ROOT
    / "configs"
    / "a100"
    / "fineweb_edu_5gb_300m_10step_public16k_seq1024_sdpa_memory_preflight.json"
)
SEQ512_PROFILE_CONFIG_PATH = (
    REPO_ROOT
    / "configs"
    / "a100"
    / "fineweb_edu_5gb_300m_50step_public16k_sdpa_profile.json"
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def analyze() -> dict[str, Any]:
    blockers: list[str] = []
    for path in (SEQ1024_ANALYSIS_PATH, SEQ1024_CONFIG_PATH, SEQ512_PROFILE_CONFIG_PATH):
        if not path.exists():
            blockers.append(f"missing required file: {rel(path)}")

    if blockers:
        return {
            "analysis_status": "failed",
            "blocker_count": len(blockers),
            "blockers": blockers,
        }

    source_analysis = load_json(SEQ1024_ANALYSIS_PATH)
    source_config = load_json(SEQ1024_CONFIG_PATH)
    seq512_profile_config = load_json(SEQ512_PROFILE_CONFIG_PATH)

    source_training = source_config.get("training", {}) if isinstance(source_config.get("training"), dict) else {}
    source_model = source_config.get("model", {}) if isinstance(source_config.get("model"), dict) else {}
    source_profiling = source_config.get("profiling", {}) if isinstance(source_config.get("profiling"), dict) else {}
    seq512_training = (
        seq512_profile_config.get("training", {})
        if isinstance(seq512_profile_config.get("training"), dict)
        else {}
    )

    if source_analysis.get("analysis_status") != "passed":
        blockers.append("MVP-29.A seq1024 memory preflight analysis must pass before 50-step planning")
    if source_analysis.get("oom_detected") is not False:
        blockers.append("seq1024 memory preflight must have oom_detected=false")
    if source_analysis.get("context_length") != 1024:
        blockers.append(f"source context_length expected 1024, got {source_analysis.get('context_length')!r}")
    if source_analysis.get("batch_size") != 4:
        blockers.append(f"source batch_size expected 4, got {source_analysis.get('batch_size')!r}")
    if source_analysis.get("attention_backend") != "sdpa":
        blockers.append(f"source attention_backend expected sdpa, got {source_analysis.get('attention_backend')!r}")
    if seq512_training.get("max_steps") != 50:
        blockers.append("seq512 profile reference config should be the existing 50-step profile")
    if source_model.get("context_length") != 1024 or source_training.get("sequence_length") != 1024:
        blockers.append("source config must keep model/training sequence length at 1024")
    if source_profiling.get("attention_backend") != "sdpa":
        blockers.append("source config profiling.attention_backend must be sdpa")

    return {
        "analysis_status": "passed" if not blockers else "failed",
        "blocker_count": len(blockers),
        "source_preflight_context_length": source_analysis.get("context_length"),
        "source_preflight_batch_size": source_analysis.get("batch_size"),
        "source_preflight_grad_accum": source_analysis.get("grad_accum"),
        "source_preflight_oom": source_analysis.get("oom_detected"),
        "source_preflight_summary_tokens_per_sec": source_analysis.get("summary_tokens_per_sec"),
        "source_preflight_peak_reserved_memory_gib": source_analysis.get("peak_reserved_memory_gib"),
        "recommended_context_length": 1024,
        "recommended_batch_size": 4,
        "recommended_grad_accum": 4,
        "recommended_max_steps": 50,
        "recommended_eval_interval": 50,
        "recommended_expected_validation_rows": 1,
        "recommended_attention_backend": "sdpa",
        "direct_seq1024_3000step_recommended": False,
        "seq1024_50step_profile_recommended": True,
        "batch_size_8_first_recommended": False,
        "estimated_cost_category": "low; likely near or slightly above MVP-28 50-step profiling startup-bound cost",
        "recommended_next_mvp": "MVP-30.I add seq1024 50-step SDPA profiling config/mode",
        "blockers": blockers,
    }


def main() -> int:
    result = analyze()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["analysis_status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
