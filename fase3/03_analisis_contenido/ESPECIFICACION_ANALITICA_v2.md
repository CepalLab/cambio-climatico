# Especificacion analitica v2 - Fase 3.3

**Fecha:** 2026-08-26  
**Estado:** plan aprobado para inicio de ejecucion  
**Version de base:** `fase3-analitica-v1`  
**Universo:** 238 documentos activos (244 historicos menos 6 exclusiones)

## 1. Proposito y productos

Fase 3.3 tiene dos productos conectados pero con ritmos distintos:

1. Una sintesis verificable de aproximadamente 30 paginas sobre la evolucion
   del abordaje de cambio climatico de la CEPAL entre 2015 y 2025.
2. Un activo analitico vivo para formular y responder preguntas futuras sin
   perder la trazabilidad hacia los documentos y citas canonicas.

El informe es el camino critico. El activo vivo se construye como derivado del
mismo trabajo analitico; no habilita cambios al canon ni retrasa la entrega.

### Reorientacion documental aprobada (2026-08-26)

El analisis empieza desde perfiles documentales completos: pregunta de
investigacion, ambito, resumen narrativo, hallazgos, conclusiones y
recomendaciones. La secuencia detallada esta en
[PLAN_REORIENTACION_DOCUMENTAL_v1.md](PLAN_REORIENTACION_DOCUMENTAL_v1.md).
Las dimensiones y citas se usan como prueba y profundizacion de sintesis
globales, no como puerta de entrada del analisis.

La primera capa directa ya se construyo sobre los 238 documentos. La matriz
ponderada de objetos, dominios y funciones se mantiene como candidata hasta
calibrar sus diez perfiles de referencia; no debe leerse todavia como una
distribucion experta del corpus.

## 2. Fuentes, limites y contrato de procedencia

### 2.1 Fuentes de verdad

- Los JSON certificados de Fase 2 son la fuente canonica de contenido,
  estructura, citas y paginas.
- `fase3/02_eda/salidas/fase3_analitica_v1.sqlite` es la capa reproducible de
  consulta y agregado.
- Los metadatos normalizados y las relaciones geograficas, sectoriales y de
  organizaciones son derivados v1; su estado y metodo deben preservarse al
  reportarlos.

### 2.2 Restricciones

- No reextraer las 8.329 dimensiones/citas ni reescribir masivamente el canon.
- No interpretar relaciones candidatas como codificacion experta definitiva.
- No usar conteos de citas como proxy unico de importancia sustantiva.
- No inferir causalidad por coocurrencia ni ausencia del fenomeno por ausencia
  de mencion.

### 2.3 Referencia de evidencia

Toda ficha de hallazgo debe incluir al menos una referencia con:

```json
{
  "document_id": "...",
  "dimension_id": 0,
  "page": "...",
  "quote": "...",
  "source_sha256": "...",
  "source_path": "..."
}
```

Tres a cinco documentos son una pauta para hallazgos transversales, no un
umbral mecanico. Un hallazgo acotado puede tener una evidencia principal, pero
debe declarar su alcance y limitacion.

## 3. Esquema SQLite vigente

Las consultas deben usar el esquema real de `construir_base_analitica.py`:

- `documents`: documento, ano, division, temas, resumen, ruta y hash de
  origen, tipo documental y niveles de aplicacion.
- `sections`: secciones jerarquicas, con `parent_section_id`, titulo, paginas
  y resumen.
- `dimensions`: cita auditada con `document_id`, `section_id`, dimension,
  pagina y subtipo de brecha.
- `relations`: relacion a nivel de `document_id`, con `field`, `entity_id`,
  `entity_name`, `source_value`, `status` y `method`.
- `interpellation` y `typology`: evaluaciones y clasificacion por documento.

En consecuencia, las relaciones no se enlazan actualmente a una dimension
individual. Las coocurrencias de entidades deben calcularse por documento o
declarar una nueva anotacion derivada con evidencia explicita; no se debe
inventar un `relations.dimension_id` inexistente.

## 4. Preguntas y operacionalizacion

Las nueve preguntas de la nota conceptual guian el analisis. Las dimensiones
existentes cubren directamente estado de situacion, diagnostico estructural,
propuestas, avances, brechas, tendencias, desafios y oportunidades.

Dos areas requieren una capa semantica derivada y controlada antes de afirmar
resultados agregados:

- `herramientas_decision`: instrumentos analiticos usados o propuestos para
  decisiones economicas, financieras o de planificacion.
- `participacion_publica`: mecanismos, procesos, derechos o dispositivos de
  participacion de poblacion, sociedad civil o comunidades en decisiones.

Cada concepto nuevo debe tener una definicion, criterios de inclusion y
exclusion, ejemplos ancla, responsable, version y referencias de evidencia.
No son nuevas dimensiones del canon: son anotaciones analiticas revisables.

## 5. Metricas y comparacion temporal

Se usa un unico binning:

| Periodo | Rango |
| --- | --- |
| P1 | 2015-2018 |
| P2 | 2019-2022 |
| P3 | 2023-2026 |

P3 debe declararse como periodo abierto, porque el corpus actual llega hasta
2025. Todo cuadro temporal declara documentos por periodo y reporta, segun la
pregunta:

- documentos con al menos una dimension o anotacion pertinente;
- proporcion sobre documentos del periodo;
- citas por documento como indicador secundario de intensidad;
- distribucion por tipologia, interpelacion o nivel de aplicacion cuando sea
  pertinente;
- excepciones y contraejemplos cualitativos.

## 6. Ficha de hallazgo

La ficha es la unidad comun entre consulta, revision, grafo e informe. Cada
ficha versionada contiene:

```json
{
  "finding_id": "F3-...",
  "question_id": "P1-P9",
  "claim": "Interpretacion acotada y verificable.",
  "scope": {"periods": ["P1"], "filters": []},
  "quantitative_support": [],
  "evidence": [],
  "exceptions": [],
  "confidence": "high|medium|low",
  "status": "draft|reviewed|approved|superseded",
  "base_version": "fase3-analitica-v1",
  "review": {"reviewer": "", "reviewed_at": "", "notes": ""}
}
```

Una ficha aprobada puede alimentar el informe. Una ficha borrador es una
hipotesis de trabajo y no debe presentarse como conclusion.

## 7. Cerebro vivo y grafo derivado

El cerebro vivo no es una migracion a Neo4j ni una base alternativa. Es un
conjunto de derivados versionados que preservan significado y decisiones:

- preguntas y subpreguntas;
- conceptos analiticos controlados;
- fichas de hallazgo y sus revisiones;
- decisiones metodologicas;
- nodos y aristas exportables para navegacion.

El grafo minimo tendra nodos `Document`, `Dimension`, `Entity`, `Concept`,
`Finding` y `Question`; y aristas `CONTAINS`, `MENTIONS`, `EVIDENCES`,
`ADDRESSES`, `SUPPORTS`, `QUALIFIES` y `SUPERSEDES`. Toda arista que no se
derive directamente de SQLite debera declarar evidencia y estado de revision.

SQLite calcula y filtra. El grafo permite recorrer evidencia, conceptos,
preguntas y decisiones. Embeddings, chat sobre el corpus o un motor de grafo
especializado quedan fuera del MVP y se evaluan despues del informe.

## 8. Plan de ejecucion

### M1. Contrato analitico

Publicar esta especificacion y el indice de la carpeta. Confirmar esquema,
denominadores, criterios de evidencia y formatos de salida.

**Criterio de salida:** documentacion enlazada desde los puntos de entrada de
Fase 3 y sin contradiccion con el esquema SQLite vigente.

### M2. Capa viva minima (iniciada 2026-08-26)

Crear formatos versionados para preguntas, conceptos, hallazgos, decisiones y
exportacion de grafo. No poblar masivamente conceptos aun.

Los contratos, catalogos y el ejemplo trazable de esta mision estan enlazados
desde el [README de analisis de contenido](README.md). El ejemplo no es un
hallazgo sustantivo ni se puede promover al informe.

**Criterio de salida:** una ficha de ejemplo puede enlazar una pregunta con una
dimension, una cita y un concepto sin ambiguedad de procedencia.

### M3. Paquetes de evidencia (completada 2026-08-26)

Implementar consultas reproducibles por pregunta. Cada paquete incluye SQL,
parametros, metricas, documentos y citas candidatas, y limitaciones.

El generador de los dos paquetes piloto vive en
[`scripts/generar_paquetes_evidencia_v1.py`](scripts/generar_paquetes_evidencia_v1.py).
Las salidas se versionan en `salidas/` y conservan el hash de la base SQLite
usada para producirlas.

La primera ejecucion produjo `paquete_evolucion_enfoques_v1` y
`paquete_gobernanza_multinivel_v1`, con sus JSON, resumenes Markdown y el
universo de citas candidatas. Ambas salidas son insumos para M4, no hallazgos
aprobados.

**Criterio de salida:** las metricas se regeneran desde SQLite y sus conteos
declaran denominador, filtros y version de base.

### M4. Piloto doble (iniciada 2026-08-26)

Ejecutar primero: (a) evolucion de enfoques 2015-2025 y (b) gobernanza
multinivel, capacidades e implementacion. Producir entre cinco y ocho fichas
de hallazgo por piloto.

**Criterio de salida:** cada ficha tiene evidencia verificable, una revision
humana y una observacion de segundo modelo sobre una muestra.

La seleccion de lectura y las planillas de registro se generan con
[`scripts/seleccionar_muestra_piloto_v1.py`](scripts/seleccionar_muestra_piloto_v1.py).
El procedimiento humano esta definido en
[GUIA_REVISION_HUMANA_PILOTO_v1.md](GUIA_REVISION_HUMANA_PILOTO_v1.md).
La revision humana se realiza sobre fichas de hallazgo `draft`; las planillas
de citas son respaldo de trazabilidad y no una tarea de lectura exhaustiva.

La primera ronda de revision de evolucion de enfoques esta sintetizada en
[hallazgos/REVISION_HALLAZGOS_EVOLUCION_v1.md](hallazgos/REVISION_HALLAZGOS_EVOLUCION_v1.md).
Contiene cinco fichas `draft` con metricas temporales, tres citas canonicas
por ficha y limites de interpretacion explicitos.

### M5. Estabilizacion

Ajustar vocabulario, protocolo de hallazgos y exportacion de grafo con las
lecciones del piloto. Luego cubrir las nueve preguntas.

### M6. Informe y visor

Redactar el informe desde fichas aprobadas y exponer en Streamlit un visor de
evidencia y relaciones. El visor se limita inicialmente a exploracion; no
incluye un chat generico.

## 9. Controles de calidad

- Cada salida declara base, denominador, filtros, exclusiones y fecha.
- Cada metrica conserva consulta o script, parametros y resultado versionado.
- Cada hallazgo se valida contra `dimensions`, paginas y hash de origen.
- Una muestra de hallazgos recibe revision humana y auditoria de segundo
  modelo antes de promoverse al informe.
- Las nuevas anotaciones conservan responsable, fecha, version y estado.

## 10. Registro de decisiones

- **2026-08-26:** se adopta el modelo de dos velocidades: informe como camino
  critico y cerebro vivo como derivado incremental.
- **2026-08-26:** se descarta Neo4j como prerrequisito; SQLite v1 es el motor
  de consulta del MVP.
- **2026-08-26:** las preguntas sobre herramientas de decision y participacion
  publica se resuelven mediante conceptos analiticos derivados, no mediante
  modificacion retroactiva de dimensiones canonicas.