# draft_status: candidate
# topic_id: B05-RTS-0093
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


def build_packet_memory_chart_vs_allocator_trace_reconciliation() -> dict:
    return {
        "topic_id": "B05-RTS-0093",
        "title": "Memory Chart And Allocator Trace",
        "learning_objective": "Reconcile a high-level memory chart with allocator trace rows when the two appear to tell different stories.",
        "writing_form": "config review",
        "concrete_anchor": "numeric toy example",
        "artifact_focus": "chart summary + allocator rows",
        "step": 12465,
        "seq_len": 3072,
        "max_memory_allocated_gb": 42.0,
        "max_memory_reserved_gb": 64.3,
        "peak_reserved_gb": 67.1,
        "train_tokens_per_sec": 163430,
        "val_loss": 2.04,
        "weighted_val_loss": 2.009,
        "latest_step": 12467,
        "best_step": 12441,
        "optimizer_step": 12462,
        "event_rows": [
            {"event": "train_step", "step": 12465, "tokens_per_sec": 163430},
            {"event": "eval_end", "step": 12466, "val_loss": 2.04, "samples": 512},
            {"event": "checkpoint_save", "step": 12467, "duration_ms": 669},
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


def diagnose_memory_chart_vs_allocator_trace_reconciliation(packet: dict) -> DiagnosticResult:
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
    packet = build_packet_memory_chart_vs_allocator_trace_reconciliation()
    result = diagnose_memory_chart_vs_allocator_trace_reconciliation(packet)
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
