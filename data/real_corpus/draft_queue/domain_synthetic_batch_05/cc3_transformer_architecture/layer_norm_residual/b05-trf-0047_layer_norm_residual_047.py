# draft_status: candidate
# topic_id: B05-TRF-0047
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC-3
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only
# batch_id: domain_synthetic_batch_05

"""Why the add path can be right while the stats are wrong (layer norm path)."""

def demo_layer_norm_residual_0047():
    residual = [1.0, -1.0, 0.5, 2.0]
    branch = [0.2, 0.1, -0.3, 0.4]
    added = [a + b for a, b in zip(residual, branch)]
    mean = sum(added) / len(added)
    centered = [x - mean for x in added]
    variance = sum(x * x for x in centered) / len(centered)
    print("topic:", "layer_norm_residual")
    print("anchor:", 'before/after comparison')
    print("residual:", residual)
    print("branch:", branch)
    print("added:", added)
    print("mean:", round(mean, 4))
    print("variance:", round(variance, 4))
    print("shape_preserved:", len(residual) == len(added))
    review_points = [
        "state the core object: layer norm path",
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
    print("subtopic_guard:", "layer_norm_residual example remains tied to layer norm path")
    print("summary_line:", "toy output is small enough to review by hand")

if __name__ == "__main__":
    demo_layer_norm_residual_0047()
