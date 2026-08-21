# Sub-lote L0001: posiciones 4 a 6

Inicia una sesión limpia de OpenCode desde `C:\Users\abustamante\Cepal-lab\experimentos\cambio_climatico\fase2` y pega el bloque siguiente.

---

## INICIO DEL PROMPT

Procesa exclusivamente estos tres documentos pendientes del lote `L0001`:

1. `https://hdl.handle.net/11362/37955` — *The effects of climate change in the coastal areas of Latin America and the Caribbean. Impacts* (`num_muestra: 6`).
2. `https://hdl.handle.net/11362/38120` — *Investigación científica en agricultura y cambio climático en América Latina y el Caribe* (`num_muestra: 7`).
3. `https://hdl.handle.net/11362/38274` — *La incertidumbre de los recursos hídricos y sus riesgos frente al cambio climático* (`num_muestra: 8`).

Esta es una preprueba analítica. No ejecutes `ledger.py`, no escribas en `fase2/corpus/resultados/` y no declares aprobación: la revisión y promoción canónica se harán después.

Lee antes de trabajar:

- `esquema_json_v1.md`
- `codebook_v0.md`
- `INTERPELACION_v0.md`
- `TIPOLOGIA_v0.md`
- `CASOS_ANCLA_INTERPELACION_v1.md`
- `OPERACION_BATCH.md`
- `ENTORNO_PDF.md`
- `corpus/lotes/L0001.json`

Para cada documento, en ese orden:

1. Descarga el PDF oficial y guárdalo como `corpus/pdfs/11362_<id>.pdf`. No uses el TXT de DSpace como fuente analítica si está truncado, es demasiado corto o falla la compuerta de calidad.
2. Crea `corpus/intermedios/11362/<id>/` y ejecuta:

```bash
python3 pipeline/preflight_pdf.py \
  corpus/pdfs/11362_<id>.pdf \
  corpus/intermedios/11362/<id>/tramos \
  --pages-per-chunk 25
```

3. Si el preflight termina con código `0`, usa exclusivamente su `tramos/manifest.json` y los tramos generados. Si termina con código `2`, crea primero `fuente_force_ocr.pdf` con:

```bash
ocrmypdf --force-ocr --deskew --language spa \
  corpus/pdfs/11362_<id>.pdf \
  corpus/intermedios/11362/<id>/fuente_force_ocr.pdf
```

Luego reejecuta el preflight sobre `fuente_force_ocr.pdf` hacia `tramos_force_ocr/`. Nunca uses `--skip-text` para una fuente con texto corrupto. Si el OCR tampoco es utilizable, no enriquezcas: escribe `PREPRUEBA_BLOQUEADA.md` con diagnóstico y continúa con el siguiente documento.
4. Si la fuente elegida es OCR, deja registrada una muestra visual pendiente de cinco páginas distribuidas antes de considerar el borrador apto para revisión humana. No inventes comprobación visual si el modelo no acepta imágenes.
5. Construye `corpus/intermedios/11362/<id>/borrador_preprueba.json` desde la fuente paginada seleccionada. Reconstruye metadatos, estructura, interpelación y tipología desde el contenido completo. Excluye portada, índice, bibliografía, anexos, créditos y listas editoriales.
6. Cada dimensión debe representar un hallazgo climático/ambiental distinto. No llenes por cuota, no desdobles variaciones de una misma idea y no uses una cita si presenta encabezado, URL, truncamiento, palabra evidentemente corrompida o falta de contexto. Las citas deben ser literales, autónomas y con página PDF verificable.
7. Ejecuta, guarda y corrige hasta obtener código `0` en esquema y citas:

```bash
python3 pipeline/validar_esquema.py \
  corpus/intermedios/11362/<id>/borrador_preprueba.json \
  > corpus/intermedios/11362/<id>/validacion_esquema.txt

python3 pipeline/validar_citas.py \
  corpus/intermedios/11362/<id>/borrador_preprueba.json \
  corpus/intermedios/11362/<id>/<DIRECTORIO_TRAMOS>/tramo_001_025.txt \
  --page-source corpus/intermedios/11362/<id>/<DIRECTORIO_TRAMOS>/manifest.json \
  --strict-quality \
  > corpus/intermedios/11362/<id>/validacion_citas.txt

python3 pipeline/auditar_densidad.py \
  corpus/intermedios/11362/<id>/borrador_preprueba.json \
  > corpus/intermedios/11362/<id>/auditoria_densidad.txt
```

Sustituye `<DIRECTORIO_TRAMOS>` por `tramos` o `tramos_force_ocr`, según la fuente que ganó el preflight. La densidad es una alerta de revisión, no una cuota.

Al finalizar, responde solo con una tabla de tres filas que indique: id, fuente elegida, ruta del borrador, dimensiones, resultado de esquema/citas/densidad y cualquier bloqueo. No modifiques otros documentos ni pidas confirmaciones intermedias.

## FIN DEL PROMPT
