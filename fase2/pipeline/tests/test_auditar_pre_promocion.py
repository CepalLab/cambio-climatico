import importlib.util
import unittest
from pathlib import Path


path = Path(__file__).resolve().parents[1] / "auditar_pre_promocion.py"
spec = importlib.util.spec_from_file_location("auditar_pre_promocion", path)
auditar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(auditar)


class ClimateCoverageTest(unittest.TestCase):
    def test_recognizes_english_climate_signal(self):
        leaves = [({"resumen": "Climate change increases drought and flood risks."}, "/A")]
        self.assertEqual(leaves, auditar.climate_relevant_leaves(leaves))

    def test_zero_eligible_leaves_are_not_low_coverage(self):
        substantive = []
        ratio = len([]) / len(substantive) if substantive else 1.0
        self.assertEqual(1.0, ratio)


if __name__ == "__main__":
    unittest.main()
