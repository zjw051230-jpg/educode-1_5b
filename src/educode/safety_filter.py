from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

ALLOWED_SEVERITIES = {"low", "medium", "high"}


@dataclass(frozen=True)
class SafetyPattern:
    name: str
    pattern: str
    severity: str = "medium"
    description: str = ""

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("pattern name is required")
        if self.severity not in ALLOWED_SEVERITIES:
            raise ValueError(f"unsupported severity: {self.severity}")
        try:
            re.compile(self.pattern, flags=re.IGNORECASE)
        except re.error as exc:
            raise ValueError(f"invalid safety regex: {self.name}") from exc


@dataclass(frozen=True)
class SafetyMatch:
    pattern_name: str
    severity: str
    matched_text: str


@dataclass(frozen=True)
class SafetyResult:
    safe: bool
    matches: list[SafetyMatch]


def validate_patterns(patterns: Iterable[SafetyPattern]) -> list[SafetyPattern]:
    pattern_list = list(patterns)
    if not pattern_list:
        raise ValueError("at least one safety pattern is required")
    names = [pattern.name for pattern in pattern_list]
    if len(set(names)) != len(names):
        raise ValueError("safety pattern names must be unique")
    return pattern_list


class SafetyFilter:
    def __init__(self, patterns: Iterable[SafetyPattern]) -> None:
        self.patterns = validate_patterns(patterns)
        self._compiled = [
            (pattern, re.compile(pattern.pattern, flags=re.IGNORECASE))
            for pattern in self.patterns
        ]

    def check_text(self, text: str) -> SafetyResult:
        matches: list[SafetyMatch] = []
        for pattern, compiled in self._compiled:
            for match in compiled.finditer(text):
                matches.append(
                    SafetyMatch(
                        pattern_name=pattern.name,
                        severity=pattern.severity,
                        matched_text=match.group(0),
                    )
                )
        return SafetyResult(safe=not matches, matches=matches)


def build_filter_report(safety_filter: SafetyFilter, texts: Iterable[str]) -> dict[str, object]:
    results = [safety_filter.check_text(text) for text in texts]
    unsafe_count = sum(1 for result in results if not result.safe)
    return {
        "text_count": len(results),
        "safe_count": len(results) - unsafe_count,
        "unsafe_count": unsafe_count,
        "match_count": sum(len(result.matches) for result in results),
        "external_api_used": False,
        "model_used": False,
    }
