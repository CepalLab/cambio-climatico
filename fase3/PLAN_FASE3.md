# Fase 3 — depuración, revisión transversal, normalización y análisis agregados

## Propósito

Preparar un corpus activo, consistente y trazable para análisis agregados, sin perder los JSON canónicos
producidos y certificados durante Fase 2.

## Secuencia de trabajo

### Artefacto inicial

`inventario_corpus_v1.json` es el manifiesto único de entrada: integra los 17 pilotos y los 227 resultados
de producción, conserva sus rutas de origen y registra procedencia, hashes y disponibilidad de certificados.
Antes de generar derivados, debe comprobarse que mantenga 244 handles únicos y correspondencia con el CSV.

### Fase 3.0 — Depuración del universo

Identificar las publicaciones que se incorporaron al corpus por error y excluirlas antes de construir
indicadores agregados.

- No borrar JSON ni evidencia histórica.
- Registrar cada exclusión con `handle`, título, motivo, responsable, fecha y decisión.
- Mantener separados el corpus histórico completo y el corpus activo para análisis.
- Regenerar inventarios, denominadores y manifiestos desde las exclusiones aprobadas.

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

## Regla de orden

Primero definir quién entra al corpus activo; después comprobar la calidad de la evidencia; luego normalizar;
solo al final construir análisis agregados.
