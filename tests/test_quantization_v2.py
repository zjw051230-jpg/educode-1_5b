import sys
import unittest
from pathlib import Path

import torch

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.educode.quantization import (  # noqa: E402
    QuantizationConfig,
    fake_dequantize_tensor,
    fake_quantize_tensor,
    qlora_readiness,
)


class QuantizationV2Tests(unittest.TestCase):
    def test_bad_quant_config_rejected(self):
        with self.assertRaises(ValueError):
            QuantizationConfig(bits=3, quant_type="nf4")
        with self.assertRaises(ValueError):
            QuantizationConfig(bits=4, quant_type="int8")

    def test_qlora_without_quant_rejected(self):
        with self.assertRaises(ValueError):
            QuantizationConfig(bits=4, quant_type="nf4", qlora_enabled=True, quantization_enabled=False)
        with self.assertRaises(ValueError):
            QuantizationConfig(bits=4, quant_type="nf4", qlora_enabled=True, experimental_ack=False)

    def test_fake_quant_dequant_finite(self):
        x = torch.tensor([-1.0, -0.2, 0.0, 0.4, 1.0])
        q = fake_quantize_tensor(x, bits=4)
        y = fake_dequantize_tensor(q)

        self.assertTrue(torch.isfinite(y).all())
        self.assertEqual(y.shape, x.shape)

    def test_readiness_is_local_only(self):
        report = qlora_readiness(
            QuantizationConfig(bits=4, quant_type="nf4", qlora_enabled=True, experimental_ack=True)
        )

        self.assertFalse(report["modal_gpu_training_run"])
        self.assertIn(report["readiness_status"], {"ready_with_caveats", "unavailable"})


if __name__ == "__main__":
    unittest.main()
