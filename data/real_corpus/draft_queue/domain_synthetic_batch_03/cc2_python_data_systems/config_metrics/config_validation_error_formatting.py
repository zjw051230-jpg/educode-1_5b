# draft_status: candidate
# topic_id: PDS-020
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC2
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only

from typing import Iterable


def format_config_errors(errors: Iterable[str], config_name: str) -> str:
    problems = [error.strip() for error in errors if error.strip()]
    if not problems:
        return f"{config_name}: no validation errors"
    lines = [f"{config_name}: validation failed"]
    for index, problem in enumerate(problems, start=1):
        lines.append(f"  {index}. {problem}")
    return "\n".join(lines)


def main() -> None:
    issues = [
        "missing field: seq_len",
        "batch_size must be a positive integer",
    ]
    print(format_config_errors(issues, config_name="tiny_run.yaml"))


if __name__ == "__main__":
    main()
