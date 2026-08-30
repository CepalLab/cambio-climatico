"""Agrega numeración al PDF de revisión sin alterar el contenido aprobado."""

from pathlib import Path

import pymupdf as fitz


ANALISIS_DIR = Path(__file__).resolve().parents[1]
CIRCULATION_DIR = ANALISIS_DIR / "circulacion"
INPUT = CIRCULATION_DIR / "Borrador_revision_CEPAL_Cambio_Climatico_2015_2026_sin_paginar.pdf"
OUTPUT = CIRCULATION_DIR / "Borrador_revision_CEPAL_Cambio_Climatico_2015_2026.pdf"


def main() -> None:
    document = fitz.open(INPUT)
    for page_index, page in enumerate(document):
        if page_index == 0:
            continue
        footer_line_y = page.rect.height - 36
        footer_number_y = page.rect.height - 17
        page.draw_line(
            fitz.Point(52, footer_line_y),
            fitz.Point(page.rect.width - 52, footer_line_y),
            color=(0.72, 0.78, 0.78),
            width=0.5,
        )
        page_number = str(page_index)
        text_width = fitz.get_text_length(page_number, fontname="helv", fontsize=8)
        page.insert_text(
            fitz.Point((page.rect.width - text_width) / 2, footer_number_y),
            page_number,
            fontname="helv",
            fontsize=8,
            color=(0.09, 0.42, 0.45),
        )
    if OUTPUT.exists():
        OUTPUT.unlink()
    document.save(OUTPUT, garbage=4, deflate=True)
    document.close()
    print(OUTPUT.as_posix())


if __name__ == "__main__":
    main()