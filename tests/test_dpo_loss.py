import sys
import unittest
from pathlib import Path

import torch

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.educode.dpo import dpo_loss  # noqa: E402
from src.educode.preference import PreferencePair, validate_preference_pair  # noqa: E402


class DPOLossTests(unittest.TestCase):
    def test_dpo_loss_is_finite_for_synthetic_logprobs(self):
        policy_chosen = torch.tensor([-1.0, -0.8])
        policy_rejected = torch.tensor([-2.0, -1.5])
        ref_chosen = torch.tensor([-1.2, -1.0])
        ref_rejected = torch.tensor([-1.8, -1.4])

        loss = dpo_loss(policy_chosen, policy_rejected, ref_chosen, ref_rejected, beta=0.1)

        self.assertEqual(loss.shape, ())
        self.assertTrue(torch.isfinite(loss))

    def test_bad_beta_and_shape_rejected(self):
        with self.assertRaises(ValueError):
            dpo_loss(torch.ones(1), torch.ones(1), torch.ones(1), torch.ones(1), beta=0)
        with self.assertRaises(ValueError):
            dpo_loss(torch.ones(2), torch.ones(1), torch.ones(2), torch.ones(2), beta=0.1)

    def test_preference_pair_validation(self):
        pair = PreferencePair(prompt="Explain SDPA", chosen="Good answer", rejected="Bad answer")

        self.assertEqual(validate_preference_pair(pair)["status"], "valid")
        with self.assertRaises(ValueError):
            PreferencePair(prompt="x", chosen="", rejected="bad")


if __name__ == "__main__":
    unittest.main()
