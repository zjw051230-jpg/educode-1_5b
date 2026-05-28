from __future__ import annotations

import tarfile
import tempfile
import unittest
import sys
import types
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

modal_stub = types.SimpleNamespace(
    App=lambda _name: types.SimpleNamespace(function=lambda **_kwargs: (lambda func: func), local_entrypoint=lambda: (lambda func: func)),
    Volume=types.SimpleNamespace(from_name=lambda *_args, **_kwargs: types.SimpleNamespace(commit=lambda: None)),
    Image=types.SimpleNamespace(
        debian_slim=lambda **_kwargs: types.SimpleNamespace(
            apt_install=lambda *_args: types.SimpleNamespace(
                pip_install=lambda *_packages: object(),
            ),
        ),
    ),
)
sys.modules.setdefault("modal", modal_stub)

from scripts.modal_a100_streaming_runner import discover_required_package_members


class ModalA100StreamingRunnerPackageDiscoveryTests(unittest.TestCase):
    def test_discovers_validation_preflight_members_under_rootless_package(self) -> None:
        required_files = (
            "data/public_corpus/fineweb_edu_sample10bt_5gb/manifest.json",
            "data/public_corpus/fineweb_edu_sample10bt_5gb/validation_summary.json",
            "data/public_corpus/fineweb_edu_sample10bt_5gb/intake_validation_summary.json",
            "data/public_corpus/fineweb_edu_sample10bt_5gb/splits/fineweb_edu_5gb.val.jsonl",
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            package_path = Path(temp_dir) / "prepared.tar.gz"
            source_dir = Path(temp_dir) / "source"
            for relative_path in (
                "manifest.json",
                "validation_summary.json",
                "intake_validation_summary.json",
                "splits/fineweb_edu_5gb.val.jsonl",
            ):
                path = source_dir / relative_path
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("{}\n", encoding="utf-8")

            with tarfile.open(package_path, "w:gz") as archive:
                for path in sorted(source_dir.rglob("*")):
                    if path.is_file():
                        archive.add(path, arcname=path.relative_to(source_dir).as_posix())

            discovered = discover_required_package_members(package_path, required_files)

        self.assertEqual(
            discovered,
            {
                "data/public_corpus/fineweb_edu_sample10bt_5gb/manifest.json": "manifest.json",
                "data/public_corpus/fineweb_edu_sample10bt_5gb/validation_summary.json": "validation_summary.json",
                "data/public_corpus/fineweb_edu_sample10bt_5gb/intake_validation_summary.json": "intake_validation_summary.json",
                "data/public_corpus/fineweb_edu_sample10bt_5gb/splits/fineweb_edu_5gb.val.jsonl": "splits/fineweb_edu_5gb.val.jsonl",
            },
        )


if __name__ == "__main__":
    unittest.main()
