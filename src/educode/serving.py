from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from educode.serving_schema import GenerateRequest, GenerateResponse, validate_generate_request


@dataclass(frozen=True)
class FakeModelBackend:
    model_name: str
    checkpoint_loaded: bool = False

    def generate(self, request: GenerateRequest | dict[str, object]) -> GenerateResponse:
        validated = validate_generate_request(request)
        suffix = " ".join(["<fake>"] * validated.max_new_tokens)
        text = f"{validated.prompt} {suffix}".strip()
        return GenerateResponse(
            text=text,
            model_name=self.model_name,
            tokens_generated=validated.max_new_tokens,
            checkpoint_loaded=self.checkpoint_loaded,
        )


def health_response() -> dict[str, object]:
    return {"status": "ok", "checkpoint_loaded": False, "gpu_required": False}


def model_metadata_response(backend: FakeModelBackend) -> dict[str, object]:
    return {
        "model_name": backend.model_name,
        "backend": "fake",
        "checkpoint_loaded": backend.checkpoint_loaded,
        "serving_mode": "local_skeleton",
    }


def build_app(backend: FakeModelBackend) -> dict[str, Any]:
    try:
        from fastapi import FastAPI
    except Exception:
        return {"fastapi_available": False, "app": None, "backend": backend.model_name}

    app = FastAPI(title="EduCode Serving Skeleton")

    @app.get("/health")
    def health() -> dict[str, object]:
        return health_response()

    @app.get("/metadata")
    def metadata() -> dict[str, object]:
        return model_metadata_response(backend)

    @app.post("/generate")
    def generate(payload: dict[str, object]) -> dict[str, object]:
        return asdict(backend.generate(payload))

    return {"fastapi_available": True, "app": app, "backend": backend.model_name}
