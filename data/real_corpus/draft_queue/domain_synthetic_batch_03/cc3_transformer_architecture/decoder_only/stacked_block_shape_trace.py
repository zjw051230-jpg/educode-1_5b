# draft_status: candidate
# topic_id: TRF-005
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC3
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only

"""Shape trace through stacked decoder blocks."""


def trace_decoder_stack(batch_size=2, seq_len=4, d_model=8, num_heads=2, ff_mult=4, num_layers=3):
    if d_model % num_heads != 0:
        raise ValueError("d_model must be divisible by num_heads")

    head_dim = d_model // num_heads
    residual_shape = (batch_size, seq_len, d_model)
    print(f"input residual: {residual_shape}")

    for layer in range(num_layers):
        print(f"\nlayer {layer}")
        print(f"  ln1 output: {residual_shape}")
        print(f"  qkv projection: {(batch_size, seq_len, 3 * d_model)}")
        print(f"  q per head: {(batch_size, num_heads, seq_len, head_dim)}")
        print(f"  k per head: {(batch_size, num_heads, seq_len, head_dim)}")
        print(f"  v per head: {(batch_size, num_heads, seq_len, head_dim)}")
        print(f"  attention scores: {(batch_size, num_heads, seq_len, seq_len)}")
        print(f"  merged heads: {residual_shape}")
        print(f"  residual after attention: {residual_shape}")
        print(f"  ln2 output: {residual_shape}")
        print(f"  feedforward expand: {(batch_size, seq_len, ff_mult * d_model)}")
        print(f"  feedforward project: {residual_shape}")
        print(f"  residual after feedforward: {residual_shape}")

    print(f"\nfinal hidden: {residual_shape}")


if __name__ == "__main__":
    trace_decoder_stack()
