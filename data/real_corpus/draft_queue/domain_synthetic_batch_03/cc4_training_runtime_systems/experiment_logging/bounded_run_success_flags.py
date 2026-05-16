# draft_status: candidate
# topic_id: RTS-020
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC4
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only


def evaluate_bounded_run(report):
    checks = {
        "has_steps": report.get("final_step", 0) > 0,
        "finite_train_loss": report.get("train_loss_finite", False),
        "checkpoint_roundtrip_ok": report.get("checkpoint_roundtrip_ok", False),
        "validation_completed": report.get("validation_completed", False),
    }
    checks["overall_success"] = all(checks.values())
    return checks


bounded_report = {
    "final_step": 100,
    "train_loss_finite": True,
    "checkpoint_roundtrip_ok": True,
    "validation_completed": True,
}

failed_report = {
    "final_step": 100,
    "train_loss_finite": True,
    "checkpoint_roundtrip_ok": False,
    "validation_completed": True,
}

print(evaluate_bounded_run(bounded_report))
print(evaluate_bounded_run(failed_report))

# Teaching note:
# Success flags help reviewers separate "run completed" from
# "run completed with the required runtime guarantees."
