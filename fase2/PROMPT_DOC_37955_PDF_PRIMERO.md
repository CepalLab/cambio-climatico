# Documento 37955: PDF primero

Inicia una sesión limpia de OpenCode desde `C:\Users\abustamante\Cepal-lab\experimentos\cambio_climatico\fase2` y pega el bloque siguiente.

---

## INICIO DEL PROMPT

Procesa exclusivamente `https://hdl.handle.net/11362/37955`, *The effects of climate change in the coastal areas of Latin America and the Caribbean. Impacts* (`num_muestra: 6`). Es una preprueba analítica: no ejecutes `ledger.py`, no escribas en `corpus/resultados/` y no declares aprobación.

Lee `esquema_json_v1.md`, `codebook_v0.md`, `INTERPELACION_v0.md`, `TIPOLOGIA_v0.md`, `CASOS_ANCLA_INTERPELACION_v1.md`, `OPERACION_BATCH.md` y `ENTORNO_PDF.md`.

Descarga el PDF oficial como `corpus/pdfs/11362_37955.pdf`. Crea `corpus/intermedios/11362/37955/` y ejecuta `preflight_pdf.py` con bloques de 25 páginas hacia `tramos/`. Si devuelve `2`, crea `fuente_force_ocr.pdf` usando `ocrmypdf --force-ocr --deskew --language spa`, y reejecuta el preflight hacia `tramos_force_ocr/`. Nunca uses `--skip-text` ante una capa de texto corrupta. Si tampoco resulta utilizable, escribe `PREPRUEBA_BLOQUEADA.md` y detente.

Construye `corpus/intermedios/11362/37955/borrador_preprueba.json` desde la fuente paginada válida. Excluye portada, índice, bibliografía, anexos, créditos y listas editoriales. Las dimensiones deben ser hallazgos distintos y las citas, literales, completas, autónomas y con página PDF verificable. No llenes por cuota ni conserves citas con truncamientos, URLs, encabezados o errores OCR evidentes.

Ejecuta y guarda en el mismo directorio `validar_esquema.py`, `validar_citas.py --strict-quality` con el `--page-source` del manifest elegido, y `auditar_densidad.py`. Corrige hasta que esquema y citas terminen con código `0`. Si usaste OCR, informa si queda pendiente una muestra visual; no inventes revisión visual.

Al finalizar responde solo con fuente seleccionada, rutas del borrador y reportes, cantidad de dimensiones y resultados de validación. No modifiques otros documentos ni pidas confirmaciones intermedias.

## FIN DEL PROMPT
