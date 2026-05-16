# draft_status: candidate
# topic_id: TRF-017
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC3
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only

"""Embedding table shape check for a toy configuration."""


def check_embedding_table(vocab_size, d_model, token_ids):
    table_shape = (vocab_size, d_model)
    print(f"embedding table shape: {table_shape}")

    bad_ids = [token_id for token_id in token_ids if token_id < 0 or token_id >= vocab_size]
    if bad_ids:
        print(f"out-of-range token ids: {bad_ids}")
    else:
        print("all token ids fit inside the embedding table")


if __name__ == "__main__":
    check_embedding_table(vocab_size=16, d_model=8, token_ids=[0, 3, 7, 15])
