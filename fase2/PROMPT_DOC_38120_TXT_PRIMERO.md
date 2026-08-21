# Documento 38120: endpoint TXT primero

Inicia una sesión limpia de OpenCode desde `C:\Users\abustamante\Cepal-lab\experimentos\cambio_climatico\fase2` y pega el bloque siguiente.

---

## INICIO DEL PROMPT

Procesa exclusivamente `https://hdl.handle.net/11362/38120`, *Investigación científica en agricultura y cambio climático en América Latina y el Caribe* (`num_muestra: 7`). Es una preprueba analítica: no ejecutes `ledger.py`, no escribas en `corpus/resultados/` y no declares aprobación.

Lee `esquema_json_v1.md`, `codebook_v0.md`, `INTERPELACION_v0.md`, `TIPOLOGIA_v0.md`, `CASOS_ANCLA_INTERPELACION_v1.md`, `OPERACION_BATCH.md` y `ENTORNO_PDF.md`.

1. Resuelve el handle con `pipeline/cepal_repositorio.py`, descarga primero el bitstream `TEXT` como `corpus/intermedios/11362/38120/texto.txt` y ejecuta:

```bash
python3 pipeline/preflight_endpoint_text.py \
  corpus/intermedios/11362/38120/texto.txt \
  --report corpus/intermedios/11362/38120/preflight_endpoint.json
```

2. Si devuelve `0`, usa el TXT como fuente de lectura económica. Si posee marcadores de página verificables, úsalo también como fuente de citas; si no, descarga el PDF oficial para verificar página y literal de cada cita. Si devuelve `2`, conserva el reporte, descarta el TXT para el enriquecimiento y sigue el flujo PDF.
3. En el flujo PDF descarga `corpus/pdfs/11362_38120.pdf` y ejecuta `preflight_pdf.py` con bloques de 25 páginas hacia `corpus/intermedios/11362/38120/tramos`. Si devuelve `2`, usa `ocrmypdf --force-ocr --deskew --language spa` y repite el preflight sobre `fuente_force_ocr.pdf` hacia `tramos_force_ocr/`. Nunca uses `--skip-text` ante una capa corrupta.
4. Construye `corpus/intermedios/11362/38120/borrador_preprueba.json` desde la fuente válida. Excluye portada, índice, bibliografía, anexos, créditos y listas editoriales. Las dimensiones deben ser hallazgos distintos, no una cuota. Las citas deben ser literales, completas, autónomas y con página PDF verificable; descarta citas con truncamientos, URLs, encabezados o errores OCR evidentes.
5. Ejecuta `validar_esquema.py`, `validar_citas.py --strict-quality` y `auditar_densidad.py`; guarda los tres reportes en el mismo directorio y corrige hasta que esquema y citas terminen con código `0`. Para las citas, usa `texto.txt --pdf corpus/pdfs/11362_38120.pdf` si el endpoint fue apto; usa el primer tramo y `--page-source` del manifest si la fuente seleccionada fue PDF u OCR. Si la fuente es OCR, marca explícitamente si queda pendiente una muestra visual; no inventes revisión visual.

Al finalizar responde solo con: fuente seleccionada, resultado de `preflight_endpoint`, rutas del borrador y reportes, cantidad de dimensiones y resultado de validaciones. No modifiques otros documentos ni pidas confirmaciones intermedias.

## FIN DEL PROMPT
