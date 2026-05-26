from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from tokenizers import Tokenizer

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "configs" / "a100" / "fineweb_edu_500mb_300m_1000step_public16k_execute.json"
MAX_SAMPLE_RECORDS = 100
INT64_BYTES = 8
CPYTHON_INT_APPROX_BYTES = 28
LIST_POINTER_BYTES = 8
LIST_HEADER_APPROX_BYTES = 56
TUPLE_HEADER_APPROX_BYTES = 56
SEQUENTIAL_PREFIX = "sequential_prefix"
SHUFFLE_BUFFER = "shuffle_buffer"
SUPPORTED_SAMPLING_POLICIES = {SEQUENTIAL_PREFIX, SHUFFLE_BUFFER}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect host-RAM pressure for bounded A100/A800 batch preparation.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH), help="Path to an A100/A800 config JSON.")
    return parser.parse_args()


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


def bytes_to_mib(byte_count: int | float) -> float:
    return round(float(byte_count) / (1024**2), 3)


def bytes_to_gib(byte_count: int | float) -> float:
    return round(float(byte_count) / (1024**3), 6)


def get_data_loading_mode(config: dict[str, Any]) -> str:
    data_config = config.get("data", {}) if isinstance(config.get("data"), dict) else {}
    return str(data_config.get("data_loading_mode", config.get("data_loading_mode", "precomputed"))).strip().lower()


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


def sample_split(path: Path, tokenizer: Tokenizer, max_records: int) -> dict[str, Any]:
    records_seen = 0
    texts_used = 0
    empty_text_count = 0
    chars_sampled = 0
    token_ids_sampled = 0

    if not path.exists():
        return {
            "path_exists": False,
            "records_seen": 0,
            "texts_used": 0,
            "empty_text_count": 0,
            "chars_sampled": 0,
            "token_ids_sampled": 0,
            "avg_tokens_per_text": None,
            "max_sample_records": max_records,
        }

    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if records_seen >= max_records:
                break
            if not line.strip():
                continue
            records_seen += 1
            record = json.loads(line)
            text = record.get("text")
            if not isinstance(text, str) or not text.strip():
                empty_text_count += 1
                continue
            encoded_ids = tokenizer.encode(text).ids
            if not encoded_ids:
                empty_text_count += 1
                continue
            texts_used += 1
            chars_sampled += len(text)
            token_ids_sampled += len(encoded_ids)

    return {
        "path_exists": True,
        "records_seen": records_seen,
        "texts_used": texts_used,
        "empty_text_count": empty_text_count,
        "chars_sampled": chars_sampled,
        "token_ids_sampled": token_ids_sampled,
        "avg_tokens_per_text": round(token_ids_sampled / texts_used, 3) if texts_used else None,
        "avg_chars_per_text": round(chars_sampled / texts_used, 3) if texts_used else None,
        "max_sample_records": max_records,
    }


def estimate_current_extract_bounded_batches_memory(
    *,
    required_batches: int,
    batch_size: int,
    sequence_length: int,
) -> dict[str, Any]:
    required_tokens = required_batches * batch_size * sequence_length + 1 if required_batches > 0 else 0
    needed_samples = required_batches * batch_size
    sliding_window_samples = max(required_tokens - sequence_length, 0)
    available_batches = sliding_window_samples // batch_size if batch_size > 0 else 0

    tensor_values = required_batches * batch_size * sequence_length
    input_tensor_bytes = tensor_values * INT64_BYTES
    label_tensor_bytes = tensor_values * INT64_BYTES
    token_buffer_bytes = required_tokens * (CPYTHON_INT_APPROX_BYTES + LIST_POINTER_BYTES)
    sliding_sample_pointer_bytes = sliding_window_samples * 2 * sequence_length * LIST_POINTER_BYTES
    sliding_sample_container_bytes = sliding_window_samples * (2 * LIST_HEADER_APPROX_BYTES + TUPLE_HEADER_APPROX_BYTES)
    samples_list_pointer_bytes = sliding_window_samples * LIST_POINTER_BYTES
    normalized_samples_pointer_bytes = sliding_window_samples * LIST_POINTER_BYTES
    batch_xy_pointer_bytes = available_batches * 2 * batch_size * LIST_POINTER_BYTES
    batch_container_bytes = available_batches * (3 * LIST_HEADER_APPROX_BYTES + TUPLE_HEADER_APPROX_BYTES)
    estimated_current_python_precompute_bytes = (
        token_buffer_bytes
        + sliding_sample_pointer_bytes
        + sliding_sample_container_bytes
        + samples_list_pointer_bytes
        + normalized_samples_pointer_bytes
        + batch_xy_pointer_bytes
        + batch_container_bytes
    )

    return {
        "required_batches": required_batches,
        "required_tokens_formula": "required_batches * batch_size * sequence_length + 1",
        "required_tokens": required_tokens,
        "needed_non_overlapping_samples": needed_samples,
        "current_sliding_window_samples": sliding_window_samples,
        "current_available_batches_before_slice": available_batches,
        "current_unused_batches_before_slice": max(available_batches - required_batches, 0),
        "estimated_input_tensor_memory_mib": bytes_to_mib(input_tensor_bytes),
        "estimated_label_tensor_memory_mib": bytes_to_mib(label_tensor_bytes),
        "estimated_input_plus_label_tensor_memory_mib": bytes_to_mib(input_tensor_bytes + label_tensor_bytes),
        "estimated_token_buffer_python_memory_mib": bytes_to_mib(token_buffer_bytes),
        "estimated_sliding_sample_pointer_memory_gib": bytes_to_gib(sliding_sample_pointer_bytes),
        "estimated_current_python_precompute_bytes": estimated_current_python_precompute_bytes,
        "estimated_current_python_precompute_memory_gib": bytes_to_gib(estimated_current_python_precompute_bytes),
        "current_plan_likely_precomputes_too_much": sliding_window_samples > max(needed_samples * 8, 100_000),
    }


def estimate_streaming_batch_memory(
    *,
    current_precompute_bytes: int,
    batch_size: int,
    sequence_length: int,
) -> dict[str, Any]:
    tensor_values = batch_size * sequence_length
    input_tensor_bytes = tensor_values * INT64_BYTES
    label_tensor_bytes = tensor_values * INT64_BYTES
    rolling_buffer_bytes = (sequence_length + 1) * (CPYTHON_INT_APPROX_BYTES + LIST_POINTER_BYTES)
    batch_row_pointer_bytes = 2 * batch_size * LIST_POINTER_BYTES
    batch_sequence_pointer_bytes = 2 * batch_size * sequence_length * LIST_POINTER_BYTES
    batch_sequence_container_bytes = 2 * batch_size * LIST_HEADER_APPROX_BYTES
    batch_container_bytes = 2 * LIST_HEADER_APPROX_BYTES + TUPLE_HEADER_APPROX_BYTES
    steady_state_python_bytes = (
        rolling_buffer_bytes
        + batch_row_pointer_bytes
        + batch_sequence_pointer_bytes
        + batch_sequence_container_bytes
        + batch_container_bytes
    )
    steady_state_total_bytes = input_tensor_bytes + label_tensor_bytes + steady_state_python_bytes

    return {
        "streaming_formula": "current microbatch tensors + rolling token buffer + current Python batch lists",
        "streaming_estimated_input_tensor_memory_mib": bytes_to_mib(input_tensor_bytes),
        "streaming_estimated_label_tensor_memory_mib": bytes_to_mib(label_tensor_bytes),
        "streaming_estimated_batch_tensor_memory_mib": bytes_to_mib(input_tensor_bytes + label_tensor_bytes),
        "streaming_estimated_rolling_buffer_python_memory_mib": bytes_to_mib(rolling_buffer_bytes),
        "streaming_estimated_batch_python_memory_mib": bytes_to_mib(steady_state_python_bytes),
        "streaming_estimated_total_steady_state_memory_mib": bytes_to_mib(steady_state_total_bytes),
        "streaming_expected_host_ram_safe": steady_state_total_bytes < 1024**3,
        "reduction_factor_estimate": round(current_precompute_bytes / steady_state_total_bytes, 3)
        if steady_state_total_bytes > 0
        else None,
    }


def estimate_shuffle_buffer_memory(sample: dict[str, Any], shuffle_buffer_size: int) -> dict[str, Any]:
    avg_chars_per_text = sample.get("avg_chars_per_text")
    if not isinstance(avg_chars_per_text, (int, float)) or shuffle_buffer_size <= 1:
        estimated_text_payload_bytes = 0
    else:
        estimated_text_payload_bytes = int(float(avg_chars_per_text) * shuffle_buffer_size * 4)
    buffer_pointer_bytes = max(shuffle_buffer_size, 0) * LIST_POINTER_BYTES
    estimated_total_bytes = estimated_text_payload_bytes + buffer_pointer_bytes + LIST_HEADER_APPROX_BYTES

    return {
        "shuffle_buffer_size": shuffle_buffer_size,
        "estimated_text_payload_memory_mib": bytes_to_mib(estimated_text_payload_bytes),
        "estimated_buffer_pointer_memory_mib": bytes_to_mib(buffer_pointer_bytes),
        "estimated_total_shuffle_buffer_memory_mib": bytes_to_mib(estimated_total_bytes),
        "estimate_uses_sample_avg_chars_per_text": avg_chars_per_text,
        "does_not_read_entire_corpus": True,
    }


def main() -> int:
    args = parse_args()
    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = PROJECT_ROOT / config_path

    config = load_json(config_path)
    data_loading_mode = get_data_loading_mode(config)
    sampling_metadata = build_sampling_metadata(config)
    train_path = resolve_repo_path(str(config["data"]["train_path"]))
    val_path = resolve_repo_path(str(config["data"]["val_path"]))
    tokenizer_path = resolve_repo_path(str(config["tokenizer"]["path"]))
    output_dir = resolve_repo_path(str(config["run"]["output_dir"]))
    summary_path = output_dir / "batch_memory_plan_summary.json"

    tokenizer = Tokenizer.from_file(str(tokenizer_path)) if tokenizer_path.exists() else None
    tokenizer_vocab_size = tokenizer.get_vocab_size() if tokenizer is not None else None

    max_steps = int(config["training"]["max_steps"])
    batch_size = int(config["training"]["batch_size"])
    gradient_accumulation_steps = int(config["training"].get("gradient_accumulation_steps", 1))
    sequence_length = int(config["training"].get("sequence_length", config["model"]["context_length"]))
    eval_interval = int(config["training"].get("eval_interval", 0))
    required_train_batches = max_steps * gradient_accumulation_steps
    required_val_batches = max_steps // eval_interval if eval_interval > 0 else 0
    current_val_batches_requested = max(required_val_batches, 1) if eval_interval > 0 else 0

    train_sample = sample_split(train_path, tokenizer, MAX_SAMPLE_RECORDS) if tokenizer is not None else {"path_exists": train_path.exists()}
    val_sample = sample_split(val_path, tokenizer, MAX_SAMPLE_RECORDS) if tokenizer is not None else {"path_exists": val_path.exists()}
    train_memory = estimate_current_extract_bounded_batches_memory(
        required_batches=required_train_batches,
        batch_size=batch_size,
        sequence_length=sequence_length,
    )
    val_memory = estimate_current_extract_bounded_batches_memory(
        required_batches=current_val_batches_requested,
        batch_size=batch_size,
        sequence_length=sequence_length,
    )
    train_streaming_memory = estimate_streaming_batch_memory(
        current_precompute_bytes=int(train_memory["estimated_current_python_precompute_bytes"]),
        batch_size=batch_size,
        sequence_length=sequence_length,
    )
    val_streaming_memory = estimate_streaming_batch_memory(
        current_precompute_bytes=int(val_memory["estimated_current_python_precompute_bytes"]),
        batch_size=batch_size,
        sequence_length=sequence_length,
    )
    train_shuffle_buffer_memory = estimate_shuffle_buffer_memory(
        train_sample,
        int(sampling_metadata["shuffle_buffer_size"]),
    )

    summary = {
        "config_path": repo_relative_path(config_path),
        "run_name": config["run"]["run_name"],
        "output_dir": repo_relative_path(output_dir),
        "train_path": repo_relative_path(train_path),
        "val_path": repo_relative_path(val_path),
        "tokenizer_path": repo_relative_path(tokenizer_path),
        "train_path_exists": train_path.exists(),
        "val_path_exists": val_path.exists(),
        "tokenizer_path_exists": tokenizer_path.exists(),
        "tokenizer_vocab_size": tokenizer_vocab_size,
        "config_tokenizer_vocab_size": config["tokenizer"].get("vocab_size"),
        "max_steps": max_steps,
        "batch_size": batch_size,
        "gradient_accumulation_steps": gradient_accumulation_steps,
        "sequence_length": sequence_length,
        "eval_interval": eval_interval,
        "data_loading_mode": data_loading_mode,
        **sampling_metadata,
        "host_ram_efficient_batching": data_loading_mode == "streaming",
        "batch_precompute_disabled": data_loading_mode == "streaming",
        "required_train_batches": required_train_batches,
        "required_val_batches": required_val_batches,
        "current_val_batches_requested": current_val_batches_requested,
        "train_memory_plan": train_memory,
        "val_memory_plan": val_memory,
        "train_streaming_memory_plan": train_streaming_memory,
        "val_streaming_memory_plan": val_streaming_memory,
        "train_shuffle_buffer_memory_plan": train_shuffle_buffer_memory,
        "estimated_shuffle_buffer_memory_note": "Estimated from at most MAX_SAMPLE_RECORDS local records; no full corpus scan is performed.",
        "current_precomputed_estimated_python_memory_gib": train_memory["estimated_current_python_precompute_memory_gib"],
        "streaming_estimated_batch_tensor_memory_mib": train_streaming_memory[
            "streaming_estimated_batch_tensor_memory_mib"
        ],
        "streaming_expected_host_ram_safe": train_streaming_memory["streaming_expected_host_ram_safe"],
        "reduction_factor_estimate": train_streaming_memory["reduction_factor_estimate"],
        "sample_limits": {
            "max_records_per_split": MAX_SAMPLE_RECORDS,
            "does_not_read_entire_corpus": True,
        },
        "train_sample": train_sample,
        "val_sample": val_sample,
        "risk_review": {
            "precomputed_path_collects_token_ids_until_required_tokens": True,
            "precomputed_path_materializes_make_next_token_samples_list": True,
            "precomputed_path_batches_all_available_sliding_samples_before_slice": True,
            "active_path_keeps_train_batches_list_for_full_run": data_loading_mode != "streaming",
            "active_path_keeps_val_batches_list_for_full_run": data_loading_mode != "streaming",
            "streaming_iterator_enabled": data_loading_mode == "streaming",
            "streaming_iterator_recommended": True,
            "likely_host_ram_bottleneck_without_streaming": bool(train_memory["current_plan_likely_precomputes_too_much"]),
        },
        "no_training": True,
        "no_model_materialization": True,
        "no_checkpoint": True,
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }
    write_json(summary_path, summary)

    print(f"summary_path={repo_relative_path(summary_path)}")
    print(f"tokenizer_vocab_size={tokenizer_vocab_size}")
    print(f"max_steps={max_steps}")
    print(f"batch_size={batch_size}")
    print(f"gradient_accumulation_steps={gradient_accumulation_steps}")
    print(f"data_loading_mode={data_loading_mode}")
    print(f"sampling_policy={summary['sampling_policy']}")
    print(f"shuffle_seed={summary['shuffle_seed']}")
    print(f"shuffle_buffer_size={summary['shuffle_buffer_size']}")
    print(f"required_train_batches={required_train_batches}")
    print(f"required_val_batches={required_val_batches}")
    print(
        "current_precomputed_estimated_python_memory_gib="
        f"{summary['current_precomputed_estimated_python_memory_gib']}"
    )
    print(f"streaming_estimated_batch_tensor_memory_mib={summary['streaming_estimated_batch_tensor_memory_mib']}")
    print(f"streaming_expected_host_ram_safe={summary['streaming_expected_host_ram_safe']}")
    print(f"reduction_factor_estimate={summary['reduction_factor_estimate']}")
    print("no_training=True")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
