# draft_status: candidate
# topic_id: B05-BIL-0077
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC-5
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only
# batch_id: domain_synthetic_batch_05

"""Concept Contrasts and Evaluation Caution 77: Safe Translation Versus Helpful Translation

ZH: 用最小规则检查双语样本是否保留同一教学对比。
EN: Use tiny rules to check whether a bilingual pair preserves the same teaching contrast.
"""

from dataclasses import dataclass


@dataclass
class PairReview:
    zh: str
    en: str
    anchor: str


def anchor_preserved(review: PairReview) -> bool:
    return review.anchor.lower() in review.en.lower() or review.anchor in review.zh


def has_claim_escalation(review: PairReview) -> bool:
    strong_phrases = ['proves', 'works well', 'fully reliable', 'is robust']
    cautious_phrases = ['不代表', '不是', '局部', '边界']
    return any(p in review.en.lower() for p in strong_phrases) and any(p in review.zh for p in cautious_phrases)


def score(review: PairReview) -> dict[str, object]:
    return {
        'anchor_preserved': anchor_preserved(review),
        'claim_escalation': has_claim_escalation(review),
        'safe_pair': anchor_preserved(review) and not has_claim_escalation(review),
    }


def main() -> None:
    pair = PairReview(
        zh='checkpoint 可恢复，不代表泛化稳定。',
        en='This checkpoint proves the model is robust.',
        anchor='checkpoint',
    )
    print('focus', 'Safe Translation Versus Helpful Translation')
    print('writing_form', 'mini lab')
    print('concrete_anchor', 'numeric toy example')
    print(score(pair))


if __name__ == '__main__':
    main()
