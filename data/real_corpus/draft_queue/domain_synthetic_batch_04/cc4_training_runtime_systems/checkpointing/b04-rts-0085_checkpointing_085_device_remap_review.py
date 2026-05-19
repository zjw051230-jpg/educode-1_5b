# topic_id: B04-RTS-0085
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


def build_checkpointing_0085(rows):
    summary = {
        'topic_id': 'B04-RTS-0085',
        'focus': 'device remap review',
        'row_count': len(rows),
        'status': 'empty' if not rows else 'ready',
    }
    if rows:
        summary['min_value'] = min(rows)
        summary['max_value'] = max(rows)
        summary['avg_value'] = round(mean(rows), 4)
    return summary


def check_checkpointing_84(summary):
    flags = {
        'has_rows': summary['row_count'] > 0,
        'range_known': 'min_value' in summary and 'max_value' in summary,
        'focus_matches': summary['focus'] == 'device remap review',
    }
    flags['review_ready'] = all(flags.values())
    return flags


sample_rows = [1.09, 1.34, 1.59, 1.84, 2.09]
summary = build_checkpointing_0085(sample_rows)
flags = check_checkpointing_84(summary)
print(summary)
print(flags)

# Teaching note:
# This example demonstrates device remap review.
# It is a review helper for synthetic educational drafts.
# It does not launch training jobs or access external systems.
# The safest use is to inspect small derived summaries before writing conclusions.
# Separate helpers in this batch cover adjacent runtime questions.
# Keeping each file narrow makes later review and deduplication easier.
