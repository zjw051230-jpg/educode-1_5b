from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime


@dataclass
class CheckpointMetadata:
    run_id: str
    step: int
    stage: str
    notes: str
    created_at: str


def build_checkpoint_metadata(run_id: str, step: int) -> dict[str, str | int]:
    metadata = CheckpointMetadata(
        run_id=run_id,
        step=step,
        stage="windows_cuda",
        notes="project-authored synthetic educational example",
        created_at=datetime.now().isoformat(timespec="seconds"),
    )
    return asdict(metadata)


def main() -> None:
    print(build_checkpoint_metadata("demo_run", step=100))


if __name__ == "__main__":
    main()
