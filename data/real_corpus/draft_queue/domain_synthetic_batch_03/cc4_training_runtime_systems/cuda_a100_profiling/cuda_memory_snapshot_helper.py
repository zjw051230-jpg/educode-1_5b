# draft_status: candidate
# topic_id: RTS-013
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC4
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only


def build_memory_snapshot(step, allocated_gb, reserved_gb, max_allocated_gb):
    return {
        "step": step,
        "cuda_allocated_gb": round(float(allocated_gb), 2),
        "cuda_reserved_gb": round(float(reserved_gb), 2),
        "cuda_max_allocated_gb": round(float(max_allocated_gb), 2),
    }


def summarize_snapshots(rows):
    if not rows:
        return {"count": 0, "max_reserved_gb": 0.0}
    return {
        "count": len(rows),
        "max_reserved_gb": max(row["cuda_reserved_gb"] for row in rows),
        "max_allocated_gb": max(row["cuda_allocated_gb"] for row in rows),
    }


snapshots = [
    build_memory_snapshot(step=1, allocated_gb=8.2, reserved_gb=9.5, max_allocated_gb=8.2),
    build_memory_snapshot(step=10, allocated_gb=8.4, reserved_gb=9.7, max_allocated_gb=8.5),
    build_memory_snapshot(step=50, allocated_gb=8.3, reserved_gb=9.7, max_allocated_gb=8.6),
]

for row in snapshots:
    print(row)

print(summarize_snapshots(snapshots))

# Teaching note:
# Snapshot rows are most useful when recorded with matching workload context.
# A raw number without step and shape metadata is hard to interpret.
