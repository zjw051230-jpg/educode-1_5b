# draft_status: candidate
# topic_id: B05-COD-0028
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC-6
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only
# batch_id: domain_synthetic_batch_05
# learning_objective: Catch step mismatches between checkpoint names and stored metadata.
# concrete_anchor: failure scenario

"""Synthetic educational example with topic-specific behavior for batch_05."""

from __future__ import annotations

import json
from collections import Counter, defaultdict

TOPIC_ID = 'B05-COD-0028'
TITLE = 'Compare filename step and metadata step'

def sample_checkpoint() -> dict[str, object]:
    return {'step': 2400, 'metadata': {'run_name': 'cc6-demo', 'best_val_loss': 1.87, 'tokenizer_hash': 'tok-a7', 'notes': 'resume after eval'}, 'config': {'seq_len': 128, 'tokenizer_hash': 'tok-a7'}, 'path': 'ckpt_2400.pt'}

def topic_action(payload: dict[str, object]) -> object:
    filename_step = int(str(payload['path']).split('_')[-1].split('.')[0])
    return {'filename_step': filename_step, 'metadata_step': int(payload['step']), 'match': filename_step == int(payload['step'])}

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

# trace_note_48: keep the example concrete and tied to the named topic.

# trace_note_50: keep the example concrete and tied to the named topic.

# trace_note_52: keep the example concrete and tied to the named topic.

# trace_note_54: keep the example concrete and tied to the named topic.

# trace_note_56: keep the example concrete and tied to the named topic.
