# draft_status: candidate
# topic_id: B05-RTS-0077
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC-4
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only
# batch_id: domain_synthetic_batch_05

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean


@dataclass
class DiagnosticResult:
    topic_id: str
    title: str
    suspicious: bool
    diagnosis: str
    evidence: list[str]


def build_packet_eval_cadence_checkpoint_interval_config_review() -> dict:
    return {
        "topic_id": "B05-RTS-0077",
        "title": "Eval Cadence And Save Interval",
        "learning_objective": "Review how eval_every and save_every interact in a config block and predict the artifact schedule.",
        "writing_form": "code walkthrough",
        "concrete_anchor": "before/after comparison",
        "artifact_focus": "config snippet + expected timeline",
        "step": 12385,
        "seq_len": 3072,
        "max_memory_allocated_gb": 42.0,
        "max_memory_reserved_gb": 68.5,
        "peak_reserved_gb": 71.3,
        "train_tokens_per_sec": 155270,
        "val_loss": 2.2,
        "weighted_val_loss": 2.169,
        "latest_step": 12387,
        "best_step": 12361,
        "optimizer_step": 12383,
        "event_rows": [
            {"event": "train_step", "step": 12385, "tokens_per_sec": 155270},
            {"event": "eval_end", "step": 12386, "val_loss": 2.2, "samples": 512},
            {"event": "checkpoint_save", "step": 12387, "duration_ms": 621},
        ],
    }


def estimate_memory_headroom_gb(packet: dict, capacity_gb: float = 80.0) -> float:
    return round(capacity_gb - packet["peak_reserved_gb"], 2)


def detect_counter_gap(packet: dict) -> int:
    return packet["latest_step"] - packet["optimizer_step"]


def classify_metric_alignment(packet: dict) -> str:
    if abs(packet["val_loss"] - packet["weighted_val_loss"]) > 0.025:
        return "aggregation_mismatch"
    if packet["latest_step"] < packet["best_step"]:
        return "stale_summary_field"
    return "aligned_enough_for_review"


def diagnose_eval_cadence_checkpoint_interval_config_review(packet: dict) -> DiagnosticResult:
    evidence: list[str] = []
    suspicious = False

    counter_gap = detect_counter_gap(packet)
    if counter_gap > 2:
        suspicious = True
        evidence.append(f"latest_step leads optimizer_step by {counter_gap}")

    if packet["max_memory_reserved_gb"] - packet["max_memory_allocated_gb"] > 20.0:
        suspicious = True
        evidence.append("reserved memory is much higher than allocated memory")

    alignment = classify_metric_alignment(packet)
    if alignment != "aligned_enough_for_review":
        suspicious = True
        evidence.append(f"metric alignment status: {alignment}")

    headroom = estimate_memory_headroom_gb(packet)
    if headroom < 4.0:
        suspicious = True
        evidence.append(f"peak reserved leaves only {headroom} GB headroom on A100")

    diagnosis = (
        "topic-specific packet needs follow-up because the artifact set suggests a bounded runtime inconsistency"
        if suspicious
        else "packet is internally coherent enough for draft review, but still bounded to the named artifact"
    )
    return DiagnosticResult(
        topic_id=packet["topic_id"],
        title=packet["title"],
        suspicious=suspicious,
        diagnosis=diagnosis,
        evidence=evidence,
    )


def render_packet_summary(packet: dict) -> str:
    values = [packet["max_memory_allocated_gb"], packet["max_memory_reserved_gb"], packet["peak_reserved_gb"]]
    return (
        f"{packet['topic_id']} :: mean_memory_gb={mean(values):.2f} "
        f"counter_gap={detect_counter_gap(packet)} alignment={classify_metric_alignment(packet)}"
    )


def main() -> None:
    packet = build_packet_eval_cadence_checkpoint_interval_config_review()
    result = diagnose_eval_cadence_checkpoint_interval_config_review(packet)
    print(render_packet_summary(packet))
    print({
        "topic_id": result.topic_id,
        "title": result.title,
        "suspicious": result.suspicious,
        "diagnosis": result.diagnosis,
        "evidence": result.evidence,
    })


if __name__ == "__main__":
    main()
