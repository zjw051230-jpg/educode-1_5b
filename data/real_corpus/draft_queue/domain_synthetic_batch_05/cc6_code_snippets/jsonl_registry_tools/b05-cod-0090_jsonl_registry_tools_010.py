# draft_status: candidate
# topic_id: B05-COD-0090
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC-6
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only
# batch_id: domain_synthetic_batch_05
# learning_objective: Detect duplicate topic identifiers.
# concrete_anchor: failure scenario

"""Synthetic educational example with topic-specific behavior for batch_05."""

from __future__ import annotations

import json
from collections import Counter, defaultdict

TOPIC_ID = 'B05-COD-0090'
TITLE = 'Detect duplicate topic ids'

def sample_text() -> str:
    rows = [
        {'topic_id': 'B05-COD-0081', 'file_type': 'Markdown', 'subdirectory': 'jsonl_registry_tools', 'title': ''},
        {'topic_id': 'B05-COD-0082', 'file_type': 'PY', 'subdirectory': 'jsonl_registry_tools', 'title': 'ok'},
    ]
    return '
'.join(json.dumps(row) for row in rows)

def parse_rows(text: str) -> list[dict[str, object]]:
    parsed = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        row = json.loads(line)
        row['_line_number'] = line_number
        parsed.append(row)
    return parsed

def topic_action(text: str) -> object:
    counts = Counter(row['topic_id'] for row in parse_rows(text) + [{'topic_id': 'B05-COD-0081'}])
    return sorted(topic for topic, count in counts.items() if count > 1)

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
