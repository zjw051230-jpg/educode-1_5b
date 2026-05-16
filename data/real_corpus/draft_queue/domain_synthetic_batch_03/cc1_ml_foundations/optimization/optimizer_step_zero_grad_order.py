# draft_status: candidate
# topic_id: MLF-012
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC-1
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only

"""Educational example for optimizer step and zero-grad ordering."""


def training_step_order():
    return [
        "forward pass",
        "compute next-token loss",
        "backward pass",
        "optimizer.step()",
        "optimizer.zero_grad()",
    ]


def why_order_matters():
    return {
        "goal": "use each batch gradient once",
        "risk_if_skipped": "gradients accumulate across batches by accident",
        "effect": "apparent optimizer behavior becomes harder to interpret",
    }


if __name__ == "__main__":
    print(training_step_order())
    print(why_order_matters())
