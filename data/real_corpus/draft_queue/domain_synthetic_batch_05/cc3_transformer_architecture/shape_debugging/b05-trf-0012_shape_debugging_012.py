# draft_status: candidate
# topic_id: B05-TRF-0012
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC-3
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only
# batch_id: domain_synthetic_batch_05

"""Turning a stack trace into a tensor checklist (shape mismatch)."""

def demo_shape_debugging_0012():
    expected = (2, 4, 12)
    observed = (2, 4, 11)
    same_rank = len(expected) == len(observed)
    mismatch_axes = [i for i, (a, b) in enumerate(zip(expected, observed)) if a != b]
    print("topic:", "shape_debugging")
    print("anchor:", 'before/after comparison')
    print("expected:", expected)
    print("observed:", observed)
    print("same_rank:", same_rank)
    print("mismatch_axes:", mismatch_axes)
    print("next_check:", "trace the first reshape or projection touching axis 2")
    review_points = [
        "state the core object: shape mismatch",
        "name the chosen anchor: before/after comparison",
        "compare the observed artifact against the intended invariant",
        "write the next debug print before touching larger model code",
    ]
    print("review_points:")
    for item in review_points:
        print("  -", item)
    next_checks = {
        "shape": "verify inner dimensions before the next reshape",
        "mask": "inspect one row and one column explicitly",
        "logits": "check whether the last axis equals vocab size",
        "stability": "compare a before/after statistic instead of guessing",
    }
    print("next_checks:", next_checks)
    print("subtopic_guard:", "shape_debugging example remains tied to shape mismatch")
    print("summary_line:", "toy output is small enough to review by hand")

if __name__ == "__main__":
    demo_shape_debugging_0012()
