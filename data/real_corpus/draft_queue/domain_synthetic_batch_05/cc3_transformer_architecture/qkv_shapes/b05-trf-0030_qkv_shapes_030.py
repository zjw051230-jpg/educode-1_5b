# draft_status: candidate
# topic_id: B05-TRF-0030
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC-3
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only
# batch_id: domain_synthetic_batch_05

"""Reading a shape trace before the first matmul (QKV head split)."""

def demo_qkv_shapes_0030():
    batch_size = 2
    seq_len = 6
    d_model = 16
    num_heads = 4
    assert d_model % num_heads == 0
    head_dim = d_model // num_heads
    hidden_shape = (batch_size, seq_len, d_model)
    q_shape = (batch_size, seq_len, d_model)
    split_shape = (batch_size, num_heads, seq_len, head_dim)
    print("topic:", "qkv_shapes")
    print("anchor:", 'mini code trace')
    print("hidden_shape:", hidden_shape)
    print("q_projected_shape:", q_shape)
    print("head_dim:", head_dim)
    print("split_shape:", split_shape)
    print("check:", split_shape[1] * split_shape[3] == hidden_shape[2])
    review_points = [
        "state the core object: QKV head split",
        "name the chosen anchor: mini code trace",
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
    print("subtopic_guard:", "qkv_shapes example remains tied to QKV head split")
    print("summary_line:", "toy output is small enough to review by hand")

if __name__ == "__main__":
    demo_qkv_shapes_0030()
