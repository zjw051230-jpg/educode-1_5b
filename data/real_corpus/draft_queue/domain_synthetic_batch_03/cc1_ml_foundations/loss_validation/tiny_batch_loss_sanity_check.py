# draft_status: candidate
# topic_id: MLF-007
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC-1
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only

"""Tiny batch shape and target-alignment sanity check example."""


def build_tiny_batch():
    inputs = [[1, 4, 7], [1, 3, 3]]
    targets = [[4, 7, 9], [3, 3, 2]]
    return inputs, targets


def describe_batch(inputs, targets, vocab_size=10):
    batch_size = len(inputs)
    time_steps = len(inputs[0])
    logits_shape = (batch_size, time_steps, vocab_size)
    return {
        "inputs": inputs,
        "targets": targets,
        "logits_shape": logits_shape,
        "checks": [
            "targets are shifted by one position",
            "batch and time dimensions match",
            "target ids stay inside the vocab range",
        ],
    }


if __name__ == "__main__":
    inputs, targets = build_tiny_batch()
    print(describe_batch(inputs, targets))
