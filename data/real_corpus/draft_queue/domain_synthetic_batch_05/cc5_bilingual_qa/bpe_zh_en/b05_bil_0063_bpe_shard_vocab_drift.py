# draft_status: candidate
# topic_id: B05-BIL-0063
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC-5
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only
# batch_id: domain_synthetic_batch_05

"""BPE Merge Rules and Vocabulary Growth 63: Shard Vocab Drift

ZH: 用最小 merge scorer 观察 bilingual 技术词的排序变化。
EN: Use a tiny merge scorer to inspect ranking shifts for bilingual technical units.
"""

from dataclasses import dataclass


@dataclass
class PairStat:
    left: str
    right: str
    count: int

    @property
    def pair(self) -> str:
        return f"{self.left}+{self.right}"


def score(stat: PairStat, literal_bonus: dict[str, int], punctuation_penalty: int) -> int:
    joined = stat.left + stat.right
    bonus = literal_bonus.get(joined, 0)
    penalty = punctuation_penalty if any(ch in stat.right for ch in ',./=-') else 0
    return stat.count + bonus - penalty


def rank_pairs(stats: list[PairStat]) -> None:
    literal_bonus = {'A100': 2, 'fp16': 2, 'KVcache': 1}
    ranked = sorted(
        ((score(stat, literal_bonus, 1), stat) for stat in stats),
        key=lambda item: (-item[0], -item[1].count, item[1].pair),
    )
    for total, stat in ranked:
        print(f"{stat.pair:14} count={stat.count} score={total}")


def main() -> None:
    stats = [
        PairStat('A', '100', 4),
        PairStat('吞', '吐', 5),
        PairStat('lr', '=', 3),
        PairStat('token', 'budget', 4),
    ]
    print('focus', 'Shard Vocab Drift')
    print('writing_form', 'mini lab')
    print('concrete_anchor', 'failure scenario')
    rank_pairs(stats)


if __name__ == '__main__':
    main()
