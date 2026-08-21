# Preflight Lote L0010 — Resumen

**Fecha:** 2026-08-19  
**Lote:** `lote-10-preflight`  
**Harness/modelo registrado:** MiMo/OpenCode — `opencode/mimo-v2.5-free`

## Resultado operativo

- Documentos procesados: **15/15**.
- Fuente seleccionada: **PDF con tramos** para los 15 documentos.
- OCR: **0** documentos.
- Revisión visual: **0** documentos.
- Bloqueos: **ninguno**.
- Cada documento conserva `tramos/preflight.json`, `tramos/manifest.json` y
  `PREPARACION_FUENTE.md`.

El único documento clasificado globalmente como `two_column` es `11362/48144`; su manifest selecciona
`pymupdf` y conserva el diagnóstico `two_column`. Los demás documentos quedaron como `single_column` o
`mixed`, por debajo del umbral de dos columnas.

## Observaciones de trazabilidad a subsanar

Reparadas el 2026-08-19:

1. Se reconstruyeron los 15 `preflight_endpoint.json` desde los `texto.txt` ya descargados. Todos devolvieron
   código `2`, documentando correctamente la decisión de pasar a PDF.
2. Se propagó el diagnóstico espacial PyMuPDF a los 15 `preflight.json` y `manifest.json`. El manifest declara
   además `layout_extraction_applied`, que es `true` exclusivamente para `11362/48144`; así no se confunde el
   diagnóstico de layout con la extracción que generó los tramos.

El lote queda con trazabilidad de preflight completa y conforme para iniciar el enriquecimiento.
