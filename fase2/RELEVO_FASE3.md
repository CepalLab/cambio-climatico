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

Como housekeeping previo, se reconstruyeron diez valores faltantes de `documento.num_muestra` desde el
`corpus_order` estable del ledger: `40457=35`, `40887=42`, `40922=44`, `41867=51`, `42725=62`, `44218=81`,
`46643=126`, `80595=196`, `82456=221` y `82547=223`. En los tres casos con certificado se sincronizó el
hash del resultado; el inventario se regenera después de esta corrección.

Las seis exclusiones adjudicadas por etiquetado temático erróneo o por tratarse de documentos no sustantivos
ya se aplican al corpus activo de la aplicación Streamlit, que queda en 238 publicaciones. El inventario
histórico conserva las 244 y los JSON originales no se eliminan.

## Secuencia recomendada

1. **Inventario y congelamiento.** [completado] Manifiesto construido en `../fase3/inventario_corpus_v1.json`; verificar handles únicos y
   correspondencia con el CSV de trazabilidad, y registrar la presencia/ausencia de certificados como
   metadato de procedencia, no como condición retroactiva de validez.
2. **Auditoría transversal.** Medir completitud, cardinalidades y valores de las dimensiones, tipologías,
   interpelaciones, niveles de aplicación, países/subregiones, fechas y citas. Reportar anomalías, sin
   reescribir la fuente canónica. [auditoría v1 generada] El corpus activo de 238 tiene 7.812 secciones,
   8.329 dimensiones/citas y 0 anomalías estructurales o taxonómicas tras corregir la nomenclatura de
   `11362/39089` a “Macroeconomía y fiscalidad”. Etapa cerrada.
   La validación exhaustiva del esquema v1 se ejecutó sobre los 238 activos: 230 quedaron sin observaciones
   y 8 requieren revisión de reglas de calidad (secciones excluidas detectadas por heurística, rangos de
   páginas, resúmenes cortos, rangos de recomendaciones y hojas con dimensiones vacías). No se detectaron
   claves obligatorias ausentes ni nombres de dimensiones fuera de la taxonomía.
   El caso `11362/3955` quedó resuelto: las secciones 5.5 y 6.5 se conservan como sustantivas y sus
   dimensiones existentes (`tendencias` y `diagnostico_estructural`) quedan reconocidas por el validador.
   El caso `11362/38120` también quedó resuelto: la sección VI se conserva como sustantiva porque sintetiza
   hallazgos y levanta implicaciones/recomendaciones de política; sus dimensiones (`estado_de_situacion` y
   `propuestas_politica`) y citas propias quedan reconocidas por el validador.
   El caso `11362/38985` quedó resuelto mediante revisión acotada de cuatro hojas: se agregaron siete
   dimensiones con citas literales verificables, se sincronizó el hash del JSON en el inventario y la
   auditoría transversal mantiene `0` anomalías (8.329 dimensiones/citas tras retirar evidencia no autónoma).
   El caso `11362/44590` quedó resuelto mediante corrección estructural: las 12 introducciones que habían
   heredado por error el rango completo de su capítulo se ajustaron a su página inicial, y se amplió el
   resumen de la sección B del capítulo IV por debajo del piso proporcional. El documento pasa el esquema;
   la validación bruta queda en 230 sin observaciones y 8 alertas de paginación aceptadas.
   La auditoría queda formalmente cerrada en `fase3/cierre_auditoria_v1.json` y
   `fase3/cierre_auditoria_v1.md`: las 8 entradas que aún aparecen en la validación bruta corresponden
   exclusivamente a 11 alertas de paginación aceptadas y documentadas, por lo que los pendientes efectivos
   son `0`. La siguiente etapa es diseñar la normalización de derivados.
   La Fase 3.1 de revisión semántica dimensión–cita revisó inicialmente 8.344 dimensiones y produjo 117
   candidatos. Tras la adjudicación y aplicación quedaron 8.329 dimensiones/citas; el cribado residual se
   conserva en `fase3/auditoria_dimensiones_v1.json` y `fase3/auditoria_dimensiones_v1.md`.
   Como primera adjudicación experta se revisaron los casos 12, 17, 40, 50, 59, 81, 88, 89 y 95:
   siete se mantienen, dos se reclasifican (`43419`: `diagnostico_estructural` → `propuestas_politica`;
   `47730`: `diagnostico_estructural` → `estado_de_situacion`) y ninguno se excluye. El detalle queda en
   `fase3/revision_semantica_casos_usuario_v1.csv`; se actualizaron hashes y se recertificó `47730`.
   La matriz semántica consolidada de los 117 candidatos quedó completa en
   `fase3/revision_semantica_117_v1.csv`: 41 mantenimientos, 75 reclasificaciones y 1 exclusión de
   dimensión; no hay decisiones pendientes, duplicados ni slugs no canónicos. Las 76 decisiones de cambio
   fueron aplicadas individualmente, con actualización de hashes y recertificación cuando las compuertas
   estuvieron disponibles.
   Las 11 alertas de paginación fueron revisadas y aceptadas como `mantener`: 7 corresponden a la heurística
   de rango de recomendaciones aplicada a desgloses que reúnen varios capítulos, y 4 a solapamientos normales
   entre rangos de subsecciones. Estas alertas no requieren modificar los JSON; el detalle queda en
   `fase3/revision_paginacion_v1.csv` y `fase3/revision_paginacion_v1.md`. La equivalencia PDF/visor/TXT queda
   explícitamente diferida.
3. **Normalización.** Diseñar tablas derivadas separadas, al menos `documentos`, `secciones`,
   `dimensiones`, `citas`, `interpelaciones` y `tipologias`. Conservar `handle`, ruta jerárquica de sección,
   página y un identificador de versión del resultado de origen.
4. **Diccionario y reglas.** Declarar taxonomías, mapeos, valores faltantes, deduplicación de citas y reglas
   para lenguaje, geografía, nivel de aplicación y fechas. Versionar todo mapeo manual.
5. **Control de calidad.** Ejecutar validaciones de unicidad, integridad referencial, cobertura y muestras
   humanas de los registros normalizados. Las correcciones deben ser idempotentes y regenerables.
6. **Análisis agregados.** Solo después de aprobar los derivados: tabulados por transformación, dimensión,
   criterio de interpelación, período, geografía y tipo documental; explicitar denominadores y exclusiones.

## Procedimiento de revisión

Las alertas de tipología se usan como cola de revisión. No implican por sí solas que un documento deba
excluirse. Cada caso se resuelve como `mantener`, `reclasificar` o `excluir`, con registros independientes
para revisiones tipológicas y exclusiones del corpus. El registro debe incluir handle, título, clasificación
actual y propuesta, evidencia, justificación, certeza, revisor, fecha y estado.

Una reclasificación o exclusión aprobada se aplica individualmente, conservando el antes/después y la
trazabilidad. Si el resultado tiene certificado, se regenera el certificado y su hash; después se regenera
el inventario y se repiten los controles de integridad. El caso `11362/48413` queda, por ahora, como
`pendiente` de revisión tipológica, no como exclusión.

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
