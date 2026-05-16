# draft_status: candidate
# topic_id: TRF-014
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC3
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only

"""Softmax-axis explanation for attention scores."""


def describe_attention_softmax(batch_size=2, num_heads=3, seq_len=4):
    score_shape = (batch_size, num_heads, seq_len, seq_len)
    print(f"score tensor shape: {score_shape}")
    print("last axis = candidate key positions for one query position")
    print("softmax should run across that last axis")

    for query_index in range(seq_len):
        print(f"query position {query_index} normalizes over keys 0..{seq_len - 1}")

    print("after causal masking, blocked future keys should receive near-zero probability")


if __name__ == "__main__":
    describe_attention_softmax()
