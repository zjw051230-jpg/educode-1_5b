# draft_status: candidate
# topic_id: B05-COD-0079
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC-6
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only
# batch_id: domain_synthetic_batch_05
# learning_objective: Summarize validation errors by config section.
# concrete_anchor: metrics interpretation

"""Synthetic educational example with topic-specific behavior for batch_05."""

from __future__ import annotations

import json
from collections import Counter, defaultdict

TOPIC_ID = 'B05-COD-0079'
TITLE = 'Summarize validation errors by section'

def sample_config() -> dict[str, object]:
    return {'training': {'micro_batch_size': 0, 'precision': 'half16', 'eval_interval': 75, 'save_interval': 200, 'seq_len': 128}, 'checkpoint': {'seq_len': 256}, 'paths': {'tokenizer_path': '', 'resume_path': ''}, 'resume': {'enabled': True}, 'optimizer': {'lr': 0.0, 'weight_decay': -0.1}, 'logging': {'metrics_path': '', 'write_every': 10}, 'flags': {'resume': 'TRUE', 'compile': 'false'}}

def topic_action(config: dict[str, object]) -> object:
    grouped = {'training': [], 'logging': []}
    if int(config['training']['micro_batch_size']) <= 0:
        grouped['training'].append('micro_batch_size must be positive')
    if not config['logging']['metrics_path']:
        grouped['logging'].append('metrics_path missing')
    return grouped

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

# trace_note_52: keep the example concrete and tied to the named topic.

# trace_note_54: keep the example concrete and tied to the named topic.

# trace_note_56: keep the example concrete and tied to the named topic.
