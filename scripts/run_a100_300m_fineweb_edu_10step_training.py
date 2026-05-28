from __future__ import annotations

import argparse
import json
import math
import sys
import time
from contextlib import nullcontext
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import torch
from tokenizers import Tokenizer

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = PROJECT_ROOT / "src"
SCRIPTS_PATH = PROJECT_ROOT / "scripts"
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "configs" / "a100" / "fineweb_edu_50mb_300m_10step_smoke.json"
EXPECTED_SOURCE_CATEGORY = "public_pretraining_corpus"
EXPECTED_LICENSE = "odc-by"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

for path in (SRC_PATH, SCRIPTS_PATH):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from educode.checkpoint import compare_model_parameters, load_checkpoint, save_checkpoint
from educode.config_loader import load_json_config
from educode.config_validator import validate_config
from educode.losses import next_token_cross_entropy
from educode.run_logging import append_jsonl, build_summary_markdown, write_json, write_metrics_record, write_text
from educode.run_setup import collect_basic_environment, get_git_branch, get_git_commit, make_run_id, snapshot_config, write_run_metadata
from educode.sequence_dataset import batch_samples, make_next_token_samples
from educode.tiny_model import TinyDecoderOnlyTransformer, TinyModelConfig, model_config_from_dict
from streaming_lm_batch_iterator import SEQUENTIAL_PREFIX, SHUFFLE_BUFFER, create_streaming_batch_iterator


def resolve_repo_path(path_text: str | Path) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return PROJECT_ROOT / path


def get_data_loading_mode(config: dict[str, Any]) -> str:
    data_config = config.get("data", {}) if isinstance(config.get("data"), dict) else {}
    mode = str(data_config.get("data_loading_mode", config.get("data_loading_mode", "precomputed"))).strip().lower()
    if mode not in {"precomputed", "streaming"}:
        raise ValueError("data_loading_mode must be either 'precomputed' or 'streaming'")
    return mode


def get_eos_token_id(config: dict[str, Any]) -> int | None:
    tokenizer_config = config.get("tokenizer", {}) if isinstance(config.get("tokenizer"), dict) else {}
    eos_token_id = tokenizer_config.get("eos_token_id", tokenizer_config.get("endoftext_token_id"))
    return eos_token_id if isinstance(eos_token_id, int) else None


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


def build_scheduler_metadata(
    config: dict[str, Any],
    base_learning_rate: float | None = None,
    final_learning_rate: float | None = None,
) -> dict[str, Any]:
    optimizer_config = config.get("optimizer", {}) if isinstance(config.get("optimizer"), dict) else {}
    base_lr = float(optimizer_config.get("learning_rate", 3e-4)) if base_learning_rate is None else base_learning_rate
    final_lr = base_lr if final_learning_rate is None else final_learning_rate
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
        "base_learning_rate": base_lr,
        "final_learning_rate": final_lr,
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
    if policy not in {SEQUENTIAL_PREFIX, SHUFFLE_BUFFER}:
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


def build_validation_sampling_settings(config: dict[str, Any]) -> dict[str, Any]:
    validation_sampling_config = config.get("validation_sampling")
    if not isinstance(validation_sampling_config, dict):
        return {
            "sampling_policy": SEQUENTIAL_PREFIX,
            "shuffle_seed": None,
            "shuffle_buffer_size": 1,
            "max_blocks_per_document": None,
        }

    policy = str(validation_sampling_config.get("policy", SEQUENTIAL_PREFIX)).strip().lower()
    if policy not in {SEQUENTIAL_PREFIX, SHUFFLE_BUFFER}:
        raise ValueError(f"unsupported validation sampling policy: {policy}")

    shuffle_buffer_size = int(validation_sampling_config.get("shuffle_buffer_size", 1))
    max_blocks_value = validation_sampling_config.get("max_blocks_per_document")
    max_blocks_per_document = int(max_blocks_value) if max_blocks_value is not None else None
    if max_blocks_per_document is not None and max_blocks_per_document <= 0:
        raise ValueError("validation max_blocks_per_document must be positive")

    if policy == SEQUENTIAL_PREFIX:
        shuffle_seed = validation_sampling_config.get("shuffle_seed")
        return {
            "sampling_policy": SEQUENTIAL_PREFIX,
            "shuffle_seed": int(shuffle_seed) if shuffle_seed is not None else None,
            "shuffle_buffer_size": shuffle_buffer_size,
            "max_blocks_per_document": max_blocks_per_document,
        }

    if shuffle_buffer_size <= 1:
        raise ValueError("validation shuffle_buffer_size must be greater than 1 for shuffle_buffer sampling")

    seed_value = validation_sampling_config.get("shuffle_seed", validation_sampling_config.get("sampling_seed", config.get("run", {}).get("seed")))
    if seed_value is None:
        raise ValueError("validation shuffle_buffer sampling requires shuffle_seed, sampling_seed, or run.seed")

    return {
        "sampling_policy": SHUFFLE_BUFFER,
        "shuffle_seed": int(seed_value),
        "shuffle_buffer_size": shuffle_buffer_size,
        "max_blocks_per_document": max_blocks_per_document,
    }


def build_split_sampling_settings(config: dict[str, Any], *, split_name: str) -> dict[str, Any]:
    if split_name == "train":
        metadata = build_sampling_metadata(config)
        return {
            "sampling_policy": metadata["sampling_policy"],
            "shuffle_seed": metadata["shuffle_seed"],
            "shuffle_buffer_size": metadata["shuffle_buffer_size"],
            "max_blocks_per_document": None,
        }

    return build_validation_sampling_settings(config)


def build_validation_coverage_metadata(
    val_stats: dict[str, Any],
    *,
    validation_batches_evaluated: int,
    batch_size: int,
    sequence_length: int,
) -> dict[str, Any]:
    unique_doc_count = val_stats.get("unique_doc_count")
    validation_prefix_only_risk = bool(
        val_stats.get("sampling_policy") == SEQUENTIAL_PREFIX
        or not isinstance(unique_doc_count, int)
        or unique_doc_count <= 1
    )
    return {
        "val_shuffle_seed": val_stats.get("shuffle_seed"),
        "val_shuffle_buffer_size": val_stats.get("shuffle_buffer_size"),
        "validation_max_blocks_per_document": val_stats.get("max_blocks_per_document"),
        "validation_unique_doc_count": unique_doc_count,
        "validation_batches_evaluated": validation_batches_evaluated,
        "validation_tokens_evaluated": validation_batches_evaluated * batch_size * sequence_length,
        "validation_prefix_only_risk": validation_prefix_only_risk,
    }


def repo_relative_path(path: Path) -> str:
    resolved = path if path.is_absolute() else PROJECT_ROOT / path
    return resolved.resolve().relative_to(PROJECT_ROOT.resolve()).as_posix()


def validate_output_dir(output_dir: Path) -> None:
    relative_path = repo_relative_path(output_dir)
    if not relative_path.startswith("experiments/a100/"):
        raise ValueError("output_dir must stay under experiments/a100/")


def path_is_under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def build_run_id_from_config(config: dict[str, Any]) -> str:
    run_name = str(config.get("run", {}).get("run_name", "")).strip()
    if not run_name:
        raise ValueError("run.run_name must be non-empty")
    return f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{run_name}"


def calculate_expected_validation_rows(max_steps: int, eval_interval: int) -> int:
    if eval_interval <= 0:
        return 0
    return max_steps // eval_interval


def count_jsonl_rows(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open("r", encoding="utf-8") as handle:
        return sum(1 for line in handle if line.strip())


def write_validation_metrics_record(path: Path, *, step: int, tokens_seen: int, val_loss: float, timestamp: str) -> None:
    append_jsonl(
        path,
        {
            "step": step,
            "tokens_seen": tokens_seen,
            "val_loss": val_loss,
            "timestamp": timestamp,
        },
    )


def validate_post_run_artifacts(output_dir: Path, *, max_steps: int, expected_validation_rows: int) -> dict[str, Any]:
    summary_json_path = output_dir / "summary.json"
    metrics_path = output_dir / "metrics.jsonl"
    validation_metrics_path = output_dir / "validation_metrics.jsonl"
    run_config_path = output_dir / "run_config.json"
    run_metadata_path = output_dir / "run_metadata.json"
    blockers: list[str] = []

    summary_data: dict[str, Any] = {}
    if summary_json_path.exists():
        summary_data = json.loads(summary_json_path.read_text(encoding="utf-8"))
    else:
        blockers.append("summary.json missing")

    metrics_rows_actual = count_jsonl_rows(metrics_path)
    validation_rows_actual = count_jsonl_rows(validation_metrics_path)

    if not metrics_path.exists():
        blockers.append("metrics.jsonl missing")
    if not validation_metrics_path.exists():
        blockers.append("validation_metrics.jsonl missing")
    if not run_config_path.exists():
        blockers.append("run_config.json missing")
    if not run_metadata_path.exists():
        blockers.append("run_metadata.json missing")
    if metrics_rows_actual != max_steps:
        blockers.append(f"metrics.jsonl row count {metrics_rows_actual} != max_steps {max_steps}")
    if validation_rows_actual != expected_validation_rows:
        blockers.append(
            f"validation_metrics.jsonl row count {validation_rows_actual} != expected {expected_validation_rows}"
        )

    if summary_data:
        if summary_data.get("metrics_rows") != metrics_rows_actual:
            blockers.append("summary metrics_rows does not match metrics.jsonl actual rows")
        if summary_data.get("validation_rows") != validation_rows_actual:
            blockers.append("summary validation_rows does not match validation_metrics.jsonl actual rows")
        checkpoint_path_text = summary_data.get("checkpoint_path")
        if not isinstance(checkpoint_path_text, str):
            blockers.append("summary checkpoint_path missing")
        else:
            checkpoint_path = resolve_repo_path(checkpoint_path_text)
            if not path_is_under(checkpoint_path, output_dir):
                blockers.append("summary checkpoint_path is outside current output_dir")
        if summary_data.get("success") is not True:
            blockers.append("summary success is not true")
        if summary_data.get("checkpoint_reload_match") is not True:
            blockers.append("checkpoint_reload_match is not true")

    return {
        "passed": not blockers,
        "blockers": blockers,
        "summary_json_path": repo_relative_path(summary_json_path),
        "metrics_path": repo_relative_path(metrics_path),
        "validation_metrics_path": repo_relative_path(validation_metrics_path),
        "run_config_path": repo_relative_path(run_config_path),
        "run_metadata_path": repo_relative_path(run_metadata_path),
        "metrics_rows_actual": metrics_rows_actual,
        "validation_rows_actual": validation_rows_actual,
        "expected_metrics_rows": max_steps,
        "expected_validation_rows": expected_validation_rows,
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run or dry-run the A100 FineWeb-Edu 300M 10-step smoke script.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH), help="Path to the A100 smoke config JSON.")
    parser.add_argument("--dry-run", action="store_true", help="Validate config/tokenizer/data/model-count path only.")
    return parser.parse_args()


def choose_runtime_device(config: dict[str, Any], dry_run: bool) -> tuple[torch.device, str]:
    requested_device = str(config.get("hardware", {}).get("device", "cuda")).lower()
    if requested_device == "cuda":
        if torch.cuda.is_available():
            return torch.device("cuda"), "config_cuda"
        if dry_run:
            return torch.device("cpu"), "cpu_fallback_no_cuda"
        raise RuntimeError("config requests cuda but torch.cuda.is_available() is False")
    return torch.device("cpu"), "config_cpu"


def choose_model_dtype(config: dict[str, Any], device: torch.device) -> tuple[torch.dtype, str]:
    if device.type != "cuda":
        return torch.float32, "float32_cpu_fallback"

    precision_policy = str(config.get("hardware", {}).get("precision", "")).lower()
    requested_dtype = str(config.get("hardware", {}).get("dtype", "")).lower()
    bf16_supported = bool(torch.cuda.is_bf16_supported()) if hasattr(torch.cuda, "is_bf16_supported") else False

    if precision_policy == "bf16_if_available_else_fp16":
        if bf16_supported:
            return torch.bfloat16, "bf16"
        return torch.float16, "fp16"

    if requested_dtype == "bf16" and bf16_supported:
        return torch.bfloat16, "bf16"
    if requested_dtype in {"fp16", "float16"}:
        return torch.float16, "fp16"
    return torch.float32, "float32"


def build_declared_model_features(config: dict[str, Any]) -> dict[str, Any]:
    model = config.get("model", {}) if isinstance(config.get("model"), dict) else {}
    profiling = config.get("profiling", {}) if isinstance(config.get("profiling"), dict) else {}
    return {
        "norm_type": model.get("norm_type"),
        "ffn_type": model.get("ffn_type"),
        "position_encoding": model.get("position_encoding"),
        "tie_embeddings": model.get("tie_embeddings"),
        "attention_backend": profiling.get("attention_backend"),
    }


def build_current_core_model_features() -> dict[str, Any]:
    return {
        "norm_type": "rmsnorm",
        "ffn_type": "swiglu",
        "position_encoding": "learned_position_embedding",
        "tie_embeddings": False,
        "attention_backend": "sdpa",
    }


def collect_feature_mismatches(config: dict[str, Any]) -> list[str]:
    declared = build_declared_model_features(config)
    implemented = build_current_core_model_features()
    mismatches: list[str] = []
    for key, implemented_value in implemented.items():
        declared_value = declared.get(key)
        if declared_value != implemented_value:
            mismatches.append(f"{key}: declared={declared_value!r}, implemented={implemented_value!r}")
    return mismatches


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


def count_model_parameters(model: torch.nn.Module) -> int:
    return sum(int(parameter.numel()) for parameter in model.parameters())


def estimate_parameter_memory_gib(parameter_count: int, dtype: torch.dtype) -> float | None:
    bytes_per_param = {
        torch.float32: 4,
        torch.float16: 2,
        torch.bfloat16: 2,
    }.get(dtype)
    if bytes_per_param is None:
        return None
    return parameter_count * bytes_per_param / (1024**3)


def is_memory_limited_exception(exc: Exception) -> bool:
    message = str(exc).lower()
    return isinstance(exc, MemoryError) or "out of memory" in message or "not enough memory" in message


def try_materialize_model(
    model_config: TinyModelConfig,
    device: torch.device,
    dtype: torch.dtype,
) -> tuple[bool, bool, int, str | None]:
    try:
        model = TinyDecoderOnlyTransformer(model_config)
        model.to(device=device)
        if device.type == "cuda":
            model.to(dtype=dtype)
        parameter_count = count_model_parameters(model)
        del model
        if device.type == "cuda":
            torch.cuda.empty_cache()
        return True, False, parameter_count, None
    except Exception as exc:
        if device.type == "cuda":
            torch.cuda.empty_cache()
        if not is_memory_limited_exception(exc):
            raise
        return False, True, count_parameters_exact_from_config(model_config), str(exc)


def extract_bounded_batches(
    split_name: str,
    split_path: Path,
    tokenizer: Tokenizer,
    sequence_length: int,
    batch_size: int,
    required_batches: int,
    eos_token_id: int | None,
) -> tuple[list[tuple[list[list[int]], list[list[int]]]], dict[str, Any]]:
    if required_batches <= 0:
        return [], {
            "split_name": split_name,
            "records_seen": 0,
            "docs_used": 0,
            "empty_text_count": 0,
            "token_ids_collected": 0,
            "available_batches": 0,
            "required_batches": 0,
        }

    required_tokens = required_batches * batch_size * sequence_length + 1
    token_ids: list[int] = []
    records_seen = 0
    docs_used = 0
    empty_text_count = 0

    with split_path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue

            records_seen += 1
            record = json.loads(line)
            text = record.get("text")
            if not isinstance(text, str) or not text.strip():
                empty_text_count += 1
                continue

            source_category = record.get("source_category")
            if source_category != EXPECTED_SOURCE_CATEGORY:
                raise ValueError(
                    f"{split_name} line {line_number} expected source_category {EXPECTED_SOURCE_CATEGORY!r} "
                    f"but found {source_category!r}"
                )

            license_name = record.get("license")
            if license_name != EXPECTED_LICENSE:
                raise ValueError(
                    f"{split_name} line {line_number} expected license {EXPECTED_LICENSE!r} but found {license_name!r}"
                )

            if record.get("allowed_for_training") is not True:
                raise ValueError(f"{split_name} line {line_number} is not approved for training")

            encoded_ids = tokenizer.encode(text).ids
            if not encoded_ids:
                empty_text_count += 1
                continue

            token_ids.extend(encoded_ids)
            if eos_token_id is not None:
                token_ids.append(eos_token_id)
            docs_used += 1

            if len(token_ids) >= required_tokens:
                break

    samples = make_next_token_samples(token_ids, sequence_length)
    batches = batch_samples(samples, batch_size)
    if len(batches) < required_batches:
        raise ValueError(
            f"{split_name} produced only {len(batches)} full batches from {docs_used} docs; need {required_batches}"
        )

    return batches[:required_batches], {
        "split_name": split_name,
        "records_seen": records_seen,
        "docs_used": docs_used,
        "empty_text_count": empty_text_count,
        "token_ids_collected": len(token_ids),
        "available_batches": len(batches),
        "required_batches": required_batches,
        "used_batches": required_batches,
        "sequence_length": sequence_length,
        "batch_size": batch_size,
    }


def compute_grad_norm(parameters) -> float | None:
    total = 0.0
    found_grad = False
    for parameter in parameters:
        if parameter.grad is None:
            continue
        grad_norm = float(parameter.grad.detach().norm(2).item())
        total += grad_norm * grad_norm
        found_grad = True
    if not found_grad:
        return None
    return math.sqrt(total)


def gradients_all_finite(parameters) -> bool:
    found_grad = False
    for parameter in parameters:
        if parameter.grad is None:
            continue
        found_grad = True
        if not bool(torch.isfinite(parameter.grad).all().item()):
            return False
    return found_grad


def autocast_context(device: torch.device, dtype: torch.dtype):
    if device.type == "cuda" and dtype in {torch.float16, torch.bfloat16}:
        return torch.autocast(device_type="cuda", dtype=dtype)
    return nullcontext()


def evaluate_loss(
    model: TinyDecoderOnlyTransformer,
    batch_x: list[list[int]],
    batch_y: list[list[int]],
    device: torch.device,
    dtype: torch.dtype,
) -> float:
    input_ids = torch.tensor(batch_x, dtype=torch.long, device=device)
    target_ids = torch.tensor(batch_y, dtype=torch.long, device=device)

    model.eval()
    with torch.no_grad():
        with autocast_context(device, dtype):
            logits = model(input_ids)
            loss = next_token_cross_entropy(logits, target_ids)

    if not bool(torch.isfinite(loss).item()):
        raise ValueError("validation loss is not finite")
    return float(loss.item())


def run_dry_run(config_path: Path, config: dict[str, Any]) -> int:
    output_dir = resolve_repo_path(config["run"]["output_dir"])
    validate_output_dir(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    tokenizer_path = resolve_repo_path(config["tokenizer"]["path"])
    train_path = resolve_repo_path(config["data"]["train_path"])
    val_path = resolve_repo_path(config["data"]["val_path"])
    expected_vocab_size = int(config["tokenizer"]["vocab_size"])
    sequence_length = int(config["training"].get("sequence_length", config["model"]["context_length"]))
    batch_size = int(config["training"]["batch_size"])
    data_loading_mode = get_data_loading_mode(config)
    eos_token_id = get_eos_token_id(config)
    scheduler_metadata = build_scheduler_metadata(config)
    sampling_metadata = build_sampling_metadata(config)
    train_sampling_settings = build_split_sampling_settings(config, split_name="train")
    val_sampling_settings = build_split_sampling_settings(config, split_name="val")

    tokenizer = Tokenizer.from_file(str(tokenizer_path))
    loaded_vocab_size = tokenizer.get_vocab_size()
    if loaded_vocab_size != expected_vocab_size:
        raise ValueError(f"tokenizer vocab mismatch: expected {expected_vocab_size} but loaded {loaded_vocab_size}")

    if data_loading_mode == "streaming":
        train_batch_iter, train_stats_tracker = create_streaming_batch_iterator(
            split_name="train",
            split_path=train_path,
            tokenizer=tokenizer,
            sequence_length=sequence_length,
            batch_size=batch_size,
            required_batches=1,
            eos_token_id=eos_token_id,
            **train_sampling_settings,
        )
        val_batch_iter, val_stats_tracker = create_streaming_batch_iterator(
            split_name="val",
            split_path=val_path,
            tokenizer=tokenizer,
            sequence_length=sequence_length,
            batch_size=batch_size,
            required_batches=1,
            eos_token_id=eos_token_id,
            **val_sampling_settings,
        )
        train_batches = [next(train_batch_iter)]
        val_batches = [next(val_batch_iter)]
        train_stats = train_stats_tracker.to_dict()
        val_stats = val_stats_tracker.to_dict()
    else:
        train_batches, train_stats = extract_bounded_batches(
            split_name="train",
            split_path=train_path,
            tokenizer=tokenizer,
            sequence_length=sequence_length,
            batch_size=batch_size,
            required_batches=1,
            eos_token_id=eos_token_id,
        )
        val_batches, val_stats = extract_bounded_batches(
            split_name="val",
            split_path=val_path,
            tokenizer=tokenizer,
            sequence_length=sequence_length,
            batch_size=batch_size,
            required_batches=1,
            eos_token_id=eos_token_id,
        )

    runtime_device, runtime_device_reason = choose_runtime_device(config, dry_run=True)
    model_dtype, model_dtype_label = choose_model_dtype(config, runtime_device)
    model_config = model_config_from_dict(config)
    exact_parameter_count = count_parameters_exact_from_config(model_config)
    materialized, memory_limited_local_dry_run, materialized_parameter_count, materialization_error = try_materialize_model(
        model_config,
        runtime_device,
        model_dtype,
    )

    feature_mismatches = collect_feature_mismatches(config)
    summary = {
        "mode": "dry_run",
        "config_path": repo_relative_path(config_path),
        "output_dir": repo_relative_path(output_dir),
        "run_name": config["run"]["run_name"],
        "run_id_will_include_run_name": True,
        "expected_hardware_target": config["hardware"].get("target"),
        "expected_gpu": config["hardware"].get("gpu"),
        "runtime_device": str(runtime_device),
        "runtime_device_reason": runtime_device_reason,
        "runtime_dtype": model_dtype_label,
        "train_path": repo_relative_path(train_path),
        "val_path": repo_relative_path(val_path),
        "tokenizer_path": repo_relative_path(tokenizer_path),
        "tokenizer_vocab_size": loaded_vocab_size,
        "tokenizer_vocab_matches_config": loaded_vocab_size == expected_vocab_size,
        "sequence_length": sequence_length,
        "batch_size": batch_size,
        "data_loading_mode": data_loading_mode,
        "streaming_batches_used": train_stats.get("used_batches", 0) + val_stats.get("used_batches", 0)
        if data_loading_mode == "streaming"
        else 0,
        "host_ram_efficient_batching": data_loading_mode == "streaming",
        "batch_precompute_disabled": data_loading_mode == "streaming",
        "train_batch_shape": [batch_size, sequence_length],
        "val_batch_shape": [batch_size, sequence_length],
        "train_batches_validated": len(train_batches),
        "val_batches_validated": len(val_batches),
        "train_sampling_policy": train_stats.get("sampling_policy"),
        "val_sampling_policy": val_stats.get("sampling_policy"),
        **build_validation_coverage_metadata(
            val_stats,
            validation_batches_evaluated=len(val_batches),
            batch_size=batch_size,
            sequence_length=sequence_length,
        ),
        "train_data_probe": train_stats,
        "val_data_probe": val_stats,
        "model_size_label": config["model"].get("model_size_label"),
        "exact_parameter_count": exact_parameter_count,
        "materialized_parameter_count": materialized_parameter_count,
        "parameter_count_matches_formula": materialized_parameter_count == exact_parameter_count,
        "estimated_parameter_memory_gib": round(estimate_parameter_memory_gib(exact_parameter_count, model_dtype), 6)
        if estimate_parameter_memory_gib(exact_parameter_count, model_dtype) is not None
        else None,
        "model_materialized_locally": materialized,
        "memory_limited_local_dry_run": memory_limited_local_dry_run,
        "materialization_error": materialization_error,
        "declared_model_features": build_declared_model_features(config),
        "current_core_model_features": build_current_core_model_features(),
        "declared_vs_core_feature_mismatches": feature_mismatches,
        "core_model_feature_parity": len(feature_mismatches) == 0,
        **scheduler_metadata,
        **sampling_metadata,
        "no_forward": True,
        "no_backward": True,
        "no_optimizer_step": True,
        "no_checkpoint": True,
        "no_training": True,
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }
    write_json(output_dir / "dry_run_summary.json", summary)

    print(f"mode={summary['mode']}")
    print(f"config_path={summary['config_path']}")
    print(f"output_dir={summary['output_dir']}")
    print(f"runtime_device={summary['runtime_device']}")
    print(f"runtime_dtype={summary['runtime_dtype']}")
    print(f"tokenizer_vocab_size={summary['tokenizer_vocab_size']}")
    print(f"exact_parameter_count={summary['exact_parameter_count']}")
    print(f"model_materialized_locally={summary['model_materialized_locally']}")
    print(f"memory_limited_local_dry_run={summary['memory_limited_local_dry_run']}")
    print(f"core_model_feature_parity={summary['core_model_feature_parity']}")
    print(f"scheduler_policy={summary['scheduler_policy']}")
    print(f"scheduler_applied={summary['scheduler_applied']}")
    print(f"learning_rate_mode={summary['learning_rate_mode']}")
    print(f"sampling_policy={summary['sampling_policy']}")
    print(f"shuffle_seed={summary['shuffle_seed']}")
    print(f"shuffle_buffer_size={summary['shuffle_buffer_size']}")
    print(f"bounded_prefix_batches_only={summary['bounded_prefix_batches_only']}")
    print(f"dry_run_summary_path={repo_relative_path(output_dir / 'dry_run_summary.json')}")
    return 0


def run_training(config_path: Path, config: dict[str, Any]) -> int:
    if bool(config.get("training", {}).get("no_training", False)):
        raise ValueError(
            "training.no_training is true in the current config; flip it to false only for an approved A100 execution step"
        )

    output_dir = resolve_repo_path(config["run"]["output_dir"])
    validate_output_dir(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    runtime_device, runtime_device_reason = choose_runtime_device(config, dry_run=False)
    model_dtype, model_dtype_label = choose_model_dtype(config, runtime_device)
    if runtime_device.type != "cuda":
        raise RuntimeError("non-dry-run training requires cuda")

    if bool(config.get("hardware", {}).get("use_tf32", False)) and hasattr(torch, "set_float32_matmul_precision"):
        torch.set_float32_matmul_precision("high")
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True

    seed = int(config.get("run", {}).get("seed", 336))
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

    tokenizer_path = resolve_repo_path(config["tokenizer"]["path"])
    train_path = resolve_repo_path(config["data"]["train_path"])
    val_path = resolve_repo_path(config["data"]["val_path"])
    expected_vocab_size = int(config["tokenizer"]["vocab_size"])
    tokenizer = Tokenizer.from_file(str(tokenizer_path))
    if tokenizer.get_vocab_size() != expected_vocab_size:
        raise ValueError(f"tokenizer vocab mismatch: expected {expected_vocab_size} but loaded {tokenizer.get_vocab_size()}")

    sequence_length = int(config["training"].get("sequence_length", config["model"]["context_length"]))
    batch_size = int(config["training"]["batch_size"])
    gradient_accumulation_steps = int(config["training"].get("gradient_accumulation_steps", 1))
    max_steps = int(config["training"]["max_steps"])
    eval_interval = int(config["training"].get("eval_interval", 0))
    checkpoint_interval = int(config["training"].get("checkpoint_interval", 0))
    grad_clip = float(config["training"].get("grad_clip", 0.0))
    data_loading_mode = get_data_loading_mode(config)
    eos_token_id = get_eos_token_id(config)
    sampling_metadata = build_sampling_metadata(config)
    train_sampling_settings = build_split_sampling_settings(config, split_name="train")
    val_sampling_settings = build_split_sampling_settings(config, split_name="val")

    train_batches_required = max_steps * gradient_accumulation_steps
    val_batches_required = max_steps // eval_interval if eval_interval > 0 else 0
    if data_loading_mode == "streaming":
        train_batch_iter, train_stats_tracker = create_streaming_batch_iterator(
            split_name="train",
            split_path=train_path,
            tokenizer=tokenizer,
            sequence_length=sequence_length,
            batch_size=batch_size,
            required_batches=train_batches_required,
            eos_token_id=eos_token_id,
            **train_sampling_settings,
        )
        val_batch_iter, val_stats_tracker = create_streaming_batch_iterator(
            split_name="val",
            split_path=val_path,
            tokenizer=tokenizer,
            sequence_length=sequence_length,
            batch_size=batch_size,
            required_batches=max(val_batches_required, 1) if eval_interval > 0 else 0,
            eos_token_id=eos_token_id,
            **val_sampling_settings,
        )
        train_stats = train_stats_tracker.to_dict()
        val_stats = val_stats_tracker.to_dict()
    else:
        train_batches, train_stats = extract_bounded_batches(
            split_name="train",
            split_path=train_path,
            tokenizer=tokenizer,
            sequence_length=sequence_length,
            batch_size=batch_size,
            required_batches=train_batches_required,
            eos_token_id=eos_token_id,
        )
        val_batches, val_stats = extract_bounded_batches(
            split_name="val",
            split_path=val_path,
            tokenizer=tokenizer,
            sequence_length=sequence_length,
            batch_size=batch_size,
            required_batches=max(val_batches_required, 1) if eval_interval > 0 else 0,
            eos_token_id=eos_token_id,
        )

    run_id = build_run_id_from_config(config)
    snapshot_path = snapshot_config(config_path, output_dir)
    env = collect_basic_environment()
    metadata_path = write_run_metadata(
        run_dir=output_dir,
        run_id=run_id,
        project="EduCode-1.5B",
        stage="a100",
        hardware_target=config["hardware"].get("target", "a100_cuda"),
        config_path=str(snapshot_path),
        git_commit=get_git_commit(PROJECT_ROOT),
        git_branch=get_git_branch(PROJECT_ROOT),
        env=env,
        status="running",
        notes=f"{config['run']['run_name']} in progress",
    )

    model_config = model_config_from_dict(config)
    model = TinyDecoderOnlyTransformer(model_config)
    model.to(device=runtime_device)
    model.to(dtype=model_dtype)
    exact_parameter_count = count_model_parameters(model)

    optimizer_config = config.get("optimizer") if isinstance(config.get("optimizer"), dict) else {}
    learning_rate = float(optimizer_config.get("learning_rate", 3e-4))
    scheduler_metadata = build_scheduler_metadata(config, base_learning_rate=learning_rate, final_learning_rate=learning_rate)
    weight_decay = float(optimizer_config.get("weight_decay", 0.0))
    betas = optimizer_config.get("betas", [0.9, 0.95])
    eps = float(optimizer_config.get("eps", 1e-8))
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=learning_rate,
        weight_decay=weight_decay,
        betas=(float(betas[0]), float(betas[1])),
        eps=eps,
    )
    scaler = torch.cuda.amp.GradScaler(enabled=model_dtype == torch.float16)

    metrics_path = output_dir / "metrics.jsonl"
    validation_metrics_path = output_dir / "validation_metrics.jsonl"
    summary_json_path = output_dir / "summary.json"
    summary_path = output_dir / "summary.md"
    checkpoint_manifest_path = output_dir / "checkpoints_manifest.json"
    configured_checkpoint_save_dir = resolve_repo_path(config["checkpoint"]["save_dir"])
    checkpoint_save_dir = output_dir / "checkpoints"
    if configured_checkpoint_save_dir.resolve() != checkpoint_save_dir.resolve():
        raise ValueError("checkpoint.save_dir must equal current output_dir/checkpoints")
    checkpoint_save_dir.mkdir(parents=True, exist_ok=True)

    first_train_loss: float | None = None
    final_train_loss: float | None = None
    final_val_loss: float | None = None
    final_grad_norm: float | None = None
    train_losses: list[float] = []
    val_losses: list[float] = []
    loss_all_finite = True
    val_loss_all_finite = True
    grad_all_finite = True
    total_tokens_seen = 0
    total_elapsed_seconds = 0.0
    last_gpu_memory_allocated_gib: float | None = None
    last_gpu_memory_reserved_gib: float | None = None
    last_checkpoint_path: Path | None = None

    for step in range(1, max_steps + 1):
        model.train()
        optimizer.zero_grad(set_to_none=True)
        step_start = time.perf_counter()
        microbatch_losses: list[float] = []

        for micro_index in range(gradient_accumulation_steps):
            if data_loading_mode == "streaming":
                batch_x, batch_y = next(train_batch_iter)
            else:
                batch_x, batch_y = train_batches[((step - 1) * gradient_accumulation_steps) + micro_index]
            input_ids = torch.tensor(batch_x, dtype=torch.long, device=runtime_device)
            target_ids = torch.tensor(batch_y, dtype=torch.long, device=runtime_device)

            with autocast_context(runtime_device, model_dtype):
                logits = model(input_ids)
                if not bool(torch.isfinite(logits).all().item()):
                    raise ValueError(f"non-finite logits at step {step} microbatch {micro_index + 1}")
                loss = next_token_cross_entropy(logits, target_ids)

            current_loss_finite = bool(torch.isfinite(loss).item())
            if not current_loss_finite:
                raise ValueError(f"non-finite loss at step {step} microbatch {micro_index + 1}")

            microbatch_losses.append(float(loss.item()))
            scaled_loss = loss / gradient_accumulation_steps
            if scaler.is_enabled():
                scaler.scale(scaled_loss).backward()
            else:
                scaled_loss.backward()
            loss_all_finite = loss_all_finite and current_loss_finite

        if scaler.is_enabled():
            scaler.unscale_(optimizer)

        if grad_clip > 0:
            torch.nn.utils.clip_grad_norm_(model.parameters(), grad_clip)

        grad_norm = compute_grad_norm(model.parameters())
        current_grad_finite = gradients_all_finite(model.parameters())
        if grad_norm is None or not current_grad_finite:
            raise ValueError(f"non-finite gradient at step {step}")
        grad_all_finite = grad_all_finite and current_grad_finite

        if scaler.is_enabled():
            scaler.step(optimizer)
            scaler.update()
        else:
            optimizer.step()

        elapsed_seconds = time.perf_counter() - step_start
        total_elapsed_seconds += elapsed_seconds

        current_train_loss = sum(microbatch_losses) / len(microbatch_losses)
        if first_train_loss is None:
            first_train_loss = current_train_loss
        final_train_loss = current_train_loss
        final_grad_norm = float(grad_norm)
        train_losses.append(current_train_loss)

        tokens_this_step = batch_size * sequence_length * gradient_accumulation_steps
        total_tokens_seen += tokens_this_step
        tokens_per_sec = tokens_this_step / elapsed_seconds if elapsed_seconds > 0 else None

        current_val_loss: float | None = None
        if eval_interval > 0 and step % eval_interval == 0:
            if data_loading_mode == "streaming":
                val_batch_x, val_batch_y = next(val_batch_iter)
            else:
                val_batch_x, val_batch_y = val_batches[(step // eval_interval) - 1]
            current_val_loss = evaluate_loss(model, val_batch_x, val_batch_y, runtime_device, model_dtype)
            final_val_loss = current_val_loss
            val_losses.append(current_val_loss)
            val_loss_all_finite = val_loss_all_finite and math.isfinite(current_val_loss)
            write_validation_metrics_record(
                validation_metrics_path,
                step=step,
                tokens_seen=total_tokens_seen,
                val_loss=current_val_loss,
                timestamp=datetime.now().isoformat(timespec="seconds"),
            )

        gpu_memory_allocated_gib = torch.cuda.memory_allocated(runtime_device) / (1024**3)
        gpu_memory_reserved_gib = torch.cuda.memory_reserved(runtime_device) / (1024**3)
        last_gpu_memory_allocated_gib = gpu_memory_allocated_gib
        last_gpu_memory_reserved_gib = gpu_memory_reserved_gib

        write_metrics_record(
            metrics_path,
            step=step,
            tokens_seen=total_tokens_seen,
            train_loss=current_train_loss,
            val_loss=current_val_loss,
            learning_rate=learning_rate,
            grad_norm=final_grad_norm,
            tokens_per_sec=tokens_per_sec,
            gpu_memory_allocated_gib=gpu_memory_allocated_gib,
            gpu_memory_reserved_gib=gpu_memory_reserved_gib,
            mfu=None,
            elapsed_seconds=elapsed_seconds,
            timestamp=datetime.now().isoformat(timespec="seconds"),
        )

        if checkpoint_interval > 0 and step % checkpoint_interval == 0:
            last_checkpoint_path = checkpoint_save_dir / f"checkpoint_step_{step:04d}.pt"
            save_checkpoint(
                path=last_checkpoint_path,
                model=model,
                optimizer=optimizer,
                step=step,
                config=config,
                metadata={
                    "run_id": run_id,
                    "stage": "a100",
                    "notes": f"{config['run']['run_name']} checkpoint",
                },
            )

        if current_val_loss is None:
            print(f"step {step}: train_loss={current_train_loss:.6f} grad_norm={final_grad_norm:.6f}")
        else:
            print(
                f"step {step}: train_loss={current_train_loss:.6f} val_loss={current_val_loss:.6f} "
                f"grad_norm={final_grad_norm:.6f}"
            )

    if last_checkpoint_path is None:
        last_checkpoint_path = checkpoint_save_dir / f"checkpoint_step_{max_steps:04d}.pt"
        save_checkpoint(
            path=last_checkpoint_path,
            model=model,
            optimizer=optimizer,
            step=max_steps,
            config=config,
            metadata={
                "run_id": run_id,
                "stage": "a100",
                "notes": f"{config['run']['run_name']} final checkpoint",
            },
        )

    model_cpu = model.to("cpu")
    reloaded_model = TinyDecoderOnlyTransformer(model_config)
    reloaded_model.to(dtype=model_dtype)
    reloaded_optimizer = torch.optim.AdamW(
        reloaded_model.parameters(),
        lr=learning_rate,
        weight_decay=weight_decay,
        betas=(float(betas[0]), float(betas[1])),
        eps=eps,
    )
    checkpoint = load_checkpoint(last_checkpoint_path, reloaded_model, reloaded_optimizer, map_location="cpu")
    parameter_compare = compare_model_parameters(model_cpu, reloaded_model)
    checkpoint_reload_match = parameter_compare["all_match"] and checkpoint.get("step") == max_steps

    if not path_is_under(last_checkpoint_path, output_dir):
        raise ValueError("checkpoint_path must resolve inside current output_dir")

    metrics_rows = count_jsonl_rows(metrics_path)
    validation_rows = count_jsonl_rows(validation_metrics_path)
    expected_validation_row_count = calculate_expected_validation_rows(max_steps, eval_interval)
    approximate_tokens_per_sec = total_tokens_seen / total_elapsed_seconds if total_elapsed_seconds > 0 else None
    feature_mismatches = collect_feature_mismatches(config)
    if data_loading_mode == "streaming":
        train_stats = train_stats_tracker.to_dict()
        val_stats = val_stats_tracker.to_dict()

    success = (
        first_train_loss is not None
        and final_train_loss is not None
        and final_val_loss is not None
        and final_grad_norm is not None
        and metrics_rows == max_steps
        and validation_rows == expected_validation_row_count
        and loss_all_finite
        and val_loss_all_finite
        and grad_all_finite
        and last_checkpoint_path.exists()
        and checkpoint_reload_match
        and metrics_path.exists()
        and validation_metrics_path.exists()
    )

    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    metadata["end_time"] = datetime.now().isoformat(timespec="seconds")
    metadata["status"] = "success" if success else "failed"
    metadata["notes"] = f"{config['run']['run_name']} complete"
    metadata["torch_version"] = torch.__version__
    metadata["cuda_available"] = torch.cuda.is_available()
    metadata["cuda_version"] = torch.version.cuda
    metadata["cudnn_version"] = torch.backends.cudnn.version() if torch.backends.cudnn.is_available() else None
    metadata["gpu_name"] = torch.cuda.get_device_name(runtime_device)
    metadata["gpu_memory_gib"] = round(torch.cuda.get_device_properties(runtime_device).total_memory / (1024**3), 3)
    write_json(metadata_path, metadata)

    checkpoint_manifest = {
        "run_id": run_id,
        "checkpoint_path": repo_relative_path(last_checkpoint_path),
        "checkpoint_exists": last_checkpoint_path.exists(),
        "checkpoint_reload_match": checkpoint_reload_match,
        "checkpoint_path_starts_with_output_dir": path_is_under(last_checkpoint_path, output_dir),
        "step": max_steps,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }
    write_json(checkpoint_manifest_path, checkpoint_manifest)

    summary_data = {
        "run_id": run_id,
        "run_name": config["run"]["run_name"],
        "config_path": repo_relative_path(config_path),
        "output_dir": repo_relative_path(output_dir),
        "runtime_device": str(runtime_device),
        "runtime_device_reason": runtime_device_reason,
        "runtime_dtype": model_dtype_label,
        "max_steps": max_steps,
        "gradient_accumulation_steps": gradient_accumulation_steps,
        "eval_interval": eval_interval,
        "batch_size": batch_size,
        "sequence_length": sequence_length,
        "data_loading_mode": data_loading_mode,
        "streaming_batches_used": train_stats.get("used_batches", 0) + val_stats.get("used_batches", 0)
        if data_loading_mode == "streaming"
        else 0,
        "host_ram_efficient_batching": data_loading_mode == "streaming",
        "batch_precompute_disabled": data_loading_mode == "streaming",
        "train_batches_used": train_batches_required,
        "val_batches_used": len(val_losses),
        "train_sampling_policy": train_stats.get("sampling_policy"),
        "val_sampling_policy": val_stats.get("sampling_policy"),
        **build_validation_coverage_metadata(
            val_stats,
            validation_batches_evaluated=len(val_losses),
            batch_size=batch_size,
            sequence_length=sequence_length,
        ),
        "train_data_probe": train_stats,
        "val_data_probe": val_stats,
        "tokenizer_vocab_size": tokenizer.get_vocab_size(),
        "exact_parameter_count": exact_parameter_count,
        "first_train_loss": round(first_train_loss, 6) if first_train_loss is not None else None,
        "final_train_loss": round(final_train_loss, 6) if final_train_loss is not None else None,
        "final_val_loss": round(final_val_loss, 6) if final_val_loss is not None else None,
        "loss_all_finite": loss_all_finite,
        "val_loss_all_finite": val_loss_all_finite,
        "grad_all_finite": grad_all_finite,
        "grad_norm_final": round(final_grad_norm, 6) if final_grad_norm is not None else None,
        "metrics_path": repo_relative_path(metrics_path),
        "validation_metrics_path": repo_relative_path(validation_metrics_path),
        "metrics_rows": metrics_rows,
        "validation_rows": validation_rows,
        "expected_validation_rows": expected_validation_row_count,
        "tokens_seen": total_tokens_seen,
        "elapsed_seconds": round(total_elapsed_seconds, 6),
        "approximate_tokens_per_sec": round(approximate_tokens_per_sec, 6)
        if approximate_tokens_per_sec is not None
        else None,
        "checkpoint_path": repo_relative_path(last_checkpoint_path),
        "checkpoint_path_starts_with_output_dir": path_is_under(last_checkpoint_path, output_dir),
        "checkpoint_reload_match": checkpoint_reload_match,
        "last_gpu_memory_allocated_gib": round(last_gpu_memory_allocated_gib, 6)
        if last_gpu_memory_allocated_gib is not None
        else None,
        "last_gpu_memory_reserved_gib": round(last_gpu_memory_reserved_gib, 6)
        if last_gpu_memory_reserved_gib is not None
        else None,
        "declared_model_features": build_declared_model_features(config),
        "current_core_model_features": build_current_core_model_features(),
        "declared_vs_core_feature_mismatches": feature_mismatches,
        **scheduler_metadata,
        **sampling_metadata,
        "success": bool(success),
    }
    write_json(summary_json_path, summary_data)
    artifact_validation = validate_post_run_artifacts(
        output_dir,
        max_steps=max_steps,
        expected_validation_rows=expected_validation_row_count,
    )
    write_json(output_dir / "post_run_artifact_validation_summary.json", artifact_validation)
    success = bool(success and artifact_validation["passed"])
    summary_data["post_run_artifact_validation"] = artifact_validation
    summary_data["success"] = success
    write_json(summary_json_path, summary_data)
    metadata["status"] = "success" if success else "failed"
    write_json(metadata_path, metadata)

    summary_markdown = build_summary_markdown(
        {
            "run_id": run_id,
            "goal": f"Validate the bounded A100/A800 training chain for {config['run']['run_name']}.",
            "hardware": f"{runtime_device} / {config['hardware'].get('target')}",
            "config_path": str(snapshot_path),
            "result": "success" if success else "failed",
            "key_metrics": summary_data,
            "generation_preview": "",
            "notes": "This script uses the current core model implementation without adding new core-model features. Scheduler fields are recorded as present but not applied unless a future implementation actually applies a scheduler.",
            "next_step": "Review the bounded GPU artifacts with the post-run validator before making any model-quality claims.",
        }
    )
    write_text(summary_path, summary_markdown)

    print(f"run_id={run_id}")
    print(f"output_dir={repo_relative_path(output_dir)}")
    print(f"runtime_device={runtime_device}")
    print(f"runtime_dtype={model_dtype_label}")
    print(f"exact_parameter_count={exact_parameter_count}")
    print(f"checkpoint_reload_match={checkpoint_reload_match}")
    print(f"success={success}")
    return 0 if success else 1


def main() -> int:
    args = parse_args()
    config_path = resolve_repo_path(args.config)
    config = load_json_config(config_path)
    errors = validate_config(config, repo_root=PROJECT_ROOT)
    if errors:
        print("validation: failed")
        for error in errors:
            print(f"- {error}")
        return 1

    if args.dry_run:
        return run_dry_run(config_path, config)
    return run_training(config_path, config)


if __name__ == "__main__":
    raise SystemExit(main())
