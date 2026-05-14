from pathlib import Path
import json


def read_jsonl(path: str) -> list[dict]:
    records: list[dict] = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        records.append(json.loads(line))
    return records


if __name__ == "__main__":
    sample_path = "data/sample.jsonl"
    print("This is a teaching example for JSONL reading.")
    print(f"Example path: {sample_path}")
    print("A real intake script would validate fields and summarize counts.")
