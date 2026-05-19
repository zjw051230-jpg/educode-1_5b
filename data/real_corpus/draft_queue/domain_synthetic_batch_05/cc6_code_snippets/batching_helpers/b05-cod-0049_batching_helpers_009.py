# draft_status: candidate
# topic_id: B05-COD-0049
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC-6
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only
# batch_id: domain_synthetic_batch_05
# learning_objective: Show how tail handling changes the final batch list.
# concrete_anchor: decision checklist

"""Synthetic educational example with topic-specific behavior for batch_05."""

from __future__ import annotations

import json
from collections import Counter, defaultdict

TOPIC_ID = 'B05-COD-0049'
TITLE = 'Keep or drop a tail batch'

def sample_sequences() -> list[list[int]]:
    return [[1, 2, 3, 4, 5], [6, 7, 8], [9, 10], [11, 12, 13, 14]]

def topic_action(samples: list[list[int]]) -> object:
    batch_size = 3
    batches = [samples[i:i + batch_size] for i in range(0, len(samples), batch_size)]
    return {'keep_tail': batches, 'drop_tail': batches[:-1] if len(batches[-1]) < batch_size else batches}

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

# trace_note_49: keep the example concrete and tied to the named topic.

# trace_note_51: keep the example concrete and tied to the named topic.

# trace_note_53: keep the example concrete and tied to the named topic.

# trace_note_55: keep the example concrete and tied to the named topic.

# trace_note_57: keep the example concrete and tied to the named topic.
