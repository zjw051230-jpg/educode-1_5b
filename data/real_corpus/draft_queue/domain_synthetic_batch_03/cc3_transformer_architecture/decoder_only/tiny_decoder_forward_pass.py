# draft_status: candidate
# topic_id: TRF-007
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC3
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only

"""Tiny decoder forward-pass shape sketch."""


def tiny_decoder_shapes(batch_size=2, seq_len=5, vocab_size=32, d_model=16, num_heads=4):
    if d_model % num_heads != 0:
        raise ValueError("d_model must be divisible by num_heads")

    head_dim = d_model // num_heads
    print(f"token ids: {(batch_size, seq_len)}")
    print(f"token embeddings: {(batch_size, seq_len, d_model)}")
    print(f"position embeddings: {(seq_len, d_model)}")
    print(f"embedded input: {(batch_size, seq_len, d_model)}")
    print(f"queries per head: {(batch_size, num_heads, seq_len, head_dim)}")
    print(f"attention scores: {(batch_size, num_heads, seq_len, seq_len)}")
    print(f"hidden after decoder stack: {(batch_size, seq_len, d_model)}")
    print(f"logits before loss: {(batch_size, seq_len, vocab_size)}")


if __name__ == "__main__":
    tiny_decoder_shapes()
