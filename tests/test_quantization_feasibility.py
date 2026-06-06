import sys
import unittest
from pathlib import Path

import torch

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.educode.quantization import (  # noqa: E402
    QuantizationConfig,
    check_bitsandbytes_available,
    fake_quantize_tensor,
    qlora_readiness,
)


class QuantizationFeasibilityTests(unittest.TestCase):
    def test_bad_quant_config_rejected(self):
        with self.assertRaises(ValueError):
            QuantizationConfig(bits=3, quant_type="nf4")
        with self.assertRaises(ValueError):
            QuantizationConfig(bits=4, quant_type="int8")

    def test_bitsandbytes_check_is_graceful(self):
        result = check_bitsandbytes_available()

        self.assertIn("available", result)
        self.assertIn("status", result)

    def test_fake_quant_helper_returns_finite_tensor(self):
        tensor = torch.tensor([-1.0, -0.25, 0.0, 0.25, 1.0])

        quantized = fake_quantize_tensor(tensor, bits=4)

        self.assertEqual(quantized.shape, tensor.shape)
        self.assertTrue(torch.isfinite(quantized).all())

    def test_qlora_readiness_reports_local_only_gate(self):
        report = qlora_readiness(QuantizationConfig(bits=4, quant_type="nf4"))

        self.assertFalse(report["modal_gpu_training_run"])
        self.assertEqual(report["requested_bits"], 4)
        self.assertIn(report["readiness_status"], {"ready_with_caveats", "unavailable"})


if __name__ == "__main__":
    unittest.main()
