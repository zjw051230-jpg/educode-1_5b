# draft_status: candidate
# topic_id: B05-BIL-0012
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC-5
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only
# batch_id: domain_synthetic_batch_05

"""Tokenizer Boundaries and Mixed Scripts 12: Unit Suffix Spacing

ZH: 用一个最小探针检查 mixed-script literal 的边界变化。
EN: Use a tiny probe to inspect boundary shifts around mixed-script literals.
"""

from dataclasses import dataclass


@dataclass
class Segment:
    text: str
    kind: str


def classify(ch: str) -> str:
    if "\u4e00" <= ch <= "\u9fff":
        return "cjk"
    if ch.isdigit():
        return "digit"
    if ch.isalpha():
        return "ascii"
    if ch.isspace():
        return "space"
    return "punct"


def segment(text: str) -> list[Segment]:
    pieces: list[Segment] = []
    for ch in text:
        kind = classify(ch)
        if not pieces or pieces[-1].kind != kind:
            pieces.append(Segment(ch, kind))
        else:
            pieces[-1].text += ch
    return [piece for piece in pieces if piece.kind != "space"]


def show_trace(label: str, text: str) -> None:
    parts = segment(text)
    joined = " ".join(f"[{p.text}:{p.kind}]" for p in parts)
    print(label, joined)


def literal_breaks(parts: list[Segment], literal: str) -> bool:
    merged = "".join(p.text for p in parts)
    if literal not in merged:
        return True
    return len([p for p in parts if literal.startswith(p.text) or p.text in literal]) > 1 and literal not in [p.text for p in parts]


def main() -> None:
    sample_a = "请保持fp16和A100 profiler一致"
    sample_b = "请保持 fp16 和 A100 profiler 一致"
    literal = "fp16"

    parts_a = segment(sample_a)
    parts_b = segment(sample_b)

    show_trace("A", sample_a)
    show_trace("B", sample_b)
    print("literal", literal)
    print("A_breaks_literal", literal_breaks(parts_a, literal))
    print("B_breaks_literal", literal_breaks(parts_b, literal))
    print("focus", 'Unit Suffix Spacing')
    print("writing_form", 'explainer note')
    print("concrete_anchor", 'mini code trace')


if __name__ == "__main__":
    main()
