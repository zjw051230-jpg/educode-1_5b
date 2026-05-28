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
BOUNDED_PROFILE_MODE = "bounded_sdpa_profile"
BOUNDED_PROFILE_MAX_STEPS = 50
BOUNDED_PROFILE_EVAL_INTERVAL = 50
EXPECTED_SDPA_PROFILE_RESULT_PACKAGE = "/vol/results/mvp28_a100_5gb_50step_sdpa_profile_results.tar.gz"
SUPPORTED_CORPUS_SIZE_LABELS_BY_PATH_MARKER = {
    "fineweb_edu_sample10bt_500mb": "500mb",
    "fineweb_edu_sample10bt_2gb": "2gb",
    "fineweb_edu_sample10bt_5gb": "5gb",
}
DISALLOWED_STALE_RUN_TOKENS = ["10step", "100step"]
SEQUENTIAL_PREFIX = "sequential_prefix"
SHUFFLE_BUFFER = "shuffle_buffer"
SUPPORTED_SAMPLING_POLICIES = {SEQUENTIAL_PREFIX, SHUFFLE_BUFFER}

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


def expected_profile_run_name(corpus_size_label: str) -> str:
    return f"fineweb_edu_{corpus_size_label}_300m_50step_public16k_sdpa_profile"


def has_stale_run_token(value: str) -> bool:
    lowered = value.lower()
    return any(token in lowered for token in DISALLOWED_STALE_RUN_TOKENS)


def is_bounded_sdpa_profile_config(config: dict[str, Any], run_name: str) -> bool:
    profiling_config = config.get("profiling")
    if not isinstance(profiling_config, dict):
        return False

    profile_mode = str(profiling_config.get("profile_mode", "")).strip().lower()
    attention_backend = str(profiling_config.get("attention_backend", "")).strip().lower()
    status = str(config.get("status", "")).strip().lower()
    return (
        profile_mode == BOUNDED_PROFILE_MODE
        and profiling_config.get("enabled") is True
        and attention_backend == "sdpa"
        and run_name.endswith("_sdpa_profile")
        and "profiling" in status
    )


def get_scheduler_policy(config: dict[str, Any]) -> str:
    scheduler_config = config.get("scheduler")
    if not isinstance(scheduler_config, dict):
        return "constant"

    policy_value = scheduler_config.get("policy")
    if policy_value is None:
        return "constant"

    policy = str(policy_value).strip().lower()
    if policy in {"constant", "not_applied"}:
        return policy
    raise NotImplementedError(f"unsupported scheduler policy: {policy}")


def build_scheduler_metadata(config: dict[str, Any]) -> dict[str, Any]:
    optimizer_config = config.get("optimizer", {}) if isinstance(config.get("optimizer"), dict) else {}
    learning_rate = float(optimizer_config.get("learning_rate", 3e-4))
    scheduler_config = config.get("scheduler")
    scheduler_config_present = isinstance(scheduler_config, dict)
    scheduler_enabled = bool(scheduler_config.get("enabled", False)) if scheduler_config_present else False
    scheduler_policy = get_scheduler_policy(config)
    scheduler_applied = False
    learning_rate_mode = "constant" if scheduler_policy == "constant" else "not_applied"

    return {
        "scheduler_config_present": scheduler_config_present,
        "scheduler_enabled": scheduler_enabled,
        "scheduler_policy": scheduler_policy,
        "scheduler_applied": scheduler_applied,
        "scheduler_config_present_but_not_applied": scheduler_policy != "constant" and not scheduler_applied,
        "learning_rate_mode": learning_rate_mode,
        "base_learning_rate": learning_rate,
        "final_learning_rate": learning_rate,
    }


def build_sampling_metadata(config: dict[str, Any]) -> dict[str, Any]:
    sampling_config = config.get("sampling")
    sampling_config_present = isinstance(sampling_config, dict)
    if not sampling_config_present:
        return {
            "sampling_config_present": False,
            "sampling_policy": SEQUENTIAL_PREFIX,
            "shuffle_seed": None,
            "shuffle_buffer_size": 1,
            "bounded_prefix_batches_only": True,
        }

    policy = str(sampling_config.get("policy", SEQUENTIAL_PREFIX)).strip().lower()
    if policy not in SUPPORTED_SAMPLING_POLICIES:
        raise ValueError(f"unsupported sampling policy: {policy}")

    shuffle_buffer_size = int(sampling_config.get("shuffle_buffer_size", 1))
    if policy == SEQUENTIAL_PREFIX:
        shuffle_seed = sampling_config.get("shuffle_seed")
        return {
            "sampling_config_present": True,
            "sampling_policy": SEQUENTIAL_PREFIX,
            "shuffle_seed": int(shuffle_seed) if shuffle_seed is not None else None,
            "shuffle_buffer_size": shuffle_buffer_size,
            "bounded_prefix_batches_only": True,
        }

    if shuffle_buffer_size <= 1:
        raise ValueError("shuffle_buffer_size must be greater than 1 for shuffle_buffer sampling")

    seed_value = sampling_config.get("shuffle_seed", config.get("run", {}).get("seed"))
    if seed_value is None:
        raise ValueError("shuffle_buffer sampling requires shuffle_seed or run.seed")

    return {
        "sampling_config_present": True,
        "sampling_policy": SHUFFLE_BUFFER,
        "shuffle_seed": int(seed_value),
        "shuffle_buffer_size": shuffle_buffer_size,
        "bounded_prefix_batches_only": False,
    }


def build_validation_sampling_metadata(config: dict[str, Any]) -> dict[str, Any]:
    validation_sampling_config = config.get("validation_sampling")
    validation_sampling_config_present = isinstance(validation_sampling_config, dict)
    if not validation_sampling_config_present:
        return {
            "validation_sampling_config_present": False,
            "validation_sampling_policy": None,
            "validation_shuffle_seed": None,
            "validation_shuffle_buffer_size": None,
            "validation_max_blocks_per_document": None,
        }

    return {
        "validation_sampling_config_present": True,
        "validation_sampling_policy": str(validation_sampling_config.get("policy", "")).strip().lower(),
        "validation_shuffle_seed": validation_sampling_config.get("shuffle_seed"),
        "validation_shuffle_buffer_size": validation_sampling_config.get("shuffle_buffer_size"),
        "validation_max_blocks_per_document": validation_sampling_config.get("max_blocks_per_document"),
    }


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
    try:
        scheduler_metadata = build_scheduler_metadata(config)
    except NotImplementedError as exc:
        scheduler_config = config.get("scheduler", {}) if isinstance(config.get("scheduler"), dict) else {}
        scheduler_policy = str(scheduler_config.get("policy", "unsupported")).strip().lower()
        blockers.append(f"unsupported scheduler policy: {scheduler_policy}")
        scheduler_metadata = {
            "scheduler_config_present": isinstance(config.get("scheduler"), dict),
            "scheduler_enabled": bool(scheduler_config.get("enabled", False)),
            "scheduler_policy": scheduler_policy,
            "scheduler_applied": False,
            "scheduler_config_present_but_not_applied": True,
            "learning_rate_mode": "unsupported",
            "base_learning_rate": float(config.get("optimizer", {}).get("learning_rate", 3e-4))
            if isinstance(config.get("optimizer"), dict)
            else 3e-4,
            "final_learning_rate": None,
            "scheduler_error": str(exc),
        }
    try:
        sampling_metadata = build_sampling_metadata(config)
    except (TypeError, ValueError) as exc:
        sampling_config = config.get("sampling", {}) if isinstance(config.get("sampling"), dict) else {}
        blockers.append(str(exc))
        sampling_metadata = {
            "sampling_config_present": isinstance(config.get("sampling"), dict),
            "sampling_policy": str(sampling_config.get("policy", "unsupported")).strip().lower(),
            "shuffle_seed": sampling_config.get("shuffle_seed"),
            "shuffle_buffer_size": sampling_config.get("shuffle_buffer_size"),
            "bounded_prefix_batches_only": True,
            "sampling_error": str(exc),
        }
    validation_sampling_metadata = build_validation_sampling_metadata(config)
    profiling_config = config.get("profiling", {}) if isinstance(config.get("profiling"), dict) else {}
    is_bounded_profile = is_bounded_sdpa_profile_config(config, run_name)
    expected_eval_interval = (
        BOUNDED_PROFILE_EVAL_INTERVAL
        if is_bounded_profile
        else EXPECTED_EVAL_INTERVAL_BY_MAX_STEPS.get(max_steps)
    )
    supported_max_steps_text = ", ".join(str(step) for step in sorted(EXPECTED_EVAL_INTERVAL_BY_MAX_STEPS))
    output_dir_text = repo_relative_path(output_dir)
    train_corpus_size_label = infer_corpus_size_label_from_path(train_path)
    val_corpus_size_label = infer_corpus_size_label_from_path(val_path)
    corpus_size_label = train_corpus_size_label if train_corpus_size_label == val_corpus_size_label else None
    expected_run_name_text = (
        expected_profile_run_name(corpus_size_label)
        if is_bounded_profile and corpus_size_label
        else expected_run_name(corpus_size_label, max_steps)
        if corpus_size_label
        else None
    )

    require(TRAINING_SCRIPT_PATH.exists(), f"missing training script: {TRAINING_SCRIPT_PATH}", blockers)
    require(train_corpus_size_label is not None, "train_path must be from supported FineWeb-Edu 500MB, 2GB, or 5GB corpus", blockers)
    require(val_corpus_size_label is not None, "val_path must be from supported FineWeb-Edu 500MB, 2GB, or 5GB corpus", blockers)
    require(corpus_size_label is not None, "train_path and val_path must use the same supported corpus size", blockers)
    require(train_path.exists(), f"missing train_path: {train_path}", blockers)
    require(val_path.exists(), f"missing val_path: {val_path}", blockers)
    require(tokenizer_path.exists(), f"missing tokenizer_path: {tokenizer_path}", blockers)
    require(is_under(output_dir, PROJECT_ROOT / "experiments" / "a100"), "output_dir must stay under experiments/a100/", blockers)
    require(checkpoint_save_dir.resolve() == expected_checkpoint_save_dir.resolve(), "checkpoint.save_dir must equal output_dir/checkpoints", blockers)
    require(no_commit_checkpoints is True, "checkpoint.no_commit_checkpoints must be true", blockers)
    require(training_no_training is False, "training.no_training must be false for execution config", blockers)
    require(data_loading_mode == "streaming", "data_loading_mode must be streaming", blockers)
    if corpus_size_label in {"2gb", "5gb"}:
        require(sampling_metadata["sampling_config_present"] is True, "2GB/5GB execution config must declare sampling", blockers)
        require(
            sampling_metadata["sampling_policy"] == SHUFFLE_BUFFER,
            "2GB/5GB execution config must use shuffle_buffer sampling",
            blockers,
        )
        require(isinstance(sampling_metadata["shuffle_seed"], int), "shuffle_buffer sampling must declare shuffle_seed", blockers)
        require(
            isinstance(sampling_metadata["shuffle_buffer_size"], int) and sampling_metadata["shuffle_buffer_size"] > 1,
            "shuffle_buffer_size must be greater than 1",
            blockers,
        )
        require(
            sampling_metadata["bounded_prefix_batches_only"] is False,
            "shuffle_buffer config must not be marked as bounded prefix only",
            blockers,
        )
    require(tokenizer_vocab_size == EXPECTED_PUBLIC16K_VOCAB_SIZE, "public16k tokenizer vocab_size must be 16384", blockers)
    require(model_vocab_size == EXPECTED_PUBLIC16K_VOCAB_SIZE, "public16k model vocab_size must be 16384", blockers)
    require(tokenizer_vocab_size == model_vocab_size, "tokenizer.vocab_size must match model.vocab_size", blockers)
    if is_bounded_profile:
        require(max_steps == BOUNDED_PROFILE_MAX_STEPS, "bounded SDPA profile max_steps must be 50", blockers)
        require(eval_interval == BOUNDED_PROFILE_EVAL_INTERVAL, "bounded SDPA profile eval_interval must be 50", blockers)
        require(max_steps < 1000, "bounded SDPA profile must stay below long-run training step counts", blockers)
        require(profiling_config.get("attention_backend") == "sdpa", "bounded profile attention_backend must be sdpa", blockers)
        require(profiling_config.get("record_tokens_per_sec") is True, "bounded profile must record tokens/sec", blockers)
        require(profiling_config.get("record_memory") is True, "bounded profile must record memory", blockers)
        require(profiling_config.get("record_mfu") is True, "bounded profile must record MFU", blockers)
        require(
            profiling_config.get("expected_result_package") == EXPECTED_SDPA_PROFILE_RESULT_PACKAGE,
            f"bounded profile expected_result_package must be {EXPECTED_SDPA_PROFILE_RESULT_PACKAGE}",
            blockers,
        )
        require(
            validation_sampling_metadata["validation_sampling_config_present"] is True,
            "bounded profile must declare validation_sampling",
            blockers,
        )
        require(
            validation_sampling_metadata["validation_sampling_policy"] == SHUFFLE_BUFFER,
            "bounded profile validation_sampling must use shuffle_buffer",
            blockers,
        )
        require(
            isinstance(validation_sampling_metadata["validation_shuffle_seed"], int),
            "bounded profile validation_sampling must declare integer shuffle_seed",
            blockers,
        )
        require(
            isinstance(validation_sampling_metadata["validation_shuffle_buffer_size"], int)
            and validation_sampling_metadata["validation_shuffle_buffer_size"] > 1,
            "bounded profile validation shuffle_buffer_size must be greater than 1",
            blockers,
        )
    else:
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
        if "scheduler_policy" in dry_run_summary:
            require(
                dry_run_summary.get("scheduler_policy") == scheduler_metadata["scheduler_policy"],
                "dry-run scheduler_policy mismatch",
                blockers,
            )
        if "learning_rate_mode" in dry_run_summary:
            require(
                dry_run_summary.get("learning_rate_mode") == scheduler_metadata["learning_rate_mode"],
                "dry-run learning_rate_mode mismatch",
                blockers,
            )
        if "sampling_policy" in dry_run_summary:
            require(
                dry_run_summary.get("sampling_policy") == sampling_metadata["sampling_policy"],
                "dry-run sampling_policy mismatch",
                blockers,
            )
        if "shuffle_seed" in dry_run_summary:
            require(
                dry_run_summary.get("shuffle_seed") == sampling_metadata["shuffle_seed"],
                "dry-run shuffle_seed mismatch",
                blockers,
            )
        if "shuffle_buffer_size" in dry_run_summary:
            require(
                dry_run_summary.get("shuffle_buffer_size") == sampling_metadata["shuffle_buffer_size"],
                "dry-run shuffle_buffer_size mismatch",
                blockers,
            )
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
        "readiness_gate_type": "bounded_sdpa_profile" if is_bounded_profile else "training_execution",
        "is_bounded_profile": is_bounded_profile,
        "profiling_enabled": profiling_config.get("enabled"),
        "profiling_profile_mode": profiling_config.get("profile_mode"),
        "profiling_attention_backend": profiling_config.get("attention_backend"),
        "profiling_record_tokens_per_sec": profiling_config.get("record_tokens_per_sec"),
        "profiling_record_memory": profiling_config.get("record_memory"),
        "profiling_record_mfu": profiling_config.get("record_mfu"),
        "profiling_expected_result_package": profiling_config.get("expected_result_package"),
        "dry_run_summary_path": repo_relative_path(dry_run_summary_path),
        "dry_run_summary_present": dry_run_summary is not None,
        "dry_run_exact_parameter_count": dry_run_summary.get("exact_parameter_count") if dry_run_summary else None,
        "dry_run_output_dir": dry_run_summary.get("output_dir") if dry_run_summary else None,
        "dry_run_no_training": dry_run_summary.get("no_training") if dry_run_summary else None,
        **scheduler_metadata,
        **sampling_metadata,
        **validation_sampling_metadata,
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
    print(f"readiness_gate_type={summary['readiness_gate_type']}")
    print(f"eval_interval={summary['eval_interval']}")
    print(f"checkpoint_interval={summary['checkpoint_interval']}")
    print(f"attention_backend={summary['profiling_attention_backend']}")
    print(f"scheduler_policy={summary['scheduler_policy']}")
    print(f"learning_rate_mode={summary['learning_rate_mode']}")
    print(f"sampling_policy={summary['sampling_policy']}")
    print(f"shuffle_seed={summary['shuffle_seed']}")
    print(f"shuffle_buffer_size={summary['shuffle_buffer_size']}")
    print(f"bounded_prefix_batches_only={summary['bounded_prefix_batches_only']}")
    print(f"ready_for_a100_execution={summary['ready_for_a100_execution']}")
    print(f"ready_for_a800_execution={summary['ready_for_a800_execution']}")
    print(f"caveats={len(caveats)}")
    print(f"blockers={len(blockers)}")
    print(f"summary_path={repo_relative_path(summary_path)}")
    return 0 if not blockers else 1


if __name__ == "__main__":
    raise SystemExit(main())
