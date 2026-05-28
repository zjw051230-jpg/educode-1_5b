from __future__ import annotations

import json
import shutil
import subprocess
import tarfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import modal

APP_NAME = "educode-a100-streaming"
VOLUME_NAME = "educode-data"
VOLUME_MOUNT_PATH = Path("/vol")
WORKSPACE_ROOT = Path("/workspace")
REPO_DIR = WORKSPACE_ROOT / "educode-1_5b"
REPO_URL = "https://github.com/zjw051230-jpg/educode-1_5b.git"
REQUIRED_COMMIT = "a8c2bb9"
DEFAULT_GPU = "A100-40GB"
TIMEOUT_SECONDS = 2 * 60 * 60
FIVE_GB_REQUIRED_PACKAGE_FILES = (
    "data/public_corpus/fineweb_edu_sample10bt_5gb/manifest.json",
    "data/public_corpus/fineweb_edu_sample10bt_5gb/validation_summary.json",
    "data/public_corpus/fineweb_edu_sample10bt_5gb/intake_summary.json",
    "data/public_corpus/fineweb_edu_sample10bt_5gb/intake_validation_summary.json",
    "data/public_corpus/fineweb_edu_sample10bt_5gb/splits/fineweb_edu_5gb.train.jsonl",
    "data/public_corpus/fineweb_edu_sample10bt_5gb/splits/fineweb_edu_5gb.val.jsonl",
)
FIVE_GB_VALIDATION_COVERAGE_REQUIRED_PACKAGE_FILES = (
    "data/public_corpus/fineweb_edu_sample10bt_5gb/manifest.json",
    "data/public_corpus/fineweb_edu_sample10bt_5gb/validation_summary.json",
    "data/public_corpus/fineweb_edu_sample10bt_5gb/intake_validation_summary.json",
    "data/public_corpus/fineweb_edu_sample10bt_5gb/splits/fineweb_edu_5gb.val.jsonl",
)
LOCAL_VALIDATION_COVERAGE_IMPORT_DIR = (
    Path(__file__).resolve().parents[1]
    / "experiments"
    / "a100"
    / "fineweb_edu_5gb_300m_1000step_public16k_execute"
    / "results_imported_modal_validation_coverage_preflight"
)
VALIDATION_COVERAGE_SUMMARY_KEYS = (
    "preflight_status",
    "mode",
    "config_path",
    "val_path",
    "used_gpu",
    "ran_training",
    "ran_backward",
    "ran_optimizer_step",
    "saved_checkpoint",
    "val_sampling_policy",
    "val_shuffle_seed",
    "val_shuffle_buffer_size",
    "validation_max_blocks_per_document",
    "validation_unique_doc_count",
    "validation_batches_evaluated",
    "validation_tokens_evaluated",
    "validation_prefix_only_risk",
    "val_data_probe",
    "blockers",
    "blocker_count",
    "checked_at",
)

app = modal.App(APP_NAME)
DATA_VOLUME = modal.Volume.from_name(VOLUME_NAME, create_if_missing=False)
IMAGE = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("git")
    .pip_install(
        "torch",
        "datasets",
        "huggingface_hub",
        "tokenizers",
        "tqdm",
        "numpy",
    )
)


@dataclass(frozen=True)
class ModeSpec:
    config_path: str
    package_path: str
    extract_dir: str
    train_path: str
    val_path: str
    result_dir: str
    train: bool
    result_package: str | None = None
    required_package_files: tuple[str, ...] = ()
    validation_coverage_preflight: bool = False
    cpu_only: bool = False
    extract_required_files_only: bool = False
    requires_train_split: bool = True


MODE_SPECS = {
    "preflight_2gb_1000": ModeSpec(
        config_path="configs/a100/fineweb_edu_2gb_300m_1000step_public16k_execute.json",
        package_path="/vol/prepared/fineweb_edu_2gb_prepared_splits.tar.gz",
        extract_dir="data/public_corpus/fineweb_edu_sample10bt_2gb",
        train_path="data/public_corpus/fineweb_edu_sample10bt_2gb/splits/fineweb_edu_2gb.train.jsonl",
        val_path="data/public_corpus/fineweb_edu_sample10bt_2gb/splits/fineweb_edu_2gb.val.jsonl",
        result_dir="/vol/results/modal_preflight_2gb_1000",
        train=False,
    ),
    "train_2gb_1000": ModeSpec(
        config_path="configs/a100/fineweb_edu_2gb_300m_1000step_public16k_execute.json",
        package_path="/vol/prepared/fineweb_edu_2gb_prepared_splits.tar.gz",
        extract_dir="data/public_corpus/fineweb_edu_sample10bt_2gb",
        train_path="data/public_corpus/fineweb_edu_sample10bt_2gb/splits/fineweb_edu_2gb.train.jsonl",
        val_path="data/public_corpus/fineweb_edu_sample10bt_2gb/splits/fineweb_edu_2gb.val.jsonl",
        result_dir="/vol/results/modal_train_2gb_1000",
        train=True,
        result_package="/vol/results/mvp21_a100_2gb_1000step_public16k_streaming_results.tar.gz",
    ),
    "train_2gb_3000": ModeSpec(
        config_path="configs/a100/fineweb_edu_2gb_300m_3000step_public16k_execute.json",
        package_path="/vol/prepared/fineweb_edu_2gb_prepared_splits.tar.gz",
        extract_dir="data/public_corpus/fineweb_edu_sample10bt_2gb",
        train_path="data/public_corpus/fineweb_edu_sample10bt_2gb/splits/fineweb_edu_2gb.train.jsonl",
        val_path="data/public_corpus/fineweb_edu_sample10bt_2gb/splits/fineweb_edu_2gb.val.jsonl",
        result_dir="/vol/results/modal_train_2gb_3000",
        train=True,
        result_package="/vol/results/mvp22_a100_2gb_3000step_public16k_streaming_results.tar.gz",
    ),
    "preflight_5gb_1000": ModeSpec(
        config_path="configs/a100/fineweb_edu_5gb_300m_1000step_public16k_execute.json",
        package_path="/vol/prepared/fineweb_edu_5gb_prepared_splits.tar.gz",
        extract_dir="data/public_corpus/fineweb_edu_sample10bt_5gb",
        train_path="data/public_corpus/fineweb_edu_sample10bt_5gb/splits/fineweb_edu_5gb.train.jsonl",
        val_path="data/public_corpus/fineweb_edu_sample10bt_5gb/splits/fineweb_edu_5gb.val.jsonl",
        result_dir="/vol/results/modal_preflight_5gb_1000",
        train=False,
        required_package_files=FIVE_GB_REQUIRED_PACKAGE_FILES,
    ),
    "train_5gb_1000": ModeSpec(
        config_path="configs/a100/fineweb_edu_5gb_300m_1000step_public16k_execute.json",
        package_path="/vol/prepared/fineweb_edu_5gb_prepared_splits.tar.gz",
        extract_dir="data/public_corpus/fineweb_edu_sample10bt_5gb",
        train_path="data/public_corpus/fineweb_edu_sample10bt_5gb/splits/fineweb_edu_5gb.train.jsonl",
        val_path="data/public_corpus/fineweb_edu_sample10bt_5gb/splits/fineweb_edu_5gb.val.jsonl",
        result_dir="/vol/results/modal_train_5gb_1000",
        train=True,
        result_package="/vol/results/mvp24_a100_5gb_1000step_public16k_streaming_results.tar.gz",
        required_package_files=FIVE_GB_REQUIRED_PACKAGE_FILES,
    ),
    "preflight_5gb_validation_coverage": ModeSpec(
        config_path="configs/a100/fineweb_edu_5gb_300m_1000step_public16k_execute.json",
        package_path="/vol/prepared/fineweb_edu_5gb_prepared_splits.tar.gz",
        extract_dir="data/public_corpus/fineweb_edu_sample10bt_5gb",
        train_path="data/public_corpus/fineweb_edu_sample10bt_5gb/splits/fineweb_edu_5gb.train.jsonl",
        val_path="data/public_corpus/fineweb_edu_sample10bt_5gb/splits/fineweb_edu_5gb.val.jsonl",
        result_dir="/vol/results/modal_preflight_5gb_validation_coverage",
        train=False,
        required_package_files=FIVE_GB_VALIDATION_COVERAGE_REQUIRED_PACKAGE_FILES,
        validation_coverage_preflight=True,
        cpu_only=True,
        extract_required_files_only=True,
        requires_train_split=False,
    ),
}


def run_command(command: list[str], cwd: Path | None = None) -> None:
    print("$ " + " ".join(command), flush=True)
    completed = subprocess.run(command, cwd=cwd, text=True)
    if completed.returncode != 0:
        raise RuntimeError(f"command failed with exit code {completed.returncode}: {' '.join(command)}")


def read_command(command: list[str], cwd: Path | None = None) -> str:
    print("$ " + " ".join(command), flush=True)
    completed = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    if completed.stdout:
        print(completed.stdout, end="")
    if completed.stderr:
        print(completed.stderr, end="")
    if completed.returncode != 0:
        raise RuntimeError(f"command failed with exit code {completed.returncode}: {' '.join(command)}")
    return completed.stdout.strip()


def safe_extract(package_path: Path, destination: Path) -> list[str]:
    destination.mkdir(parents=True, exist_ok=True)
    extracted: list[str] = []
    with tarfile.open(package_path, "r:gz") as archive:
        for member in archive.getmembers():
            target = (destination / member.name).resolve()
            if not target.is_relative_to(destination.resolve()):
                raise ValueError(f"unsafe tar member path: {member.name}")
            extracted.append(member.name)
        archive.extractall(destination)
    return extracted


def safe_extract_required_files(package_path: Path, destination: Path, required_files: tuple[str, ...]) -> list[str]:
    destination.mkdir(parents=True, exist_ok=True)
    required = set(required_files)
    extracted: list[str] = []
    with tarfile.open(package_path, "r:gz") as archive:
        members_by_name = {member.name: member for member in archive.getmembers()}
        missing = sorted(required - set(members_by_name))
        if missing:
            raise FileNotFoundError(f"missing required package members: {missing}")
        for file_path in required_files:
            member = members_by_name[file_path]
            target = (destination / member.name).resolve()
            if not target.is_relative_to(destination.resolve()):
                raise ValueError(f"unsafe tar member path: {member.name}")
            archive.extract(member, destination)
            extracted.append(member.name)
    return extracted


def clone_repo(repo_url: str, ref: str) -> str:
    if REPO_DIR.exists():
        shutil.rmtree(REPO_DIR)
    WORKSPACE_ROOT.mkdir(parents=True, exist_ok=True)
    run_command(["git", "clone", repo_url, str(REPO_DIR)])
    run_command(["git", "checkout", ref], cwd=REPO_DIR)
    if ref == "main":
        run_command(["git", "pull", "--ff-only"], cwd=REPO_DIR)
    history = read_command(["git", "log", "--oneline", "-n", "100"], cwd=REPO_DIR)
    if REQUIRED_COMMIT not in history:
        raise RuntimeError(f"required commit {REQUIRED_COMMIT} not found in cloned repo history")
    return read_command(["git", "rev-parse", "--short", "HEAD"], cwd=REPO_DIR)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def copy_required_file(source: Path, destination: Path) -> None:
    if not source.exists():
        raise FileNotFoundError(f"missing expected output file: {source}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def write_receipt(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_local_validation_coverage_artifacts(receipt: dict[str, Any]) -> None:
    summary = {key: receipt.get(key) for key in VALIDATION_COVERAGE_SUMMARY_KEYS}
    write_receipt(LOCAL_VALIDATION_COVERAGE_IMPORT_DIR / "modal_preflight_receipt.json", receipt)
    write_receipt(LOCAL_VALIDATION_COVERAGE_IMPORT_DIR / "validation_coverage_preflight_summary.json", summary)


def repo_absolute_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return REPO_DIR / path


def verify_required_package_files(spec: ModeSpec) -> list[str]:
    verified_files: list[str] = []
    for file_path in spec.required_package_files:
        path = REPO_DIR / file_path
        if not path.exists():
            raise FileNotFoundError(f"missing required prepared package file after extraction: {file_path}")
        verified_files.append(file_path)
    return verified_files


def run_preflight(spec: ModeSpec, result_dir: Path) -> dict[str, Any]:
    config_path = repo_absolute_path(spec.config_path)
    run_command(["python", "scripts/inspect_training_batch_memory_plan.py", "--config", config_path.as_posix()], cwd=REPO_DIR)
    run_command(
        ["python", "scripts/run_a100_300m_fineweb_edu_10step_training.py", "--config", config_path.as_posix(), "--dry-run"],
        cwd=REPO_DIR,
    )
    run_command(["python", "scripts/check_a100_execution_readiness.py", "--config", config_path.as_posix()], cwd=REPO_DIR)

    config = load_json(config_path)
    output_dir = REPO_DIR / config["run"]["output_dir"]
    copied_files = []
    for filename in ["batch_memory_plan_summary.json", "dry_run_summary.json", "execution_readiness_summary.json"]:
        copy_required_file(output_dir / filename, result_dir / filename)
        copied_files.append(filename)

    readiness = load_json(output_dir / "execution_readiness_summary.json")
    dry_run = load_json(output_dir / "dry_run_summary.json")
    memory_plan = load_json(output_dir / "batch_memory_plan_summary.json")
    return {
        "memory_plan_status": "success",
        "dry_run_status": "success",
        "readiness_status": readiness.get("status"),
        "ready_for_a100_execution": readiness.get("ready_for_a100_execution"),
        "ready_for_a800_execution": readiness.get("ready_for_a800_execution"),
        "blockers": readiness.get("blockers", []),
        "copied_files": copied_files,
        "data_loading_mode": readiness.get("data_loading_mode"),
        "batch_size": memory_plan.get("batch_size"),
        "gradient_accumulation_steps": memory_plan.get("gradient_accumulation_steps"),
        "max_steps": readiness.get("max_steps"),
        "tokenizer_vocab_size": readiness.get("tokenizer_vocab_size"),
        "parameter_count": dry_run.get("exact_parameter_count"),
    }


def build_validation_sampling_settings_for_preflight(config: dict[str, Any]) -> dict[str, Any]:
    validation_sampling = config.get("validation_sampling")
    if not isinstance(validation_sampling, dict):
        return {
            "sampling_policy": "sequential_prefix",
            "shuffle_seed": None,
            "shuffle_buffer_size": 1,
            "max_blocks_per_document": None,
        }

    policy = str(validation_sampling.get("policy", "sequential_prefix")).strip().lower()
    shuffle_buffer_size = int(validation_sampling.get("shuffle_buffer_size", 1))
    max_blocks_value = validation_sampling.get("max_blocks_per_document")
    max_blocks_per_document = int(max_blocks_value) if max_blocks_value is not None else None
    seed_value = validation_sampling.get("shuffle_seed", validation_sampling.get("sampling_seed", config.get("run", {}).get("seed")))
    return {
        "sampling_policy": policy,
        "shuffle_seed": int(seed_value) if seed_value is not None else None,
        "shuffle_buffer_size": shuffle_buffer_size,
        "max_blocks_per_document": max_blocks_per_document,
    }


def get_eos_token_id_for_preflight(config: dict[str, Any]) -> int | None:
    tokenizer_config = config.get("tokenizer", {}) if isinstance(config.get("tokenizer"), dict) else {}
    eos_token_id = tokenizer_config.get("eos_token_id", tokenizer_config.get("endoftext_token_id"))
    return eos_token_id if isinstance(eos_token_id, int) else None


def run_validation_coverage_preflight(spec: ModeSpec, result_dir: Path) -> dict[str, Any]:
    import sys

    scripts_path = REPO_DIR / "scripts"
    if str(scripts_path) not in sys.path:
        sys.path.insert(0, str(scripts_path))

    from tokenizers import Tokenizer
    from streaming_lm_batch_iterator import create_streaming_batch_iterator

    config_path = repo_absolute_path(spec.config_path)
    config = load_json(config_path)
    val_path = repo_absolute_path(spec.val_path)
    tokenizer_path = repo_absolute_path(config["tokenizer"]["path"])
    tokenizer = Tokenizer.from_file(str(tokenizer_path))

    sequence_length = int(config["training"].get("sequence_length", config["model"]["context_length"]))
    batch_size = int(config["training"]["batch_size"])
    max_steps = int(config["training"]["max_steps"])
    eval_interval = int(config["training"].get("eval_interval", 0))
    validation_batches_required = max_steps // eval_interval if eval_interval > 0 else 0
    if validation_batches_required <= 0:
        raise ValueError("validation coverage preflight requires eval_interval > 0")

    val_sampling_settings = build_validation_sampling_settings_for_preflight(config)
    val_batch_iter, val_stats_tracker = create_streaming_batch_iterator(
        split_name="val",
        split_path=val_path,
        tokenizer=tokenizer,
        sequence_length=sequence_length,
        batch_size=batch_size,
        required_batches=validation_batches_required,
        eos_token_id=get_eos_token_id_for_preflight(config),
        **val_sampling_settings,
    )

    validation_batches_evaluated = 0
    try:
        for _ in range(validation_batches_required):
            next(val_batch_iter)
            validation_batches_evaluated += 1
    finally:
        close = getattr(val_batch_iter, "close", None)
        if close is not None:
            close()

    val_stats = val_stats_tracker.to_dict()
    validation_unique_doc_count = val_stats.get("unique_doc_count")
    validation_prefix_only_risk = bool(
        val_stats.get("sampling_policy") == "sequential_prefix"
        or not isinstance(validation_unique_doc_count, int)
        or validation_unique_doc_count <= 1
    )
    validation_tokens_evaluated = validation_batches_evaluated * batch_size * sequence_length
    blockers: list[str] = []
    if val_stats.get("sampling_policy") != "shuffle_buffer":
        blockers.append(f"val_sampling_policy expected 'shuffle_buffer', got {val_stats.get('sampling_policy')!r}")
    if val_stats.get("shuffle_seed") != 7331:
        blockers.append(f"val_shuffle_seed expected 7331, got {val_stats.get('shuffle_seed')!r}")
    if val_stats.get("shuffle_buffer_size") != 64:
        blockers.append(f"val_shuffle_buffer_size expected 64, got {val_stats.get('shuffle_buffer_size')!r}")
    if val_stats.get("max_blocks_per_document") != 8:
        blockers.append(f"validation_max_blocks_per_document expected 8, got {val_stats.get('max_blocks_per_document')!r}")
    if validation_unique_doc_count is None or validation_unique_doc_count <= 1:
        blockers.append(f"validation_unique_doc_count must be greater than 1, got {validation_unique_doc_count!r}")
    if validation_batches_evaluated <= 0:
        blockers.append("validation_batches_evaluated must be greater than 0")
    if validation_tokens_evaluated <= 0:
        blockers.append("validation_tokens_evaluated must be greater than 0")
    if validation_prefix_only_risk:
        blockers.append("validation_prefix_only_risk must be false")

    summary = {
        "preflight_status": "passed" if not blockers else "failed",
        "mode": "preflight_5gb_validation_coverage",
        "config_path": spec.config_path,
        "val_path": spec.val_path,
        "used_gpu": False,
        "ran_training": False,
        "ran_backward": False,
        "ran_optimizer_step": False,
        "saved_checkpoint": False,
        "val_sampling_policy": val_stats.get("sampling_policy"),
        "val_shuffle_seed": val_stats.get("shuffle_seed"),
        "val_shuffle_buffer_size": val_stats.get("shuffle_buffer_size"),
        "validation_max_blocks_per_document": val_stats.get("max_blocks_per_document"),
        "validation_unique_doc_count": validation_unique_doc_count,
        "validation_batches_evaluated": validation_batches_evaluated,
        "validation_tokens_evaluated": validation_tokens_evaluated,
        "validation_prefix_only_risk": validation_prefix_only_risk,
        "val_data_probe": val_stats,
        "blockers": blockers,
        "blocker_count": len(blockers),
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }
    result_path = result_dir / "validation_coverage_preflight_summary.json"
    write_receipt(result_path, summary)
    return summary


def run_training(spec: ModeSpec, result_dir: Path) -> dict[str, Any]:
    run_preflight(spec, result_dir)
    config_path = repo_absolute_path(spec.config_path)
    run_command(["python", "scripts/run_a100_300m_fineweb_edu_10step_training.py", "--config", config_path.as_posix()], cwd=REPO_DIR)
    config = load_json(config_path)
    output_dir = REPO_DIR / config["run"]["output_dir"]
    run_command(["python", "scripts/validate_a800_public16k_run_artifacts.py", "--output-dir", config["run"]["output_dir"]], cwd=REPO_DIR)

    required_files = [
        "summary.json",
        "summary.md",
        "metrics.jsonl",
        "validation_metrics.jsonl",
        "run_config.json",
        "run_metadata.json",
        "post_run_artifact_validation_summary.json",
    ]
    for filename in required_files:
        copy_required_file(output_dir / filename, result_dir / filename)

    if spec.result_package is None:
        return {"training_status": "success", "result_package": None}

    result_package = Path(spec.result_package)
    result_package.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(result_package, "w:gz") as archive:
        for filename in required_files:
            archive.add(output_dir / filename, arcname=filename)
    return {"training_status": "success", "result_package": result_package.as_posix()}


def run_modal_job_impl(mode: str, repo_url: str, ref: str) -> dict[str, Any]:
    if mode not in MODE_SPECS:
        raise ValueError(f"unsupported mode {mode}; expected one of {sorted(MODE_SPECS)}")

    spec = MODE_SPECS[mode]
    package_path = Path(spec.package_path)
    result_dir = Path(spec.result_dir)
    result_dir.mkdir(parents=True, exist_ok=True)

    if not package_path.exists():
        raise FileNotFoundError(f"missing prepared package in Modal Volume: {package_path}")

    repo_commit = clone_repo(repo_url, ref)
    if spec.extract_required_files_only:
        extracted_members = safe_extract_required_files(package_path, REPO_DIR, spec.required_package_files)
    else:
        extracted_members = safe_extract(package_path, REPO_DIR / spec.extract_dir)

    train_path = REPO_DIR / spec.train_path
    val_path = REPO_DIR / spec.val_path
    if spec.requires_train_split and not train_path.exists():
        raise FileNotFoundError(f"missing train split after extraction: {train_path}")
    if not val_path.exists():
        raise FileNotFoundError(f"missing val split after extraction: {val_path}")
    verified_package_files = verify_required_package_files(spec)

    if spec.validation_coverage_preflight:
        result = run_validation_coverage_preflight(spec, result_dir)
    elif spec.train:
        result = run_training(spec, result_dir)
    else:
        result = run_preflight(spec, result_dir)

    receipt = {
        "status": "success",
        "mode": mode,
        "gpu_requested": None if spec.cpu_only else DEFAULT_GPU,
        "cpu_only": spec.cpu_only,
        "volume_name": VOLUME_NAME,
        "repo_url": repo_url,
        "repo_ref": ref,
        "repo_commit": repo_commit,
        "required_commit": REQUIRED_COMMIT,
        "config_path": spec.config_path,
        "prepared_package": spec.package_path,
        "extracted_members": extracted_members,
        "verified_package_files": verified_package_files,
        "train_path_exists": train_path.exists(),
        "val_path_exists": val_path.exists(),
        "result_dir": spec.result_dir,
        "ran_training": spec.train,
        "produced_checkpoint": spec.train,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        **result,
    }
    write_receipt(result_dir / "modal_preflight_receipt.json", receipt)
    DATA_VOLUME.commit()
    return receipt


@app.function(image=IMAGE, gpu=DEFAULT_GPU, timeout=TIMEOUT_SECONDS, volumes={str(VOLUME_MOUNT_PATH): DATA_VOLUME})
def run_modal_job(mode: str = "preflight_2gb_1000", repo_url: str = REPO_URL, ref: str = "main") -> dict[str, Any]:
    return run_modal_job_impl(mode=mode, repo_url=repo_url, ref=ref)


@app.function(image=IMAGE, timeout=TIMEOUT_SECONDS, volumes={str(VOLUME_MOUNT_PATH): DATA_VOLUME})
def run_modal_cpu_job(mode: str = "preflight_5gb_validation_coverage", repo_url: str = REPO_URL, ref: str = "main") -> dict[str, Any]:
    return run_modal_job_impl(mode=mode, repo_url=repo_url, ref=ref)


@app.local_entrypoint()
def main(mode: str = "preflight_2gb_1000", repo_url: str = REPO_URL, ref: str = "main") -> None:
    if mode not in MODE_SPECS:
        raise ValueError(f"unsupported mode {mode}; expected one of {sorted(MODE_SPECS)}")
    spec = MODE_SPECS[mode]
    if spec.cpu_only:
        receipt = run_modal_cpu_job.remote(mode=mode, repo_url=repo_url, ref=ref)
    else:
        receipt = run_modal_job.remote(mode=mode, repo_url=repo_url, ref=ref)
    if spec.validation_coverage_preflight:
        write_local_validation_coverage_artifacts(receipt)
    print(json.dumps(receipt, ensure_ascii=False, indent=2))
