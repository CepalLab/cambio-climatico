"""Genera thumbnails de la primera pagina de cada PDF local.

Uso: python3 scripts/make_covers.py  (desde visualizador/)
Sale a web/public/portadas/<num>.jpg (ancho 480px).
Los docs sin PDF usan card tipografica (fallback en el frontend).
"""
import os
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
PDFDIR = Path(os.environ.get("CEPAL_PDFS") or (REPO / "fase2/corpus/pdfs"))
OUT = ROOT / "web/public/portadas"
OUT.mkdir(parents=True, exist_ok=True)

hechas, errores = 0, []
for pdf in sorted(PDFDIR.glob("11362_*.pdf")):
    num = pdf.stem.split("_", 1)[1]
    dest = OUT / f"{num}.jpg"
    if dest.exists():
        hechas += 1
        continue
    try:
        with fitz.open(pdf) as doc:
            page = doc[0]
            pix = page.get_pixmap(matrix=fitz.Matrix(480 / page.rect.width,
                                                     480 / page.rect.width))
            pix.save(dest)
        hechas += 1
    except Exception as e:  # noqa: BLE001
        errores.append(f"{num}: {e}")

print(f"portadas: {hechas} ok, {len(errores)} errores")
for e in errores[:10]:
    print("ERR", e)
