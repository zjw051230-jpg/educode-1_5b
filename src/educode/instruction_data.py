from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

ALLOWED_ROLES = {"system", "user", "assistant"}


@dataclass(frozen=True)
class InstructionValidationResult:
    accepted: bool
    estimated_tokens: int
    issues: tuple[str, ...]

    @property
    def issue_count(self) -> int:
        return len(self.issues)


def estimate_token_count(text: str) -> int:
    pieces = re.findall(r"\w+|[^\w\s]", text, flags=re.UNICODE)
    return max(1, len(pieces)) if text else 0


def sample_text(sample: dict[str, object]) -> str:
    messages = sample.get("messages")
    if not isinstance(messages, list):
        return ""
    parts: list[str] = []
    for message in messages:
        if isinstance(message, dict):
            role = str(message.get("role", ""))
            content = str(message.get("content", ""))
            parts.append(f"{role}: {content}")
    return "\n".join(parts)


def validate_messages(messages: object) -> list[str]:
    issues: list[str] = []
    if not isinstance(messages, list) or not messages:
        return ["messages must be a non-empty list"]

    roles: list[str] = []
    for index, message in enumerate(messages):
        if not isinstance(message, dict):
            issues.append(f"message {index} must be an object")
            continue
        role = message.get("role")
        content = message.get("content")
        if role not in ALLOWED_ROLES:
            issues.append(f"message {index} has unsupported role")
        else:
            roles.append(str(role))
        if not isinstance(content, str) or not content.strip():
            issues.append(f"message {index} content must be non-empty text")

    if "user" not in roles:
        issues.append("at least one user turn is required")
    if "assistant" not in roles:
        issues.append("at least one assistant turn is required")
    if roles and roles[-1] != "assistant":
        issues.append("last message should be an assistant response")
    return issues


def validate_instruction_sample(
    sample: dict[str, object],
    *,
    max_estimated_tokens: int = 4096,
) -> InstructionValidationResult:
    issues: list[str] = []
    if not isinstance(sample.get("id"), str) or not str(sample.get("id")).strip():
        issues.append("id must be non-empty text")

    issues.extend(validate_messages(sample.get("messages")))
    estimated_tokens = estimate_token_count(sample_text(sample))
    if estimated_tokens > max_estimated_tokens:
        issues.append("estimated token count exceeds limit")

    return InstructionValidationResult(
        accepted=not issues,
        estimated_tokens=estimated_tokens,
        issues=tuple(issues),
    )


def chat_to_prompt_completion(sample: dict[str, object]) -> dict[str, str]:
    result = validate_instruction_sample(sample)
    if not result.accepted:
        raise ValueError("; ".join(result.issues))

    messages = sample["messages"]
    assert isinstance(messages, list)
    last_assistant_index = max(
        index for index, message in enumerate(messages) if isinstance(message, dict) and message.get("role") == "assistant"
    )
    prompt_messages = messages[:last_assistant_index]
    completion_message = messages[last_assistant_index]
    prompt = "\n".join(
        f"{message['role']}: {message['content']}"
        for message in prompt_messages
        if isinstance(message, dict)
    )
    return {"prompt": prompt, "completion": str(completion_message["content"])}


def iter_jsonl(path: Path) -> Iterable[dict[str, object]]:
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            payload = json.loads(line)
            if not isinstance(payload, dict):
                raise ValueError(f"line {line_number} must be a JSON object")
            yield payload


def load_jsonl_samples(path: Path, *, max_estimated_tokens: int = 4096) -> dict[str, object]:
    results: list[dict[str, object]] = []
    for sample in iter_jsonl(path):
        validation = validate_instruction_sample(sample, max_estimated_tokens=max_estimated_tokens)
        results.append(
            {
                "id": sample.get("id"),
                "accepted": validation.accepted,
                "estimated_tokens": validation.estimated_tokens,
                "issues": list(validation.issues),
            }
        )

    accepted_count = sum(1 for result in results if result["accepted"])
    return {
        "validation_status": "passed" if accepted_count == len(results) else "failed",
        "sample_count": len(results),
        "accepted_count": accepted_count,
        "rejected_count": len(results) - accepted_count,
        "results": results,
    }
