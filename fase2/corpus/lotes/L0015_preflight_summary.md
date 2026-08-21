# Resumen de preflight — L0015

**Fecha de cierre:** 2026-08-20  
**Harness:** MiMo/OpenCode

## Resultado

- Documentos procesados: **16/16**.
- Fuente `pdf_tramos`: **15**, con extracción PyMuPDF layout-aware.
- Fuente `endpoint_apto`: **1** (`11362/48823`).
- Bloqueados: **0**.
- OCR forzado: **0**.
- Revisión visual requerida: **0**.

Los quince documentos con PDF conservan sus `preflight.json`, `manifest.json` y tramos en
`corpus/intermedios/11362/<id>/tramos/`. El documento `11362/48823` conserva el preflight y los
tramos del endpoint en `corpus/intermedios/11362/48823/tramos_endpoint/`.

El lote queda preparado exclusivamente para la fase posterior de enriquecimiento. La reserva del ledger
se conserva abierta; este preflight no modifica su estado ni escribe resultados analíticos.
