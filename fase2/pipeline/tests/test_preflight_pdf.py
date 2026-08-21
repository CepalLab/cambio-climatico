import importlib.util
import sys
import unittest
from pathlib import Path


pipeline_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(pipeline_dir))
path = pipeline_dir / "preflight_pdf.py"
spec = importlib.util.spec_from_file_location("preflight_pdf", path)
preflight_pdf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preflight_pdf)


class PreflightPdfTraceabilityTest(unittest.TestCase):
    def test_preserves_pymupdf_diagnostic_when_another_extractor_wins(self):
        candidates = [
            {"extractor": "pypdf", "quality": {"usable": True}},
            {
                "extractor": "pymupdf",
                "quality": {"usable": True},
                "layout": {"layout": "mixed", "method": "pymupdf_text_blocks_spatial_order"},
            },
        ]
        self.assertEqual(
            {"layout": "mixed", "method": "pymupdf_text_blocks_spatial_order"},
            preflight_pdf.pymupdf_layout_diagnostic(candidates),
        )

    def test_uses_unknown_only_without_pymupdf_diagnostic(self):
        self.assertEqual("unknown", preflight_pdf.pymupdf_layout_diagnostic([])["layout"])


if __name__ == "__main__":
    unittest.main()
