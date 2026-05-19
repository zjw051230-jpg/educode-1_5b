# draft_status: candidate
# topic_id: B04-BIL-0418
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC-5
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only
# batch_id: domain_synthetic_batch_04

"""Debugging Tensor Shapes and Data Issues 18: Unexpected Nan

ZH: 遇到 NaN 时先看输入还是梯度。
EN: whether to inspect inputs or gradients first when NaNs appear.
"""

from typing import Dict, List

def build_demo_rows() -> List[Dict[str, object]]:
    """Create tiny synthetic bilingual diagnostics rows for draft review."""
    return [
        {
            "topic_id": "B04-BIL-0418",
            "group_theme": "Debugging Tensor Shapes and Data Issues",
            "variant": "unexpected nan",
            "question_zh": "为什么这个模式值得检查？",
            "question_en": "Why is this pattern worth checking?",
            "signal": "draft_review_only",
        },
        {
            "topic_id": "B04-BIL-0418",
            "question_zh": "如果只看表面流畅度会漏掉什么？",
            "question_en": "What do we miss if we inspect fluency only?",
            "signal": "boundary_and_alignment",
        },
    ]

def summarize_rows(rows: List[Dict[str, object]]) -> Dict[str, object]:
    return {
        "row_count": len(rows),
        "has_chinese": any("question_zh" in row for row in rows),
        "has_english": any("question_en" in row for row in rows),
        "signals": [row.get("signal") for row in rows],
    }

if __name__ == "__main__":
    rows = build_demo_rows()
    print(rows)
    print(summarize_rows(rows))

# 教学说明 / Educational notes:
# - 这个 Python 片段围绕 unexpected nan 构造最小双语检查样例。
# - This Python snippet builds a tiny bilingual inspection example around unexpected nan.
# - 它不访问网络、不读写真实用户数据，也不运行训练。
# - It does not touch networks, real user data, or training execution.
# - 第 18 个局部样例强调 reviewer 应先看结构，再看表面措辞。
# - Reviewers should inspect structure before judging surface wording.
