# Fase 3 — depuración, revisión transversal, normalización y análisis agregados

## Propósito

Preparar un corpus activo, consistente y trazable para análisis agregados, sin perder los JSON canónicos
producidos y certificados durante Fase 2.

## Secuencia de trabajo

### Artefacto inicial

`inventario_corpus_v1.json` es el manifiesto único de entrada: integra los 17 pilotos y los 227 resultados
de producción, conserva sus rutas de origen y registra procedencia, hashes y disponibilidad de certificados.
Antes de generar derivados, debe comprobarse que mantenga 244 handles únicos y correspondencia con el CSV.

El `num_muestra` de resultados de producción se reconstruye, cuando falta, desde `corpus_order` del ledger,
que es el orden estable del corpus definitivo. No se usa el orden alfabético de archivos ni la posición local
de un lote. La corrección se aplica al campo `documento.num_muestra`, se registra en el historial de cambios
y, si el resultado tiene certificado, se actualiza el `result_sha256` del certificado.

### Fase 3.0 — Depuración del universo

Identificar las publicaciones que se incorporaron al corpus por error y excluirlas antes de construir
indicadores agregados.

- No borrar JSON ni evidencia histórica.
- Registrar cada exclusión con `handle`, título, motivo, responsable, fecha y decisión.
- Mantener separados el corpus histórico completo y el corpus activo para análisis.
- Regenerar inventarios, denominadores y manifiestos desde las exclusiones aprobadas.

#### Procedimiento para revisiones y ajustes

Las alertas automáticas —por ejemplo, documentos cuya tipología no contiene `Sostenibilidad ambiental`
— son colas de revisión, no decisiones de exclusión. Cada caso debe clasificarse en una de estas tres
salidas:

1. **Mantener sin cambios:** la clasificación y la inclusión en el corpus son defendibles.
2. **Reclasificar:** el documento pertenece al corpus, pero cambia su transformación primaria o secundaria.
3. **Excluir:** el documento no debió formar parte del corpus; se conserva su JSON como registro histórico.

Las reclasificaciones y las exclusiones se registran por separado. El registro mínimo de cada revisión es:
`handle`, título, ruta del JSON, clasificación actual, propuesta, tipo de decisión, evidencia revisada,
justificación, certeza, revisor, fecha y estado (`pendiente`, `adjudicado` o `aplicado`). La decisión debe
revisarse contra la pregunta de investigación, resumen, conclusiones, estructura del documento y anclas de
`TIPOLOGIA_v0.md`, distinguiendo el objeto sustantivo de los instrumentos institucionales.

Los registros de trabajo son [revisiones_tipologia_v1.csv](00_control/revisiones/revisiones_tipologia_v1.csv) y
[exclusiones_corpus_v1.csv](00_control/inventario/exclusiones_corpus_v1.csv). El primer caso registrado es `11362/48413`, como
propuesta pendiente de adjudicación; el registro de exclusiones todavía no contiene decisiones.

Una decisión adjudicada se aplica solo de forma individual y explícita al JSON canónico. Se conserva un
registro antes/después; si existe certificado, se regenera y se actualiza su hash. Luego se regenera el
inventario y se ejecutan controles de handles, esquema y la alerta que originó la revisión. No se hacen
reescrituras masivas ni se convierten las alertas tipológicas en exclusiones automáticas.

### Fase 3.1 — Revisión transversal de dimensiones y citas

Auditar la relación dimensión → cita para comprobar que la evidencia sea literal, relevante y semánticamente
coherente con la dimensión declarada.

- Revisar literalidad, página, relevancia y relación semántica de cada cita.
- Priorizar inconsistencias sistemáticas y los casos de mayor impacto analítico.
- Toda corrección debe modificar explícitamente el JSON canónico de Fase 2, regenerar su certificado cuando
  corresponda y documentar la reparación.
- No avanzar a agregados mientras existan defectos metodológicos conocidos que alteren las conclusiones.

### Fase 3.2 — Normalización de derivados

Construir estructuras normalizadas a partir del corpus ya depurado y revisado.

- Conservar los JSON de Fase 2 como fuente inmutable; no hacer una reescritura masiva del canon.
- Crear derivados versionados, como mínimo: `documentos`, `secciones`, `dimensiones`, `citas`,
  `interpelaciones` y `tipologias`.
- Usar `documento.handle` como llave primaria estable y preservar ruta jerárquica, páginas y versión del
  resultado de origen.
- Versionar los diccionarios, mapeos manuales, taxonomías y reglas para valores faltantes o deduplicación.

### Fase 3.3 — Análisis agregados

Con el corpus activo, revisado y normalizado, producir tabulados y análisis por dimensión, transformación,
interpelación, período, geografía y tipo documental. Todo resultado debe declarar su denominador, filtros y
exclusiones.

#### Inicio operativo 2026-08-26

El contrato de ejecución, el modelo de evidencia y el plan de entregables viven
en [03_analisis_contenido/ESPECIFICACION_ANALITICA_v2.md](03_analisis_contenido/ESPECIFICACION_ANALITICA_v2.md).
La implementación separa dos productos conectados: la síntesis de 30 páginas,
que es el camino crítico, y un activo analítico vivo derivado para consultas
futuras. SQLite sigue siendo el motor de agregados; el grafo se construye como
exportación navegable y trazable, no como prerrequisito tecnológico.

Antes de extender el análisis a las nueve preguntas, se ejecutarán dos pilotos:
evolución de enfoques 2015-2025 y gobernanza multinivel, capacidades e
implementación. Sus fichas de hallazgo deberán superar controles de evidencia,
revisión humana y auditoría de segundo modelo.

## Regla de orden

Primero definir quién entra al corpus activo; después comprobar la calidad de la evidencia; luego normalizar;
solo al final construir análisis agregados.
