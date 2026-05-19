# draft_status: candidate
# topic_id: B05-MLF-0098
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC-1
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only
# batch_id: domain_synthetic_batch_05


"""Tokenizer Boundary Change Not Reflected.
Synthetic teaching script for CC-1 batch_05.
Learning objective: Show how a boundary change upstream can invalidate downstream metric comparisons.
Writing form: bug-reproduction snippet. Concrete anchor: failure scenario.
"""

from __future__ import annotations

from statistics import mean

DEFINITION = "Tokenizer Boundary Change Not Reflected"
LEARNING_OBJECTIVE = "Show how a boundary change upstream can invalidate downstream metric comparisons."
ANCHOR = "failure scenario"

def load_trace_0098():
    return [
        {"step": 1, "train_loss": 2.190, "val_loss": 2.350, "grad_norm": 2.510},
        {"step": 2, "train_loss": 2.220, "val_loss": 2.380, "grad_norm": 2.540},
        {"step": 3, "train_loss": 2.340, "val_loss": 2.500, "grad_norm": 2.660},
        {"step": 4, "train_loss": 2.460, "val_loss": 2.620, "grad_norm": 2.780},
    ]

def averaged_gap(trace):
    return round(mean(row["val_loss"] - row["train_loss"] for row in trace), 4)

def largest_val_jump(trace):
    jumps = []
    for left, right in zip(trace, trace[1:]):
        jumps.append(round(right["val_loss"] - left["val_loss"], 4))
    return max(jumps, key=abs)

def classify_behavior(trace):
    gap = averaged_gap(trace)
    jump = largest_val_jump(trace)
    final_train = trace[-1]["train_loss"]
    final_val = trace[-1]["val_loss"]
    labels = []
    if gap > 0.22:
        labels.append("generalization_pressure")
    if jump > 0.12:
        labels.append("validation_instability")
    if final_val < final_train:
        labels.append("suspect_metric_definition")
    if not labels:
        labels.append("controlled_behavior")
    return labels

def compare_fix(before, after):
    return {
        "gap_before": averaged_gap(before),
        "gap_after": averaged_gap(after),
        "jump_before": largest_val_jump(before),
        "jump_after": largest_val_jump(after),
    }

def print_report(trace, repaired_trace):
    print(f"topic={DEFINITION}")
    print(f"objective={LEARNING_OBJECTIVE}")
    print(f"anchor={ANCHOR}")
    print(f"labels={classify_behavior(trace)}")
    print(compare_fix(trace, repaired_trace))
    print("step train val grad")
    for row in trace:
        print(row["step"], row["train_loss"], row["val_loss"], row["grad_norm"])

def repaired_trace(trace):
    repaired = []
    for row in trace:
        repaired.append({
            "step": row["step"],
            "train_loss": round(row["train_loss"] - 0.03, 3),
            "val_loss": round(row["val_loss"] - 0.06, 3),
            "grad_norm": round(max(row["grad_norm"] - 0.04, 0.01), 3),
        })
    return repaired

def anchor_commentary(trace):
    commentary = []
    for row in trace:
        commentary.append(
            f"step {row['step']}: train={row['train_loss']:.3f}, val={row['val_loss']:.3f}, grad={row['grad_norm']:.3f}"
        )
    return commentary

if __name__ == "__main__":
    trace = load_trace_0098()
    fixed = repaired_trace(trace)
    print_report(trace, fixed)
    for line in anchor_commentary(trace):
        print(line)
