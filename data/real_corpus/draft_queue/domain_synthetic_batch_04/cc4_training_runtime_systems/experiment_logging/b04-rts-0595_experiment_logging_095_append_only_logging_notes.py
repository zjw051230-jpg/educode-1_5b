# topic_id: B04-RTS-0595
# draft_status: candidate
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC-4
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only
# batch_id: domain_synthetic_batch_04

from statistics import mean


def build_experiment_logging_0595(rows):
    summary = {
        'topic_id': 'B04-RTS-0595',
        'focus': 'append-only logging notes',
        'row_count': len(rows),
        'status': 'empty' if not rows else 'ready',
    }
    if rows:
        summary['min_value'] = min(rows)
        summary['max_value'] = max(rows)
        summary['avg_value'] = round(mean(rows), 4)
    return summary


def check_experiment_logging_94(summary):
    flags = {
        'has_rows': summary['row_count'] > 0,
        'range_known': 'min_value' in summary and 'max_value' in summary,
        'focus_matches': summary['focus'] == 'append-only logging notes',
    }
    flags['review_ready'] = all(flags.values())
    return flags


sample_rows = [1.19, 1.44, 1.69, 1.94, 2.19]
summary = build_experiment_logging_0595(sample_rows)
flags = check_experiment_logging_94(summary)
print(summary)
print(flags)

# Teaching note:
# This example demonstrates append-only logging notes.
# It is a review helper for synthetic educational drafts.
# It does not launch training jobs or access external systems.
# The safest use is to inspect small derived summaries before writing conclusions.
# Separate helpers in this batch cover adjacent runtime questions.
# Keeping each file narrow makes later review and deduplication easier.
