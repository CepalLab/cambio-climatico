# Preflight económico — L0001, posiciones 7 a 9

Inicia una sesión limpia de OpenCode desde `C:\Users\abustamante\Cepal-lab\experimentos\cambio_climatico\fase2` y pega el bloque siguiente.

---

## INICIO DEL PROMPT

Realiza exclusivamente la preparación determinista de fuentes para estos tres documentos pendientes de `L0001`:

1. `11362/38985` — *Sostenibilidad ambiental y competitividad internacional: la huella de carbono de las exportaciones de alimentos* (`num_muestra: 9`).
2. `11362/39009` — *Evaluación de los impactos del cambio climático sobre la salud: economía del cambio climático en la Argentina* (`num_muestra: 10`).
3. `11362/39089` — *The Economics of Climate Change in Central America: Summary 2012* (`num_muestra: 11`).

No realices enriquecimiento, no leas analíticamente los documentos, no construyas JSON, no ejecutes `ledger.py` y no escribas en `corpus/resultados/`. El objetivo es elegir y dejar preparada la fuente más confiable al menor costo antes de abrir una sesión analítica independiente por documento.

Para cada handle:

1. Resuélvelo mediante `pipeline/cepal_repositorio.py` y descarga primero el bitstream `TEXT` como `corpus/intermedios/11362/<id>/texto.txt`.
2. Ejecuta `pipeline/preflight_endpoint_text.py`, guarda `preflight_endpoint.json` y, cuando el TXT sea apto y tenga saltos de página, genera `tramos_endpoint/manifest.json` con bloques de 25 páginas.
3. Si el TXT es apto y tiene tramos endpoint, registra `endpoint_apto` y no generes OCR ni descargues el PDF: el manifest endpoint será la fuente paginada para validar citas. Si es apto pero no conserva saltos de página, descarga el PDF después para paginar/validar las citas.
4. Si el TXT no es apto, descarga el PDF oficial como `corpus/pdfs/11362_<id>.pdf` y ejecuta `pipeline/preflight_pdf.py` con bloques de 25 páginas hacia `corpus/intermedios/11362/<id>/tramos`.
5. Si el preflight del PDF devuelve `2`, crea `fuente_force_ocr.pdf` con `ocrmypdf --force-ocr --deskew --language spa` y repite el preflight hacia `tramos_force_ocr/`. Nunca uses `--skip-text` cuando la capa existente sea corrupta.
6. Escribe `PREPARACION_FUENTE.md` por documento: handle, fuente seleccionada, rutas, métricas del preflight, necesidad de muestra visual y cualquier bloqueo. No simules revisión visual.

Al finalizar responde solo con una tabla de tres filas: id, fuente seleccionada (`endpoint_apto`, `pdf_tramos`, `ocr_forzada` o `bloqueado`), rutas y necesidad de revisión visual. No continúes al enriquecimiento.

## FIN DEL PROMPT
