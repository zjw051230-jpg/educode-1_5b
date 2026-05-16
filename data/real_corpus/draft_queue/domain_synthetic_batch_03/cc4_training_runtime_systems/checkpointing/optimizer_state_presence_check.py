# draft_status: candidate
# topic_id: RTS-006
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC4
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only


def check_optimizer_state(checkpoint):
    if "optimizer_state" not in checkpoint:
        return {"ok": False, "reason": "missing optimizer_state"}

    optimizer_state = checkpoint["optimizer_state"]
    state = optimizer_state.get("state", {})
    param_groups = optimizer_state.get("param_groups", [])

    return {
        "ok": True,
        "state_entry_count": len(state),
        "param_group_count": len(param_groups),
        "has_state_entries": bool(state),
    }


checkpoint_with_optimizer = {
    "model_state": {"layer.weight": [0.1, 0.2]},
    "optimizer_state": {
        "state": {0: {"exp_avg": [0.01, 0.02]}},
        "param_groups": [{"lr": 3e-4, "weight_decay": 0.1}],
    },
}

checkpoint_without_optimizer = {
    "model_state": {"layer.weight": [0.1, 0.2]},
}

print(check_optimizer_state(checkpoint_with_optimizer))
print(check_optimizer_state(checkpoint_without_optimizer))

# Teaching note:
# A checkpoint can still be useful for inference without optimizer state.
# It is less useful for faithful training resume.
# The review question should match the intended use.
