# Modelo de conocimiento vivo v1

**Estado:** vigente para el MVP de Fase 3.3  
**Base de evidencia:** `fase3-analitica-v1`

## Proposito

Este contrato define derivados revisables para trabajar preguntas presentes y
futuras sin alterar los JSON canonicos de Fase 2. Los artefactos usan JSON
valido, claves en espanol y `snake_case`.

## Artefactos y ubicacion

| Artefacto | Ubicacion | Unidad estable |
| --- | --- | --- |
| Catalogo de preguntas | `preguntas/` | `question_id` (`P1` a `P9`) |
| Catalogo de conceptos | `conceptos/` | `concept_id` (`CON-...`) |
| Ficha de hallazgo | `hallazgos/` | `finding_id` (`F3-...`) |
| Decision metodologica | `decisiones/` | `decision_id` (`DEC-...`) |
| Exportacion navegable | `grafo/` | `node_id` y `edge_id` |

## Reglas de identidad y procedencia

- `document_id` corresponde exactamente a `documents.document_id` de SQLite.
- `dimension_id` corresponde exactamente a `dimensions.dimension_id` de
  SQLite.
- La evidencia canonica conserva pagina, cita, `source_path` y
  `source_sha256`.
- Los conceptos, hallazgos y aristas interpretativas declaran `status`,
  responsable y fecha. Son derivados, no citas literales.
- Una ficha con estado `draft` o `reviewed` no es una conclusion del informe.
  Solo `approved` puede promocionarse a redaccion.

## Formato minimo por artefacto

### Pregunta

Una pregunta contiene texto, proposito, dimensiones de partida, conceptos
requeridos, filtros posibles y limitaciones. Las preguntas no son hallazgos.

### Concepto

Un concepto contiene definicion operativa, criterios de inclusion y exclusion,
ejemplos ancla y referencias. Un concepto puede ser `draft`, `reviewed`,
`approved` o `deprecated`.

### Hallazgo

Un hallazgo contiene una interpretacion acotada, alcance, apoyo cuantitativo,
evidencia, excepciones, nivel de confianza y revision. La evidencia es una
lista de referencias canonicas, no una bibliografia libre.

### Decision

Una decision registra que se adopto, difirio o rechazo una regla, con motivo,
impacto, responsable y artefactos afectados.

### Grafo

El grafo se exporta como JSON de nodos y aristas. Las aristas directas de
SQLite pueden indicar `derived_from: "sqlite"`; las aristas analiticas deben
llevar `evidence_refs` y su estado de revision.

## Ciclo de vida

1. Registrar o precisar una pregunta.
2. Proponer un concepto o reutilizar uno aprobado.
3. Generar evidencia reproducible desde SQLite.
4. Crear ficha de hallazgo en `draft`.
5. Revisar evidencia, excepciones y alcance.
6. Promover a `approved` o marcar `superseded` con una decision trazable.

El ejemplo de M2 en las carpetas hermanas demuestra el recorrido completo,
pero no constituye un resultado sustantivo del corpus.