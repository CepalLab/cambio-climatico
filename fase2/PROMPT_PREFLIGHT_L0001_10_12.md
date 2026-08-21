# Preflight económico — L0001, posiciones 10 a 12

Inicia una sesión limpia de Codex desde `C:\Users\abustamante\Cepal-lab\experimentos\cambio_climatico\fase2` y pega el bloque siguiente.

---

## INICIO DEL PROMPT

Realiza exclusivamente la preparación determinista de fuentes para estos tres documentos pendientes de `L0001`:

1. `11362/39135` — *Emisiones de gases de efecto invernadero y mitigación en el sector de uso del suelo, cambio en el uso del suelo y silvicultura: economía del cambio climático en la Argentina* (`num_muestra: 12`).
2. `11362/39140` — *Impactos y vulnerabilidad al cambio climático de los principales ríos de Mendoza y San Juan a partir de la evolución de los glaciares cordilleranos: economía del cambio climático en la Argentina* (`num_muestra: 13`).
3. `11362/39149` — *Cambio Climático en Centroamérica: impactos potenciales y opciones de política pública* (`num_muestra: 14`).

No realices enriquecimiento, no construyas JSON analíticos, no ejecutes `ledger.py` y no escribas en `corpus/resultados/`.

Para cada handle: resuelve la fuente con `pipeline/cepal_repositorio.py`, descarga primero `TEXT` como `corpus/intermedios/11362/<id>/texto.txt` y ejecuta `pipeline/preflight_endpoint_text.py` con `--report` y `--output-dir .../tramos_endpoint --pages-per-chunk 25`.

Si el endpoint es apto y conserva saltos de página, selecciona `endpoint_apto`; no descargues PDF ni ejecutes OCR. Si falla, descarga el PDF, corre `preflight_pdf.py`; si devuelve `2`, aplica `ocrmypdf --force-ocr --deskew --language spa` y repite el preflight sobre el PDF OCR. Nunca uses `--skip-text` con una capa corrupta.

Escribe `PREPARACION_FUENTE.md` por documento con fuente seleccionada, métricas, rutas, necesidad de muestra visual y bloqueos. Al finalizar responde solo con una tabla de tres filas: id, fuente seleccionada, manifest/ruta y necesidad de revisión visual.

## FIN DEL PROMPT
