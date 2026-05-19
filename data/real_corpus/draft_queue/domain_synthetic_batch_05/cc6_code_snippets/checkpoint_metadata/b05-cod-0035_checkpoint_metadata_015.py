# draft_status: candidate
# topic_id: B05-COD-0035
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC-6
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only
# batch_id: domain_synthetic_batch_05
# learning_objective: Create a readable inspection summary for checkpoint metadata.
# concrete_anchor: numeric toy example

"""Synthetic educational example with topic-specific behavior for batch_05."""

from __future__ import annotations

import json
from collections import Counter, defaultdict

TOPIC_ID = 'B05-COD-0035'
TITLE = 'Summarize metadata fields for human inspection'

def sample_checkpoint() -> dict[str, object]:
    return {'step': 2400, 'metadata': {'run_name': 'cc6-demo', 'best_val_loss': 1.87, 'tokenizer_hash': 'tok-a7', 'notes': 'resume after eval'}, 'config': {'seq_len': 128, 'tokenizer_hash': 'tok-a7'}, 'path': 'ckpt_2400.pt'}

def topic_action(payload: dict[str, object]) -> object:
    return [fstep={payload['step']}, frun={payload['metadata']['run_name']}, floss={payload['metadata']['best_val_loss']}]

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

# trace_note_47: keep the example concrete and tied to the named topic.

# trace_note_49: keep the example concrete and tied to the named topic.

# trace_note_51: keep the example concrete and tied to the named topic.

# trace_note_53: keep the example concrete and tied to the named topic.

# trace_note_55: keep the example concrete and tied to the named topic.

# trace_note_57: keep the example concrete and tied to the named topic.
