from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from tokenizers import Tokenizer

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = PROJECT_ROOT / "src"
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "configs" / "a100" / "fineweb_edu_500mb_300m_1000step_public16k_execute.json"
TRAINING_SCRIPT_PATH = PROJECT_ROOT / "scripts" / "run_a100_300m_fineweb_edu_10step_training.py"
EXPECTED_PUBLIC16K_VOCAB_SIZE = 16384
EXPECTED_EVAL_INTERVAL_BY_MAX_STEPS = {
    1000: 100,
    3000: 300,
    5000: 500,
}
SUPPORTED_CORPUS_SIZE_LABELS_BY_PATH_MARKER = {
    "fineweb_edu_sample10bt_500mb": "500mb",
    "fineweb_edu_sample10bt_2gb": "2gb",
}
DISALLOWED_STALE_RUN_TOKENS = ["10step", "100step"]

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from educode.tiny_model import TinyModelConfig, model_config_from_dict


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def resolve_repo_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return PROJECT_ROOT / path


def repo_relative_path(path: Path) -> str:
    try:
        return path.relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def is_under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def count_parameters_exact_from_config(model_config: TinyModelConfig) -> int:
    d_model = model_config.d_model
    vocab_size = model_config.vocab_size
    context_length = model_config.context_length
    num_layers = model_config.num_layers
    d_ff = model_config.d_ff

    token_embedding_params = vocab_size * d_model
    position_embedding_params = context_length * d_model
    attention_params = (3 * d_model * d_model) + (d_model * d_model)
    feedforward_params = (d_model * d_ff) + (d_model * d_ff) + (d_ff * d_model)
    norm_params = 2 * d_model
    block_params = attention_params + feedforward_params + norm_params
    final_norm_params = d_model
    lm_head_params = d_model * vocab_size

    return token_embedding_params + position_embedding_params + (num_layers * block_params) + final_norm_params + lm_head_params


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check A100/A800 execution readiness for a bounded FineWeb-Edu public16k run.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH), help="Path to the A100/A800 execution config JSON.")
    return parser.parse_args()


def require(condition: bool, message: str, blockers: list[str]) -> None:
    if not condition:
        blockers.append(message)


def warn_unless(condition: bool, message: str, caveats: list[str]) -> None:
    if not condition:
        caveats.append(message)


def infer_corpus_size_label_from_path(path: Path) -> str | None:
    path_parts = {part.lower() for part in path.parts}
    for marker, label in SUPPORTED_CORPUS_SIZE_LABELS_BY_PATH_MARKER.items():
        if marker in path_parts:
            return label
    return None


def expected_run_name(corpus_size_label: str, max_steps: int) -> str:
    return f"fineweb_edu_{corpus_size_label}_300m_{max_steps}step_public16k_execute"


def has_stale_run_token(value: str) -> bool:
    lowered = value.lower()
    return any(token in lowered for token in DISALLOWED_STALE_RUN_TOKENS)


def main() -> int:
    args = parse_args()
    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = PROJECT_ROOT / config_path

    config = load_json(config_path)
    blockers: list[str] = []
    caveats: list[str] = []

    run_name = str(config["run"]["run_name"])
    output_dir = resolve_repo_path(str(config["run"]["output_dir"]))
    train_path = resolve_repo_path(str(config["data"]["train_path"]))
    val_path = resolve_repo_path(str(config["data"]["val_path"]))
    tokenizer_path = resolve_repo_path(str(config["tokenizer"]["path"]))
    checkpoint_save_dir = resolve_repo_path(str(config["checkpoint"]["save_dir"]))
    expected_checkpoint_save_dir = output_dir / "checkpoints"
    dry_run_summary_path = output_dir / "dry_run_summary.json"

    tokenizer_vocab_size = int(config["tokenizer"]["vocab_size"])
    model_vocab_size = int(config["model"]["vocab_size"])
    max_steps = int(config["training"]["max_steps"])
    eval_interval = int(config["training"]["eval_interval"])
    checkpoint_interval = int(config["training"]["checkpoint_interval"])
    training_no_training = config["training"].get("no_training")
    data_loading_mode = str(config.get("data", {}).get("data_loading_mode", config.get("data_loading_mode", ""))).strip().lower()
    no_commit_checkpoints = config.get("checkpoint", {}).get("no_commit_checkpoints")
    expected_eval_interval = EXPECTED_EVAL_INTERVAL_BY_MAX_STEPS.get(max_steps)
    supported_max_steps_text = ", ".join(str(step) for step in sorted(EXPECTED_EVAL_INTERVAL_BY_MAX_STEPS))
    output_dir_text = repo_relative_path(output_dir)
    train_corpus_size_label = infer_corpus_size_label_from_path(train_path)
    val_corpus_size_label = infer_corpus_size_label_from_path(val_path)
    corpus_size_label = train_corpus_size_label if train_corpus_size_label == val_corpus_size_label else None
    expected_run_name_text = expected_run_name(corpus_size_label, max_steps) if corpus_size_label else None

    require(TRAINING_SCRIPT_PATH.exists(), f"missing training script: {TRAINING_SCRIPT_PATH}", blockers)
    require(train_corpus_size_label is not None, "train_path must be from supported FineWeb-Edu 500MB or 2GB corpus", blockers)
    require(val_corpus_size_label is not None, "val_path must be from supported FineWeb-Edu 500MB or 2GB corpus", blockers)
    require(corpus_size_label is not None, "train_path and val_path must use the same supported corpus size", blockers)
    require(train_path.exists(), f"missing train_path: {train_path}", blockers)
    require(val_path.exists(), f"missing val_path: {val_path}", blockers)
    require(tokenizer_path.exists(), f"missing tokenizer_path: {tokenizer_path}", blockers)
    require(is_under(output_dir, PROJECT_ROOT / "experiments" / "a100"), "output_dir must stay under experiments/a100/", blockers)
    require(checkpoint_save_dir.resolve() == expected_checkpoint_save_dir.resolve(), "checkpoint.save_dir must equal output_dir/checkpoints", blockers)
    require(no_commit_checkpoints is True, "checkpoint.no_commit_checkpoints must be true", blockers)
    require(training_no_training is False, "training.no_training must be false for execution config", blockers)
    require(data_loading_mode == "streaming", "data_loading_mode must be streaming", blockers)
    require(tokenizer_vocab_size == EXPECTED_PUBLIC16K_VOCAB_SIZE, "public16k tokenizer vocab_size must be 16384", blockers)
    require(model_vocab_size == EXPECTED_PUBLIC16K_VOCAB_SIZE, "public16k model vocab_size must be 16384", blockers)
    require(tokenizer_vocab_size == model_vocab_size, "tokenizer.vocab_size must match model.vocab_size", blockers)
    require(max_steps in EXPECTED_EVAL_INTERVAL_BY_MAX_STEPS, f"max_steps must be one of: {supported_max_steps_text}", blockers)
    require(eval_interval == expected_eval_interval, f"eval_interval must be {expected_eval_interval} for {max_steps}-step public16k run", blockers)
    require(checkpoint_interval == max_steps, "checkpoint_interval must equal max_steps", blockers)
    require(str(config["training"].get("save_interval")) == str(max_steps), "training.save_interval must equal max_steps", blockers)
    require(expected_run_name_text is not None and run_name == expected_run_name_text, f"run_name must be {expected_run_name_text}", blockers)
    require(output_dir.name == run_name, "output_dir basename must match run_name", blockers)
    require(not has_stale_run_token(run_name), "run_name must not contain stale 10step/100step tokens", blockers)
    require(not has_stale_run_token(output_dir_text), "output_dir must not contain stale 10step/100step tokens", blockers)

    loaded_tokenizer_vocab_size: int | None = None
    if tokenizer_path.exists():
        loaded_tokenizer_vocab_size = Tokenizer.from_file(str(tokenizer_path)).get_vocab_size()
        require(
            loaded_tokenizer_vocab_size == tokenizer_vocab_size,
            f"loaded tokenizer vocab {loaded_tokenizer_vocab_size} != config tokenizer vocab {tokenizer_vocab_size}",
            blockers,
        )

    model_config = model_config_from_dict(config)
    expected_parameter_count = count_parameters_exact_from_config(model_config)

    dry_run_summary: dict[str, Any] | None = None
    if dry_run_summary_path.exists():
        dry_run_summary = load_json(dry_run_summary_path)
        require(dry_run_summary.get("output_dir") == output_dir_text, "dry-run output_dir mismatch", blockers)
        require(dry_run_summary.get("run_name") == run_name, "dry-run run_name mismatch", blockers)
        require(dry_run_summary.get("tokenizer_vocab_size") == tokenizer_vocab_size, "dry-run tokenizer_vocab_size mismatch", blockers)
        require(
            dry_run_summary.get("exact_parameter_count") == expected_parameter_count,
            "dry-run exact_parameter_count mismatch",
            blockers,
        )
        require(dry_run_summary.get("no_training") is True, "dry-run no_training must be true", blockers)
        if dry_run_summary.get("core_model_feature_parity") is False:
            caveats.append("core_model_feature_parity=false in dry-run summary; treat execution as systems validation only.")
    else:
        warn_unless(False, f"missing optional dry-run summary: {repo_relative_path(dry_run_summary_path)}", caveats)

    output_dir.mkdir(parents=True, exist_ok=True)
    summary_path = output_dir / "execution_readiness_summary.json"
    summary = {
        "status": "success" if not blockers else "failed",
        "config_path": repo_relative_path(config_path),
        "run_name": run_name,
        "output_dir": output_dir_text,
        "train_path": repo_relative_path(train_path),
        "val_path": repo_relative_path(val_path),
        "corpus_size_label": corpus_size_label,
        "expected_run_name": expected_run_name_text,
        "tokenizer_path": repo_relative_path(tokenizer_path),
        "tokenizer_vocab_size": tokenizer_vocab_size,
        "loaded_tokenizer_vocab_size": loaded_tokenizer_vocab_size,
        "data_loading_mode": data_loading_mode,
        "model_vocab_size": model_vocab_size,
        "exact_parameter_count": expected_parameter_count,
        "max_steps": max_steps,
        "eval_interval": eval_interval,
        "expected_eval_interval": expected_eval_interval,
        "checkpoint_interval": checkpoint_interval,
        "training_no_training": training_no_training,
        "checkpoint_save_dir": repo_relative_path(checkpoint_save_dir),
        "checkpoint_path_expectation": repo_relative_path(expected_checkpoint_save_dir),
        "checkpoint_path_uses_output_dir": checkpoint_save_dir.resolve() == expected_checkpoint_save_dir.resolve(),
        "no_commit_checkpoints": no_commit_checkpoints,
        "dry_run_summary_path": repo_relative_path(dry_run_summary_path),
        "dry_run_summary_present": dry_run_summary is not None,
        "dry_run_exact_parameter_count": dry_run_summary.get("exact_parameter_count") if dry_run_summary else None,
        "dry_run_output_dir": dry_run_summary.get("output_dir") if dry_run_summary else None,
        "dry_run_no_training": dry_run_summary.get("no_training") if dry_run_summary else None,
        "blockers": blockers,
        "blocker_count": len(blockers),
        "caveats": caveats,
        "caveat_count": len(caveats),
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "ready_for_a100_execution": not blockers,
        "ready_for_a800_execution": not blockers,
        "no_training_ran_in_this_step": True,
        "no_a100_or_a800_session_entered_in_this_step": True,
    }
    write_json(summary_path, summary)

    print(f"status={summary['status']}")
    print(f"config_path={summary['config_path']}")
    print(f"run_name={summary['run_name']}")
    print(f"output_dir={summary['output_dir']}")
    print(f"tokenizer_vocab_size={summary['tokenizer_vocab_size']}")
    print(f"data_loading_mode={summary['data_loading_mode']}")
    print(f"exact_parameter_count={summary['exact_parameter_count']}")
    print(f"max_steps={summary['max_steps']}")
    print(f"eval_interval={summary['eval_interval']}")
    print(f"checkpoint_interval={summary['checkpoint_interval']}")
    print(f"ready_for_a100_execution={summary['ready_for_a100_execution']}")
    print(f"ready_for_a800_execution={summary['ready_for_a800_execution']}")
    print(f"caveats={len(caveats)}")
    print(f"blockers={len(blockers)}")
    print(f"summary_path={repo_relative_path(summary_path)}")
    return 0 if not blockers else 1


if __name__ == "__main__":
    raise SystemExit(main())
