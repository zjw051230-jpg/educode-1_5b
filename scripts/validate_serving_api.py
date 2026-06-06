from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from educode.serving import FakeModelBackend, build_app, health_response, model_metadata_response
from educode.serving_schema import GenerateRequest


def main() -> int:
    backend = FakeModelBackend(model_name="educode-fake")
    response = backend.generate(GenerateRequest(prompt="def add(a, b):", max_new_tokens=4))
    app_info = build_app(backend)
    payload = {
        "validation_status": "passed",
        "health": health_response(),
        "metadata": model_metadata_response(backend),
        "generate_response": asdict(response),
        "fastapi_available": app_info["fastapi_available"],
        "server_started": False,
        "checkpoint_loaded": False,
        "modal_used": False,
        "gpu_used": False,
        "training_started": False,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
