# Paginación PDF — L0002

Desde `...\cambio_climatico\fase2`, procesa solo `39855`, `40297` y `40299`. Sus TXT son aptos pero no tienen saltos de página. No hagas enriquecimiento ni ledger.

Para cada uno, descarga el PDF oficial como `corpus/pdfs/11362_<id>.pdf`, ejecuta `pipeline/preflight_pdf.py` hacia `corpus/intermedios/11362/<id>/tramos --pages-per-chunk 25`; si retorna 2, usa OCR forzada (`ocrmypdf --force-ocr --deskew --language spa`) y repite hacia `tramos_force_ocr/`. Escribe/actualiza `PREPARACION_FUENTE.md` y responde solo con id, fuente paginada y necesidad de revisión visual.
