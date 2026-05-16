# draft_status: candidate
# topic_id: BIL-019
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC5
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only

from typing import Iterable, List


LEAKY_PREFIXES = ["Answer:", "Response:", "A:", "EN:"]


def find_suspicious_prefixes(lines: Iterable[str]) -> List[str]:
    hits: List[str] = []
    for line in lines:
        stripped = line.strip()
        for prefix in LEAKY_PREFIXES:
            if stripped.startswith(prefix):
                hits.append(stripped)
                break
    return hits


if __name__ == "__main__":
    demo_lines = [
        "请用中文解释 tokenizer。",
        "Answer: tokenizer 用来把文本切成 token。",
        "EN: Keep the term tokenizer unchanged.",
    ]
    for hit in find_suspicious_prefixes(demo_lines):
        print(hit)

# Educational notes:
# - This snippet does not prove leakage; it only flags prefixes that deserve human review.
# - Prefix checks are useful when bilingual drafts mix template labels from two languages.
# - The strings here are synthetic examples for draft triage.
