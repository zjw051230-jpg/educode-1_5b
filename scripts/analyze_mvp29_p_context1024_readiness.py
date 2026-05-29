from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
BASELINE_ANALYSIS_PATH = (
    REPO_ROOT
    / "experiments"
    / "a100"
    / "fineweb_edu_5gb_300m_50step_public16k_sdpa_profile"
    / "results_imported_modal_streaming"
    / "mvp28_a_sdpa_profile_analysis_summary.json"
)
BASELINE_CONFIG_PATH = (
    REPO_ROOT
    / "configs"
    / "a100"
    / "fineweb_edu_5gb_300m_50step_public16k_sdpa_profile.json"
)
TRAIN_3000_CONFIG_PATH = (
    REPO_ROOT
    / "configs"
    / "a100"
    / "fineweb_edu_5gb_300m_3000step_public16k_execute.json"
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def analyze() -> dict[str, Any]:
    blockers: list[str] = []
    for path in (BASELINE_ANALYSIS_PATH, BASELINE_CONFIG_PATH, TRAIN_3000_CONFIG_PATH):
        if not path.exists():
            blockers.append(f"missing required file: {rel(path)}")

    if blockers:
        return {
            "analysis_status": "failed",
            "blocker_count": len(blockers),
            "blockers": blockers,
        }

    baseline_analysis = load_json(BASELINE_ANALYSIS_PATH)
    baseline_config = load_json(BASELINE_CONFIG_PATH)
    train_3000_config = load_json(TRAIN_3000_CONFIG_PATH)

    baseline_context_length = int(baseline_config["model"]["context_length"])
    target_context_length = 1024
    baseline_batch_size = int(baseline_config["training"]["batch_size"])
    baseline_grad_accum = int(baseline_config["training"]["gradient_accumulation_steps"])
    baseline_attention_backend = baseline_config["profiling"].get("attention_backend")
    train_3000_context_length = int(train_3000_config["model"]["context_length"])

    recommended_batch_size = 4
    recommended_grad_accum = 4
    recommended_preflight_steps = 10
    estimated_attention_memory_multiplier = (target_context_length / baseline_context_length) ** 2
    baseline_tokens_per_step = baseline_batch_size * baseline_context_length * baseline_grad_accum
    recommended_tokens_per_step = recommended_batch_size * target_context_length * recommended_grad_accum

    if baseline_analysis.get("analysis_status") != "passed":
        blockers.append("MVP-28.A baseline analysis must be passed before seq1024 planning")
    if baseline_context_length != 512:
        blockers.append(f"baseline context_length expected 512, got {baseline_context_length}")
    if train_3000_context_length != 512:
        blockers.append(f"5GB 3000-step reference context_length expected 512, got {train_3000_context_length}")
    if baseline_attention_backend != "sdpa":
        blockers.append(f"baseline attention backend expected sdpa, got {baseline_attention_backend!r}")

    return {
        "analysis_status": "passed" if not blockers else "failed",
        "blocker_count": len(blockers),
        "baseline_context_length": baseline_context_length,
        "target_context_length": target_context_length,
        "baseline_peak_allocated_memory_gib": baseline_analysis.get("peak_allocated_memory_gib"),
        "baseline_peak_reserved_memory_gib": baseline_analysis.get("peak_reserved_memory_gib"),
        "estimated_attention_memory_multiplier": round(estimated_attention_memory_multiplier, 2),
        "baseline_batch_size": baseline_batch_size,
        "baseline_grad_accum": baseline_grad_accum,
        "baseline_tokens_per_optimizer_step": baseline_tokens_per_step,
        "recommended_preflight_steps": recommended_preflight_steps,
        "recommended_batch_size": recommended_batch_size,
        "recommended_grad_accum": recommended_grad_accum,
        "recommended_tokens_per_optimizer_step": recommended_tokens_per_step,
        "recommended_attention_backend": "sdpa",
        "direct_3000step_seq1024_recommended": False,
        "recommended_next_mvp": "MVP-29.I add seq1024 10-step SDPA memory preflight config/mode",
        "blockers": blockers,
    }


def main() -> int:
    result = analyze()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["analysis_status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
