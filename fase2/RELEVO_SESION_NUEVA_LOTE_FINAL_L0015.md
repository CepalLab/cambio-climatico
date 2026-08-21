# Relevo — sesión nueva para el lote final L0015

**Corte:** 2026-08-20  
**Estado del corpus:** 213 aprobados, 16 pendientes y 15 documentos L0014 en cola.  
**Ledger:** L0013 está cerrado; L0014 sigue abierto y en enriquecimiento.

## Qué está terminado

- L0013 fue promovido y aprobado: 15 resultados canónicos y 15 certificados SHA-256 válidos.
- El preflight de L0014 está completo: 15/15 documentos con `pdf_tramos`, sin bloqueos, OCR forzado ni
  revisión visual requerida. Sus artefactos están en `corpus/intermedios/11362/<id>/`.
- El pipeline mantiene extracción espacial PyMuPDF para todo documento que detecte al menos una página
  `two_column`, incluso si el layout general es `mixed`.

## Estado de L0014

L0014 continúa en enriquecimiento. Su estado `queued` en el ledger es esperado porque esa ejecución no
registró intentos allí. No modificar sus borradores, tramos, matrices, resultados ni reserva de lote.
Cuando termine, aplicar revisión dimensión–cita, certificación y promoción como en L0013.

## Misión de la sesión nueva

Reservar exclusivamente el lote final con los 16 documentos pendientes; es compatible con que L0014 siga
en proceso:

```bash
cd C:\Users\abustamante\Cepal-lab\experimentos\cambio_climatico\fase2
python3 pipeline/ledger.py status --json
python3 pipeline/ledger.py next-batch --size 16 --name lote-15-preflight
```

El comando debe crear `corpus/lotes/L0015.json`. Si el ledger informa una cantidad distinta de 16 pendientes,
detenerse y documentar la diferencia: no ajustar el tamaño ni usar L0014 como cola.

Después, crear `PROMPT_PREFLIGHT_L0015_MIMO.md` desde `PROMPT_PREFLIGHT_L0014_MIMO.md`, cambiando únicamente
el código de lote y la ruta de manifiesto. La misión MiMo debe ser solo de preflight: no enriquecer, no
ejecutar `ledger.py`, no escribir en `corpus/resultados/` y registrar el modelo/harness real o `no registrado`.

Para cada documento, conservar `preflight_endpoint.json` cuando corresponda y, para la fuente elegida,
`preflight.json`, `manifest.json`, `PREPARACION_FUENTE.md`, `layout`, `layout_extraction_applied` y extractor.
Si se detecta cualquier página `two_column`, conservar la extracción espacial PyMuPDF del pipeline.

## Referencias obligatorias

- `ESTADO_OPERATIVO_ACTUAL.md`
- `CIERRE_L0013.md`
- `PROMPT_PREFLIGHT_L0014_MIMO.md`
- `PROMPT_ENRIQUECIMIENTO_UNIDAD.md`
- `PROMPT_REVISION_DIMENSIONES_CITAS.md`
- `ENTORNO_PDF.md`
- `pipeline/ledger.py`
