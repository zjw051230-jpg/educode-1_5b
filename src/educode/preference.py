from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class PreferencePair:
    prompt: str
    chosen: str
    rejected: str
    source: str = "synthetic"

    def __post_init__(self) -> None:
        for field_name in ("prompt", "chosen", "rejected"):
            if not getattr(self, field_name).strip():
                raise ValueError(f"{field_name} must be non-empty")
        if self.chosen == self.rejected:
            raise ValueError("chosen and rejected responses must differ")

    def to_dict(self) -> dict:
        return asdict(self)


def validate_preference_pair(pair: PreferencePair) -> dict:
    return {
        "status": "valid",
        "prompt_chars": len(pair.prompt),
        "chosen_chars": len(pair.chosen),
        "rejected_chars": len(pair.rejected),
        "source": pair.source,
    }
