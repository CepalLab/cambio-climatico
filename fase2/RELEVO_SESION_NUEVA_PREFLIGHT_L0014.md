# Relevo — sesión nueva para preflight L0014

**Corte:** 2026-08-20  
**Estado del corpus:** 198 aprobados, 31 pendientes y 15 documentos de L0013 en cola.  
**Ledger:** L0012 está cerrado; L0013 está abierto.

## Qué está terminado

- L0011 y L0012 fueron promovidos, certificados y cerrados.
- L0013 tiene preflight materializado para sus 15 documentos: fuente, tramos y manifest de páginas.
  El ledger mantiene sus documentos como `queued` porque el preflight determinista no ejecuta `ledger.py`.
- El pipeline incorpora desde este punto extracción espacial PyMuPDF si existe cualquier página de dos
  columnas, incluidos documentos `mixed`.
- Las citas estrictas rechazan ahora rótulos editoriales, metadatos de tablas, listas no proposicionales y
  reutilización exacta de una misma cita entre dimensiones.
- La cobertura climática reconoce inglés y trata 0/0 como no aplicable.

## Qué sigue en L0013

L0013 está en enriquecimiento. Mantener la separación entre preflight, borrador, validaciones, revisión
semántica y promoción. Antes de certificar los documentos de riesgo, usar
`PROMPT_REVISION_DIMENSIONES_CITAS.md` y pasar la matriz resultante mediante `--review-matrix` a
`certificar_promocion.py`.

Los documentos L0013 de 80 o más páginas son `81149`, `80595`, `81035`, `81101` y `80987`; deben usar
índice primero, bloques contiguos y consolidación robusta. Los grupos por extensión ya definidos son:

- Grupo 1: 80695, 81194, 80769, 81084, 80952.
- Grupo 2: 80762, 80955, 80746, 81051, 80737.
- Grupo 3: 81149, 80595, 81035, 81101, 80987.

## Misión de la sesión nueva

No usar L0013 como cola ni modificar sus artefactos. Crear y procesar solo el preflight de L0014:

```bash
cd C:\Users\abustamante\Cepal-lab\experimentos\cambio_climatico\fase2
python3 pipeline/ledger.py status --json
python3 pipeline/ledger.py next-batch --size 15 --name lote-14-preflight
```

Luego preparar `PROMPT_PREFLIGHT_L0014_MIMO.md` a partir de la plantilla L0013, actualizando únicamente el
código de lote y el manifiesto. La misión MiMo debe ser solo de preflight: no enriquecer, no ejecutar
`ledger.py`, no escribir en `corpus/resultados/` y registrar el modelo real o `no registrado`.

Al revisar el manifest L0014, verificar que cada fuente seleccionada conserve `layout`,
`layout_extraction_applied` y el extractor. La regla vigente es preferir PyMuPDF layout-aware si se detecta
al menos una página `two_column`, no solo cuando el documento completo supera 50%.

## Referencias obligatorias

- `ESTADO_OPERATIVO_ACTUAL.md`
- `PROMPT_PREFLIGHT_L0013_MIMO.md`
- `PROMPT_ENRIQUECIMIENTO_UNIDAD.md`
- `PROMPT_REVISION_DIMENSIONES_CITAS.md`
- `ENTORNO_PDF.md`
- `pipeline/ledger.py`
