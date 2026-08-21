# Estado operativo actual - Fase 2

**Corte:** 2026-08-21

## Estado del corpus

- Corpus total: 244 publicaciones.
- Aprobadas y promovidas: 244.
- Pendientes sin reservar: 0.
- En cola: 0 documentos.
- Último lote cerrado: `L0015` (`lote-15-preflight`), 16/16 documentos aprobados.
- No hay lotes activos. L0015 fue promovido con 16 certificados gemelos válidos (15 fuentes
  `pdf_tramos` y 1 `endpoint_apto`).

Los JSON aprobados viven en `corpus/resultados/`. El estado vivo se consulta siempre en el ledger:

```bash
python3 fase2/pipeline/ledger.py status --json
```

## Relevo para una sesión nueva

1. Consultar el ledger; no usar manifiestos históricos como cola viva.
2. No hay enriquecimientos pendientes en el corpus actual; ante una ampliación, consultar primero el ledger
   y reservar un nuevo lote desde la cola viva.
3. Generar `indice_fuente.json` desde `tramos/` antes de construir cada borrador.
4. Para documentos extensos, separar por bloques contiguos y consolidar después de que los parciales estén listos.
5. Ejecutar y guardar esquema, orden JSON, índice, citas con `--page-source tramos --strict-quality`, densidad y
   `auditar_pre_promocion.py`; en documentos de más de 80 páginas, usar `--strict-coverage`.
6. Generar `validacion_final.json` con `certificar_promocion.py`. Tras revisión humana OK, copiar atómicamente
   el borrador y su certificado gemelo `doc_<id>.validation.json` a `corpus/resultados/` y sincronizar el ledger.

## Criterio para documentos extensos

- Hasta aproximadamente 70–80 páginas de cuerpo: corrida unitaria, si la fuente y el contexto lo permiten.
- Más de 80 páginas: índice primero, parciales por bloques contiguos y consolidación posterior.
- Más de 130 páginas o documento técnico complejo: consolidación y corrección final con un modelo más robusto.
- Revisar especialmente títulos de nivel 2+, jerarquía, orden, omisiones de subsecciones y páginas de citas.

## Compuertas vigentes

- `validar_indice.py` bloquea títulos recortados, reformulados, omitidos o fuera de orden.
- `validar_esquema.py` bloquea retrocesos de páginas entre secciones hermanas.
- `validar_orden_json.py` bloquea reordenamientos de claves dentro de los bloques canónicos.
- `validar_citas.py` debe ejecutarse con diagnóstico UTF-8 completo y `--strict-quality`.
- `preflight_pdf.py` detecta layouts `two_column` mediante bloques PyMuPDF; si existe cualquier página de dos columnas, selecciona la extracción layout-aware y registra el diagnóstico en `preflight.json` y `manifest.json`.
- `preparar_tramos_pdf.py` usa el mismo extractor espacial; nunca enriquecer desde una fuente lineal que pueda entrelazar columnas.

## Cierre L0010

Los 15 documentos de L0010 fueron promovidos y aprobados tras revalidación. Cada resultado canónico conserva
un certificado gemelo con hashes SHA-256 del JSON, índice y fuente paginada. Se corrigieron la autoría de
`11362/47883`, la jerarquía de `11362/47903` y la trazabilidad/certificación de `11362/47855` y `11362/48166`.
La alerta de densidad de `11362/47883` (93 dimensiones en 86 páginas) fue revisada; se eliminó una única cita
duplicada y se aceptó conservar el resto por la exhaustividad analítica del documento.

## Cierre L0009

Los 15 documentos de L0009 fueron promovidos tras auditoría independiente y certificados con hashes del JSON,
índice y fuente. `11362/47604` se reparó antes de promoción (38/38 citas). Desde L0010 se bloquean títulos
no canónicos, certificados desactualizados y cobertura insuficiente mediante las nuevas compuertas.

## Cierre L0008

Los 15 documentos de L0008 fueron promovidos tras correcciones y revisión final. Todos pasaron esquema, índice,
orden JSON y citas estrictas; se verificaron 881/881 citas. Se aceptó y documentó la alerta de densidad residual
de 11362/45966 (0,76 dimensiones por página) después de reducir sus dimensiones de 292 a 116. 11362/46499
conservó revisión visual focalizada para las páginas 201–225.

El ledger registra L0008 como `completed`, con 138 documentos aprobados y 106 pendientes.

## Cierre L0007 (histórico)

Los 15 documentos de L0007 fueron promovidos tras revisión humana. Todos pasaron esquema, índice, orden JSON,
citas estrictas y auditoría de densidad; se verificaron 482/482 citas.

Durante el lote se identificó el riesgo de extracción entrelazada en documentos de dos columnas. El pipeline fue
fortalecido con `pipeline/layout_extraction.py`: detección espacial mediante bloques PyMuPDF, selección
layout-aware cuando más del 50% de las páginas son de dos columnas y trazabilidad del layout en `preflight.json`
y `manifest.json`. L0007 no se reprocesó porque sus documentos ya habían sido reparados.

## Siguiente misión

Mientras L0014 termina su enriquecimiento, una sesión nueva puede iniciar el enriquecimiento de L0015
usando sus fuentes preflight validadas y conservando la separación entre ambos lotes.

## Protocolo de cierre y relevo

Antes de cerrar cualquier sesión de procesamiento:

1. Ejecutar `python3 fase2/pipeline/ledger.py status --json` y confirmar que el ledger refleja los estados reales.
2. Ejecutar `python3 fase2/pipeline/ledger.py export` para dejar una salida legible del estado.
3. Confirmar por documento la separación entre preflight, borrador, validaciones, revisión humana y promoción.
4. Confirmar que cada documento conserve fuente, manifest, `indice_fuente.json`, bitácora de ejecución y reportes.
5. Actualizar este archivo con fecha de corte, último lote, aprobados, pendientes, bloqueados, incidencias y siguiente comando.
6. Si el lote terminó, crear o actualizar `CIERRE_LXXXX.md` con documentos, método, modelo/harness, validaciones,
   decisiones humanas, alertas aceptadas y cualquier corrección de pipeline.
7. Si se detectó un issue estructural, documentarlo en `ENTORNO_PDF.md` u `OPERACION_BATCH.md` y anotar aquí
   qué cambió y desde qué lote aplica.
8. Revisar `git status --short` para identificar archivos nuevos o modificados que deban conservarse en el relevo.

El relevo debe dejar claro qué está terminado, qué está solamente en preprueba, qué requiere revisión humana,
qué puede retomarse y cuál es el primer comando de la próxima sesión. No declarar una sesión cerrada basándose
solo en la existencia de archivos: ledger, artefactos y documentación deben contar la misma historia.

## Referencias

- Flujo operativo: `OPERACION_BATCH.md`
- Entorno PDF/OCR y columnas: `ENTORNO_PDF.md`
- Prompt estándar: `PROMPT_ENRIQUECIMIENTO_UNIDAD.md`
- Documentos extensos y A/B: `PROTOCOLO_LARGOS_Y_AB_v1.md`
- Estado y trazabilidad: `pipeline/ledger.py`, `EJECUCION_ENRIQUECIMIENTO.md`
