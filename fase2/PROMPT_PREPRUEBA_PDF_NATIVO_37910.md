# Preprueba PDF nativo/OCR — 11362/37910

Pega el bloque entre **INICIO DEL PROMPT** y **FIN DEL PROMPT** en una sesión limpia del harness, iniciada desde la raíz del repositorio.

---

## INICIO DEL PROMPT

Procesa exclusivamente `https://hdl.handle.net/11362/37910`, **Financiamiento para el cambio climático en América Latina en 2013**. Esta es una preprueba: no toques `corpus/resultados/` ni ejecutes comandos de `ledger.py`.

El TXT de DSpace de este documento tiene fuentes codificadas ilegibles. No lo uses para interpretar, resumir ni citar. Lee el PDF nativamente o mediante OCR:

`fase2/corpus/pdfs/11362_37910.pdf`

Lee `fase2/esquema_json_v1.md`, `codebook_v0.md`, `INTERPELACION_v0.md`, `TIPOLOGIA_v0.md`, `CASOS_ANCLA_INTERPELACION_v1.md` y `OPERACION_BATCH.md` antes de comenzar.

## Extracción paginada obligatoria

1. Lee el índice del PDF y crea `fase2/corpus/intermedios/11362/37910/tramos_nativo/mapa_capitulos.json` con títulos y rangos de páginas **impresas** verificados visualmente. Excluye bibliografía, anexos y material editorial del análisis.
2. Crea bloques de 20 páginas en `tramos_nativo/`. Cada archivo debe contener texto nativo/OCR legible y los marcadores de cada página: `=== PÁGINA IMPRESA N ===`.
3. Crea `tramos_nativo/manifest.json` con `source_pdf`, `page_count`, `pages_per_chunk`, `quality: {"usable": true}` y la lista de bloques `{ "pages": "N-M", "path": "..." }`.
4. Si no puedes generar texto legible y paginado para todas las páginas sustantivas, escribe `fase2/corpus/intermedios/11362/37910/PREPRUEBA_BLOQUEADA.md` explicando el impedimento y detente. No generes JSON analítico.

## Borrador y controles

Solo si la extracción anterior es legible y paginada, construye:

`fase2/corpus/intermedios/11362/37910/borrador_preprueba_nativo.json`

Usa `num_muestra: 4`. El índice, metadatos, capítulos y citas deben salir de la lectura nativa/OCR y del registro del corpus; no se infieren desde el TXT ilegible. Toda cita debe ser una oración o cláusula autónoma, literal, sin encabezados, URLs, viñetas sueltas ni frases cortadas.

Ejecuta:

```bash
python3 fase2/pipeline/validar_esquema.py \
  fase2/corpus/intermedios/11362/37910/borrador_preprueba_nativo.json \
  > fase2/corpus/intermedios/11362/37910/validacion_esquema_nativo.txt

python3 fase2/pipeline/validar_citas.py \
  fase2/corpus/intermedios/11362/37910/borrador_preprueba_nativo.json \
  fase2/corpus/intermedios/11362/37910/tramos_nativo/tramo_001_020.txt \
  --page-source fase2/corpus/intermedios/11362/37910/tramos_nativo/manifest.json \
  --strict-quality \
  > fase2/corpus/intermedios/11362/37910/validacion_citas_nativo.txt

python3 fase2/pipeline/auditar_densidad.py \
  fase2/corpus/intermedios/11362/37910/borrador_preprueba_nativo.json \
  > fase2/corpus/intermedios/11362/37910/auditoria_densidad_nativo.txt
```

Corrige hasta que el esquema y las citas terminen con código 0. La auditoría de densidad es una alerta revisable, no un bloqueo por defecto.

Al finalizar, responde solo con: condición de extracción (nativa u OCR), rutas de mapa/tramos/borrador/reportes, conteo de dimensiones, resultado de validaciones y confirmación de que no tocaste ledger ni resultados canónicos.

## FIN DEL PROMPT
