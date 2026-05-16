# draft_status: candidate
# topic_id: TRF-010
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC3
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only

"""Masked attention logits example using plain Python lists."""


def apply_causal_mask(scores):
    masked = []
    for i, row in enumerate(scores):
        masked_row = []
        for j, value in enumerate(row):
            masked_row.append(value if j <= i else float("-inf"))
        masked.append(masked_row)
    return masked


def print_matrix(name, matrix):
    print(name)
    for row in matrix:
        print("  ", row)


if __name__ == "__main__":
    raw_scores = [
        [1.2, 0.3, -0.4, 0.8],
        [0.5, 1.1, 0.7, -0.2],
        [0.9, 0.2, 1.4, 0.6],
        [0.1, 0.0, 0.3, 1.7],
    ]
    masked_scores = apply_causal_mask(raw_scores)
    print_matrix("raw scores", raw_scores)
    print_matrix("masked scores", masked_scores)
