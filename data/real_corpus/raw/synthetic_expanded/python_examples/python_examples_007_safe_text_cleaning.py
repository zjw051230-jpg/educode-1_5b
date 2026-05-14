from __future__ import annotations


def normalize_text(raw_text: str) -> str:
    cleaned_lines: list[str] = []
    for line in raw_text.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        cleaned_lines.append(line.rstrip())
    cleaned_text = "\n".join(cleaned_lines).strip()
    return cleaned_text


def is_meaningful_text(text: str) -> bool:
    return bool(text and text.strip())


def main() -> None:
    sample = "  line one  \r\nline two\r\n\r\n"
    cleaned = normalize_text(sample)
    print(cleaned)
    print(is_meaningful_text(cleaned))


if __name__ == "__main__":
    main()
