# draft_status: candidate
# topic_id: B05-COD-0009
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC-6
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only
# batch_id: domain_synthetic_batch_05
# learning_objective: Compare train and validation counts instead of reporting one flat total.
# concrete_anchor: numeric toy example

"""Synthetic educational example with topic-specific behavior for batch_05."""

from __future__ import annotations

import json
from collections import Counter, defaultdict

TOPIC_ID = 'B05-COD-0009'
TITLE = 'Compare split-level category counts'

def sample_rows() -> list[dict[str, object]]:
    return [
        {'source_category': 'synthetic_examples', 'split': 'train', 'worker_id': 'CC-6', 'relative_path': 'a.md'},
        {'source_category': 'synthetic_examples', 'split': 'val', 'worker_id': 'CC-6', 'relative_path': 'b.md'},
        {'source_category': 'external_general_text', 'split': 'val', 'worker_id': 'CC-6', 'relative_path': 'c.md'},
    ]

def count_by_category(rows: list[dict[str, object]]) -> dict[str, int]:
    return dict(sorted(Counter(str(row['source_category']) for row in rows).items()))

def topic_action(rows: list[dict[str, object]]) -> object:
    grouped: defaultdict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        grouped[str(row['split'])][str(row['source_category'])] += 1
    return {split: dict(counter) for split, counter in sorted(grouped.items())}

def main() -> None:
    if 'sample_rows' in globals():
        payload = sample_rows()
    elif 'sample_checkpoint' in globals():
        payload = sample_checkpoint()
    elif 'sample_sequences' in globals():
        payload = sample_sequences()
    elif 'sample_config' in globals():
        payload = sample_config()
    else:
        payload = sample_text()
    output = {'topic_id': TOPIC_ID, 'title': TITLE, 'result': topic_action(payload)}
    print(json.dumps(output, ensure_ascii=False, sort_keys=True))
    assert output['topic_id'] == TOPIC_ID


if __name__ == '__main__':
    main()

# trace_note_57: keep the example concrete and tied to the named topic.
