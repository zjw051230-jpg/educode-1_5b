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
REQUIRED_COMMIT = "66b00b9"
DEFAULT_GPU = "A100-40GB"
TIMEOUT_SECONDS = 2 * 60 * 60

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


def run_preflight(spec: ModeSpec, result_dir: Path) -> dict[str, Any]:
    run_command(["python", "scripts/inspect_training_batch_memory_plan.py", "--config", spec.config_path], cwd=REPO_DIR)
    run_command(
        ["python", "scripts/run_a100_300m_fineweb_edu_10step_training.py", "--config", spec.config_path, "--dry-run"],
        cwd=REPO_DIR,
    )
    run_command(["python", "scripts/check_a100_execution_readiness.py", "--config", spec.config_path], cwd=REPO_DIR)

    config = load_json(REPO_DIR / spec.config_path)
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


def run_training(spec: ModeSpec, result_dir: Path) -> dict[str, Any]:
    run_preflight(spec, result_dir)
    run_command(["python", "scripts/run_a100_300m_fineweb_edu_10step_training.py", "--config", spec.config_path], cwd=REPO_DIR)
    config = load_json(REPO_DIR / spec.config_path)
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


@app.function(image=IMAGE, gpu=DEFAULT_GPU, timeout=TIMEOUT_SECONDS, volumes={str(VOLUME_MOUNT_PATH): DATA_VOLUME})
def run_modal_job(mode: str = "preflight_2gb_1000", repo_url: str = REPO_URL, ref: str = "main") -> dict[str, Any]:
    if mode not in MODE_SPECS:
        raise ValueError(f"unsupported mode {mode}; expected one of {sorted(MODE_SPECS)}")

    spec = MODE_SPECS[mode]
    package_path = Path(spec.package_path)
    result_dir = Path(spec.result_dir)
    result_dir.mkdir(parents=True, exist_ok=True)

    if not package_path.exists():
        raise FileNotFoundError(f"missing prepared package in Modal Volume: {package_path}")

    repo_commit = clone_repo(repo_url, ref)
    extracted_members = safe_extract(package_path, REPO_DIR / spec.extract_dir)

    train_path = REPO_DIR / spec.train_path
    val_path = REPO_DIR / spec.val_path
    if not train_path.exists():
        raise FileNotFoundError(f"missing train split after extraction: {train_path}")
    if not val_path.exists():
        raise FileNotFoundError(f"missing val split after extraction: {val_path}")

    if spec.train:
        result = run_training(spec, result_dir)
    else:
        result = run_preflight(spec, result_dir)

    receipt = {
        "status": "success",
        "mode": mode,
        "gpu_requested": DEFAULT_GPU,
        "volume_name": VOLUME_NAME,
        "repo_url": repo_url,
        "repo_ref": ref,
        "repo_commit": repo_commit,
        "required_commit": REQUIRED_COMMIT,
        "config_path": spec.config_path,
        "prepared_package": spec.package_path,
        "extracted_members": extracted_members,
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


@app.local_entrypoint()
def main(mode: str = "preflight_2gb_1000", repo_url: str = REPO_URL, ref: str = "main") -> None:
    receipt = run_modal_job.remote(mode=mode, repo_url=repo_url, ref=ref)
    print(json.dumps(receipt, ensure_ascii=False, indent=2))
