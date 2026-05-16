# draft_status: candidate
# topic_id: RTS-017
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC4
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only


def build_run_summary(run_id, final_step, train_loss, val_loss, checkpoint_ok):
    return {
        "run_id": run_id,
        "final_step": int(final_step),
        "final_train_loss": float(train_loss),
        "final_val_loss": None if val_loss is None else float(val_loss),
        "checkpoint_roundtrip_ok": bool(checkpoint_ok),
    }


def build_status_flags(summary):
    return {
        "has_validation": summary["final_val_loss"] is not None,
        "is_bounded_run": summary["final_step"] > 0,
        "resume_review_ready": summary["checkpoint_roundtrip_ok"],
    }


summary = build_run_summary(
    run_id="tiny-a100-smoke-07",
    final_step=100,
    train_loss=2.31,
    val_loss=2.48,
    checkpoint_ok=True,
)

print(summary)
print(build_status_flags(summary))

# Teaching note:
# A summary dict should favor simple, explicit fields.
# It is easier to audit than a large nested object for small educational runs.
