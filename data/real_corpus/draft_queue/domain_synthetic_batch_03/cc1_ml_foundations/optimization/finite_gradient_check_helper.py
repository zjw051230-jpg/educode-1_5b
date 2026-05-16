# draft_status: candidate
# topic_id: MLF-014
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC-1
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only

"""Finite gradient check helper for tiny training experiments."""


def gradients_are_finite(named_grads):
    results = {}
    for name, grad_values in named_grads.items():
        results[name] = all(value == value and value not in (float("inf"), float("-inf")) for value in grad_values)
    return results


def demo_gradients():
    return {
        "embed.weight": [0.1, -0.2, 0.05],
        "lm_head.weight": [0.3, 0.0, -0.4],
    }


if __name__ == "__main__":
    print(gradients_are_finite(demo_gradients()))
