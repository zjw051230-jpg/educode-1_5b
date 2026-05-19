# draft_status: candidate
# topic_id: B05-RTS-0078
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


def build_packet_throughput_fell_after_checkpoint_multi_signal_triage() -> dict:
    return {
        "topic_id": "B05-RTS-0078",
        "title": "Throughput Fell After Checkpoint",
        "learning_objective": "Use logs, throughput rows, and save timing to triage why step latency stayed elevated after a checkpoint.",
        "writing_form": "comparison table",
        "concrete_anchor": "decision checklist",
        "artifact_focus": "save log + timing table",
        "step": 12390,
        "seq_len": 4096,
        "max_memory_allocated_gb": 43.2,
        "max_memory_reserved_gb": 59.2,
        "peak_reserved_gb": 62.0,
        "train_tokens_per_sec": 155780,
        "val_loss": 2.12,
        "weighted_val_loss": 2.089,
        "latest_step": 12392,
        "best_step": 12366,
        "optimizer_step": 12387,
        "event_rows": [
            {"event": "train_step", "step": 12390, "tokens_per_sec": 155780},
            {"event": "eval_end", "step": 12391, "val_loss": 2.12, "samples": 512},
            {"event": "checkpoint_save", "step": 12392, "duration_ms": 624},
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


def diagnose_throughput_fell_after_checkpoint_multi_signal_triage(packet: dict) -> DiagnosticResult:
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
    packet = build_packet_throughput_fell_after_checkpoint_multi_signal_triage()
    result = diagnose_throughput_fell_after_checkpoint_multi_signal_triage(packet)
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
