import importlib.util
import sys
import unittest
from pathlib import Path


path = Path(__file__).resolve().parents[1] / "layout_extraction.py"
spec = importlib.util.spec_from_file_location("layout_extraction", path)
layout_extraction = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = layout_extraction
spec.loader.exec_module(layout_extraction)


class FakePage:
    class Rect:
        width = 600
        height = 800

    rect = Rect()

    def __init__(self, blocks):
        self._blocks = blocks

    def get_text(self, mode):
        assert mode == "blocks"
        return [(*block, 0, 0) for block in self._blocks]


def block(x0, y0, x1, y1, text):
    # PyMuPDF: x0, y0, x1, y1, text, block_no, block_type.
    return (x0, y0, x1, y1, text, 0, 0)


class LayoutExtractionTest(unittest.TestCase):
    def test_reads_left_column_before_right_column(self):
        page = FakePage(
            [
                block(40, 150, 280, 180, "Izquierda uno"),
                block(320, 150, 560, 180, "Derecha uno"),
                block(40, 210, 280, 240, "Izquierda dos"),
                block(320, 210, 560, 240, "Derecha dos"),
            ]
        )
        text, metadata = layout_extraction.extract_page_layout_aware(page)
        self.assertEqual(
            "Izquierda uno\n\nIzquierda dos\n\nDerecha uno\n\nDerecha dos",
            text,
        )
        self.assertEqual("two_column", metadata["layout"])

    def test_preserves_full_width_block_between_column_sections(self):
        page = FakePage(
            [
                block(40, 150, 280, 180, "Izquierda arriba"),
                block(320, 150, 560, 180, "Derecha arriba"),
                block(30, 250, 570, 280, "Tabla o banner"),
                block(40, 320, 280, 350, "Izquierda abajo"),
                block(320, 320, 560, 350, "Derecha abajo"),
            ]
        )
        text, _ = layout_extraction.extract_page_layout_aware(page)
        self.assertEqual(
            "Izquierda arriba\n\nDerecha arriba\n\nTabla o banner\n\nIzquierda abajo\n\nDerecha abajo",
            text,
        )

    def test_single_column_remains_top_to_bottom(self):
        page = FakePage(
            [
                block(40, 150, 560, 180, "Primer párrafo"),
                block(40, 210, 560, 240, "Segundo párrafo"),
            ]
        )
        text, metadata = layout_extraction.extract_page_layout_aware(page)
        self.assertEqual("Primer párrafo\n\nSegundo párrafo", text)
        self.assertEqual("single_column", metadata["layout"])


if __name__ == "__main__":
    unittest.main()
