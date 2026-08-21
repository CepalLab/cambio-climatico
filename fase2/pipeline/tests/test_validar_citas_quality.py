import importlib.util
import sys
import unittest
from pathlib import Path


path = Path(__file__).resolve().parents[1] / "validar_citas.py"
spec = importlib.util.spec_from_file_location("validar_citas", path)
validar_citas = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = validar_citas
spec.loader.exec_module(validar_citas)


class CitationQualityTest(unittest.TestCase):
    def test_rejects_table_and_figure_labels(self):
        self.assertIsNotNone(validar_citas.citation_quality("Table 7 Investment needs by sector"))
        self.assertIsNotNone(validar_citas.citation_quality("Figura 3. Emisiones regionales"))

    def test_rejects_meta_sentence_about_table_sources(self):
        quote = "The sources of information for the amounts in table 7 are briefly presented below."
        self.assertIsNotNone(validar_citas.citation_quality(quote))

    def test_keeps_complete_body_statement(self):
        quote = "Annual investment will have to increase by between 0.2% and 1.0% of regional GDP."
        self.assertIsNone(validar_citas.citation_quality(quote))


if __name__ == "__main__":
    unittest.main()
