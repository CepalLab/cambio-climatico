# Relevo hacia Fase 3 — limpieza, revisión transversal y análisis agregados

**Corte:** 2026-08-24  
**Estado de Fase 2:** cerrado. El ledger registra 244/244 publicaciones aprobadas; no quedan lotes activos.

## Congelamiento de entrada

La fuente canónica de Fase 3 es `corpus/resultados/json/`. El inventario documental base permanece en
`../documentos_definitivos_trazabilidad.csv`. Los certificados disponibles están en
`corpus/resultados/certificados/`; los resultados históricos anteriores a esa compuerta no deben
considerarse inválidos por carecer de certificado. `corpus/resultados/archivo/` contiene artefactos no
canónicos, como borradores, que no forman parte del corpus activo.

No editar masivamente los JSON canónicos durante la limpieza. Toda normalización o tabla derivada debe vivir
en un espacio nuevo de Fase 3, mantener `documento.handle` como llave estable y registrar la versión/hashes
de los insumos. Si se detecta un defecto en un resultado, corregirlo mediante una reparación explícita de
Fase 2, recertificarlo y documentar la nueva versión antes de regenerar los derivados.

## Objetivo de la próxima fase

Preparar un conjunto analítico longitudinal y reproducible que permita responder preguntas agregadas sobre
el corpus, sin perder la trazabilidad sección–dimensión–cita de Fase 2.

## Artefacto de entrada

El universo unificado se registra en `../fase3/inventario_corpus_v1.json`: reúne los 17 pilotos y los 227
resultados de producción sin moverlos de sus ubicaciones originales. El manifiesto conserva origen, ruta,
handle, título, fecha, hashes del JSON y del certificado cuando existe, y las claves superiores observadas.
Su validación actual confirma 244 handles únicos y correspondencia exacta con las 244 filas del CSV de
trazabilidad. Las exclusiones, auditorías y tablas derivadas deben referenciar este inventario y no depender
de un conteo directo de archivos.

## Secuencia recomendada

1. **Inventario y congelamiento.** [completado] Manifiesto construido en `../fase3/inventario_corpus_v1.json`; verificar handles únicos y
   correspondencia con el CSV de trazabilidad, y registrar la presencia/ausencia de certificados como
   metadato de procedencia, no como condición retroactiva de validez.
2. **Auditoría transversal.** Medir completitud, cardinalidades y valores de las dimensiones, tipologías,
   interpelaciones, niveles de aplicación, países/subregiones, fechas y citas. Reportar anomalías, sin
   reescribir la fuente canónica.
3. **Normalización.** Diseñar tablas derivadas separadas, al menos `documentos`, `secciones`,
   `dimensiones`, `citas`, `interpelaciones` y `tipologias`. Conservar `handle`, ruta jerárquica de sección,
   página y un identificador de versión del resultado de origen.
4. **Diccionario y reglas.** Declarar taxonomías, mapeos, valores faltantes, deduplicación de citas y reglas
   para lenguaje, geografía, nivel de aplicación y fechas. Versionar todo mapeo manual.
5. **Control de calidad.** Ejecutar validaciones de unicidad, integridad referencial, cobertura y muestras
   humanas de los registros normalizados. Las correcciones deben ser idempotentes y regenerables.
6. **Análisis agregados.** Solo después de aprobar los derivados: tabulados por transformación, dimensión,
   criterio de interpelación, período, geografía y tipo documental; explicitar denominadores y exclusiones.

## Invariantes que se deben preservar

- `documento.handle` es la clave primaria estable del corpus.
- Una cita sigue ligada a su página y a su sección de origen; no convertirla en evidencia desanclada.
- Los valores de interpelación (`Sí`, `Parcial`, `No`) y la tipología conservan sus justificaciones y certeza.
- Los resultados analíticos derivados no reemplazan los JSON certificados.
- Las fuentes descargadas, tramos y SQLite son artefactos locales/reproducibles; no son el producto
  canónico versionado.

## Exclusiones de Git para este cierre

Se versionan resultados canónicos, certificados, documentación, manifiestos, prompts estándar y el código
del pipeline, incluidos scripts de reparación que preservan la procedencia de Fase 2. Permanecen fuera de
Git los PDFs descargados, extracciones intermedias, SQLite y snapshots de ejecución, configuraciones locales
de agentes, prompts temporales y launchers/monitores locales. Las exclusiones están declaradas en
`../.gitignore`.

## Primer comando de la próxima sesión

```bash
python3 fase2/pipeline/ledger.py status --json
```

Debe devolver 244 documentos `approved` antes de iniciar cualquier derivado de Fase 3.
