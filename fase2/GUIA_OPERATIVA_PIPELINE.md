# Guía operativa — pipeline de enriquecimiento Fase 2b

**Qué es esto**: instrucciones para ejecutar el pipeline de análisis profundo hoy, en cualquier harness o
modelo. Es una guía de "cómo correrlo", no un registro de decisiones — para el razonamiento detrás de cada
regla, el histórico de calibración (Rondas 1-4) y la postura crítica sobre el enfoque, ver
[PLAN_ANALISIS_PROFUNDO.md](PLAN_ANALISIS_PROFUNDO.md). Si una regla de acá parece arbitraria, la
justificación está ahí, no en este documento.

**Antes de correr el pipeline sobre un documento nuevo**, leer en este orden:

1. [codebook_v0.md](codebook_v0.md) — dimensiones del codebook, unidad de análisis (apartado).
2. [INTERPELACION_v0.md](INTERPELACION_v0.md) — los 4 criterios de interpelación y sus reglas de decisión.
3. [TIPOLOGIA_v0.md](TIPOLOGIA_v0.md) — protocolo de 5 pasos para transformación primaria/secundaria.
4. [big_push.md](big_push.md) — definición operativa del "gran impulso ambiental" (criterio i de interpelación).
5. [esquema_json_v1.md](esquema_json_v1.md) — esquema de salida, reglas transversales, slugs canónicos.

---

## Etapa 0 — Adquisición de documentos (sin scraping)

El repositorio de CEPAL corre DSpace 7.5 y expone una API REST pública sin autenticación:

```
GET /server/api/pid/find?id={handle}          → 302 → /server/api/core/items/{uuid}
GET /server/api/core/items/{uuid}             → metadatos, incluye dc.format.extent ("107 páginas")
GET /server/api/core/items/{uuid}/bundles     → bundles ORIGINAL (PDF), TEXT (txt autoextraído), THUMBNAIL
GET /server/api/core/bundles/{uuid}/bitstreams → URL de descarga directa de cada bitstream
```

Implementado en [pipeline/cepal_repositorio.py](pipeline/cepal_repositorio.py) (solo stdlib, sin dependencias
nuevas — este pipeline corre offline, fuera de la app Streamlit desplegada, así que no toca
`requirements.txt`). Se resuelve el handle → se descarga el PDF (o se usa el `.txt` para un pre-filtro
rápido) → `dc.format.extent` dice de antemano cuántas páginas tiene, lo que permite decidir la estrategia de
lectura (una sola pasada vs. paginado) antes de gastar ninguna llamada de lectura.

**PDFs no se versionan en git** — se descargan a `fase2/pilot/pdfs/` (o `fase2/corpus/pdfs/` a escala),
carpeta agregada a `.gitignore`. Solo los artefactos de salida (JSON/CSV enriquecidos) se commitean.

## Etapa 1 — Lectura de texto completo

Usar la herramienta de lectura de PDF nativa del harness (`Read` en Claude Code) sobre el PDF descargado, no
el `.txt` autoextraído por DSpace: el `.txt` de DSpace tiene artefactos de intercalado de columnas en
layouts a dos columnas (p. ej. "IntroduJcatniouna ry" en vez de "Introduction... January 1, 2018"), mientras
que una lectura nativa de PDF de buena calidad reordena columnas correctamente. El `.txt` sirve como
fallback barato para un futuro pre-filtro por palabra clave a escala de corpus, no para la extracción fina.

Para documentos largos, `dc.format.extent` permite decidir de antemano si hace falta paginar la lectura en
varios tramos (los informes insignia de Agenda 2030 rondan 200-300 páginas). Ver
[PLAN_ANALISIS_PROFUNDO.md §3.3](PLAN_ANALISIS_PROFUNDO.md) para los números reales de consumo de contexto
observados en el piloto.

**Si el harness no tiene una herramienta de lectura de PDF nativa equivalente, o su calidad de extracción no
está verificada**: no seguir a la Etapa 2 sin antes correr el
[Protocolo de prueba de portabilidad](#protocolo-de-prueba-de-portabilidad-de-harnessmodelo) de este
documento.

## Etapa 2 — Enriquecimiento documental

A partir del texto completo, extraer con evidencia textual (no parafraseo libre):

- Pregunta(s) de investigación explícita o implícita del documento.
- Alcance: `ambito_aplicacion` (región/países donde el documento analiza o propone aplicar) separado de
  `referentes_dependencias` (países/bloques citados solo como comparación u origen de un instrumento
  externo), más alcance sectorial y temporal.
- Hallazgos principales (con cifra o cita concreta cuando exista). Cifras no literales (derivadas de un
  gráfico o tabla) se marcan como computadas, indicando la operación — ver la regla de
  [esquema_json_v1.md §2](esquema_json_v1.md).
- Conclusiones y recomendaciones (distinguiendo explícitamente cuáles son del documento y cuáles son
  recomendaciones a terceros/gobiernos).
- `resumen_narrativo`: 3-5 oraciones en formato de relato, no de lista. Guardrail anti-genérico: debe fallar
  el test "¿esto podría describir cualquier otro documento del corpus con solo cambiar el título?" —
  incluir al menos 2 elementos verificables y específicos (cifra, mecanismo nombrado, país/subregión,
  hallazgo distintivo).

## Etapa 3 — Resumen de secciones

A partir del índice (cuando existe — los documentos de proyecto/estudios técnicos de CEPAL casi siempre lo
traen; los policy briefs cortos no: en ese caso los **encabezados tipográficos de nivel 1 cuentan como
índice**, cada encabezado es una sección propia y no se fusionan secciones contiguas), un resumen por
sección con:

- Título y rango de páginas de la sección, según la numeración interna del documento.
- **Estructura anidada por niveles**: se capturan siempre todas las secciones de nivel 1 del índice, en
  orden, sin excepciones. Se desciende a subsecciones (`subsecciones`, mismo shape, `nivel` 2 o 3) solo
  cuando el padre supera ~8-10 páginas; nunca se aplanan ni se salta del nivel 1 al nivel 3 sin registrar el
  padre intermedio.
- **Dimensiones solo en las hojas**: cuando una sección tiene `subsecciones`, el padre lleva
  `"dimensiones": []` — las etiquetas viven en las subsecciones, salvo que el padre tenga contenido propio
  no cubierto por ningún hijo, en cuyo caso ese fragmento sí lleva su propia cita+página.
- **El resumen ejecutivo/abstract del documento no se procesa como sección** (su contenido ya alimenta
  `resumen_enriquecido`; procesarlo duplicaría el conteo de dimensiones en el agregado). Se deja constancia
  con `documento.tiene_resumen_ejecutivo: true`.
- **Los anexos técnicos no se procesan como sección** (metodología detallada, pruebas de robustez, fuentes
  de datos). No se etiquetan dimensiones sobre su contenido.
- Resumen de largo proporcional al número de páginas de la sección (~1 línea por página, piso de 3-4 líneas,
  sin techo), que incluya (a) el argumento/función de la sección dentro del documento — qué trabajo hace, no
  solo qué temas toca —, (b) cifras o datos clave si los hay, (c) instrumentos/actores/casos nombrados si
  los hay.
- Etiquetado con las 9 dimensiones canónicas del codebook (multi-etiqueta), con **al menos una cita textual
  + página propia por cada dimensión etiquetada** — una dimensión no hereda la cita de otra dimensión de la
  misma fila.

## Etapa 4 — Interpelación institucional

Metodología completa en [INTERPELACION_v0.md](INTERPELACION_v0.md): 4 criterios de la nota conceptual, cada
uno con veredicto en 3 valores (Sí / Parcial / No — nunca binario), regla anti-copia (evidencia = cita
textual literal con página, nunca parafraseo de la definición del criterio), y definición operativa por
criterio. Se aplican los 4 criterios sin excepción a todo documento del corpus, incluso a los de naturaleza
distinta a una propuesta de política climática (diagnósticos, proyecciones cuantitativas) — en esos casos el
campo `nota` debe indicar explícitamente esa naturaleza distinta.

## Etapa 5 — Tipología de documentos

Metodología completa en [TIPOLOGIA_v0.md](TIPOLOGIA_v0.md): transformación primaria/secundaria reutilizando
el canon de las 11 Grandes Transformaciones, con el protocolo de 5 pasos (tensión dialéctica → primaria →
secundaria obligatoria → justificación anti-copia → validación de anclas). El "tipo de brecha" (retrospectiva
/ prospectiva) no es un eje de tipología — vive en el codebook como `subtipo_brecha` de la dimensión
`brechas_implementacion`.

## Etapa 6 (futura) — Mapeo a preguntas de investigación

Explícitamente pospuesta hasta depurar las preguntas de investigación de la nota conceptual (son 9, no 8 —
la novena, participación pública, es fácil de perder) y fijar su unidad de análisis (corpus completo, no
documento ni apartado). No construir sobre esto todavía.

---

## Validación

Correr `python fase2/pipeline/validar_esquema.py [rutas...]` sobre cada JSON producido antes de darlo por
completo. Sin argumentos, valida los 3 JSON del piloto. Chequea estructura (claves, slugs, formato de citas,
veredictos, tipología) y hace un chequeo heurístico de referencias cruzadas — **no** chequea calidad de
juicio (evidencia genérica vs. específica, veredictos correctos); eso depende de la disciplina de quien
ejecuta el pipeline, humano o modelo.

## Cuándo usar Workflow

Para 1 documento suelto, lectura directa alcanza — no hace falta orquestación. Para lotes (los 12 documentos
restantes de la muestra de calibración, o los 244 del corpus), usar el patrón `pipeline()` del framework de
Workflow del Lab: **un documento por agente, las etapas 1→5 encadenadas dentro de la misma
conversación/agente** (nunca un agente nuevo por etapa — repagar la lectura del texto fuente en cada etapa
cuesta 2.5-3x más sin aportar nada; ver el detalle de costo en
[PLAN_ANALISIS_PROFUNDO.md §4.3](PLAN_ANALISIS_PROFUNDO.md)), en paralelo entre documentos. Para invocarlo,
pedirlo explícitamente — p. ej. *"corré el pipeline de enriquecimiento sobre los 12 documentos restantes de
la muestra usando un workflow"*. No conviene lanzarlo antes de que el equipo del curso valide el enfoque del
piloto (ver [PLAN_ANALISIS_PROFUNDO.md §5](PLAN_ANALISIS_PROFUNDO.md)).

## Revisión ciega externa de veredictos (posterior al lote, fuera de este pipeline)

La parte subjetiva de la salida (interpelación + tipología) se verifica con una **segunda lectura ciega en
un harness/modelo externo**, corrida por lotes una vez completado el trabajo del ejecutor — no es una etapa
de este pipeline y no la ejecuta el mismo agente. Instrucciones autocontenidas (insumos exactos, regla de
ceguera, formato de salida, comparación y adjudicación) en
[INSTRUCCIONES_REVISOR_EXTERNO.md](INSTRUCCIONES_REVISOR_EXTERNO.md). Para el piloto de la muestra de 17 el
revisor designado es DeepSeek en OpenCode (Ronda 5); el rol es intercambiable por cualquier harness/modelo
que pase el protocolo de portabilidad de abajo.

---

## Protocolo de prueba de portabilidad de harness/modelo

**Por qué hace falta un protocolo, no solo "probarlo y ver"**: el pipeline depende de dos capacidades que
hoy se dan por sentadas dentro de Claude Code y que no están garantizadas en otro harness o modelo:

1. **Extracción de PDF fiel** — la Etapa 1 depende de que la herramienta de lectura del harness reordene
   columnas, tablas y notas al pie correctamente (ver
   [PLAN_ANALISIS_PROFUNDO.md §1.4](PLAN_ANALISIS_PROFUNDO.md)). Esto sigue sin resolverse de forma agnóstica
   de harness — el candidato pendiente es un extractor determinístico (`docling`) que corra una vez por
   documento y deje un artefacto de texto/Markdown reutilizable por cualquier harness.
2. **Disciplina de juicio calibrada** — los criterios de interpelación y tipología se afinaron en 4 rondas de
   corrección humana específicas para las fallas observadas en este modelo (evidencia genérica vs. la más
   fuerte, veredictos ante ambigüedad, anti-"justificación zombie"). La metodología escrita reduce el riesgo
   de que otro modelo repita esos mismos errores, pero no lo elimina — y `validar_esquema.py` no lo detecta,
   porque chequea forma, no calidad de juicio.

Este protocolo no resuelve el punto 1 (sigue haciendo falta que el harness lea PDF razonablemente bien, o
correr `docling` antes) — pero da una forma barata de saber, con evidencia y no con supuestos, si vale la
pena portar el pipeline a otro harness/modelo antes de escalar.

> **Este protocolo ya se ejecutó una vez** (2026-07-13, Ronda 5): 4 corridas nuevas sobre doc09 con
> modelos/harnesses distintos, más la referencia calibrada. Resultados, ranking y refuerzos propuestos en
> [pilot/EVALUACION_MULTIMODELO_DOC09.md](pilot/EVALUACION_MULTIMODELO_DOC09.md) (registro de evaluación —
> **no es metodología del pipeline**, no leerlo como insumo para correr el pipeline). Hallazgo principal:
> los 3 checkpoints del Paso 5 no capturan todos los modos de falla observados — hay una propuesta de
> ampliarlos a ~6, pendiente de decisión.

**Paso 1 — Elegir el caso de prueba**: usar doc09
([pilot/doc09_caribbean_power.json](pilot/doc09_caribbean_power.json), 12 páginas totales / 10 hasta
conclusiones) — es el más corto del piloto y ya pasó por las 4 rondas de calibración, así que su JSON actual
sirve de respuesta de referencia conocida.

**Paso 2 — Aislar el insumo**: darle al harness/modelo nuevo *solo*
[pilot/pdfs/doc09_caribbean_power.pdf](pilot/pdfs/doc09_caribbean_power.pdf) (o su `.txt` si no puede leer
PDF nativamente) más los 5 documentos de metodología listados al inicio de esta guía. No mostrarle
`pilot/doc09_caribbean_power.json` — contaminaría la prueba.

**Paso 3 — Chequeo de extracción (bloqueante)**: antes de mirar el contenido analítico, comparar 3-4 pasajes
del texto que el harness dice haber leído contra el PDF original, priorizando zonas de dos columnas o
tablas (p. ej. el Diagrama 1 o la Tabla 1 de doc09). Si aparece intercalado de columnas (el artefacto ya
documentado: "IntroduJcatniouna ry" en vez de texto corrido), ese harness necesita un extractor
determinístico antes de seguir — no tiene sentido evaluar el resto todavía.

**Paso 4 — Validación estructural**: correr `pipeline/validar_esquema.py` sobre el JSON producido. Si falla
estructuralmente, es un problema de instrucción-seguimiento del formato, no de portabilidad de la
metodología — reforzar el prompt con el esqueleto de `esquema_json_v1.md §1` y reintentar antes de sacar
conclusiones sobre juicio.

**Paso 5 — Chequeo de calidad de juicio**, contra 3 puntos de doc09 ya conocidos como difíciles:

- Criterio (ii) articulación de actores: ¿cita el IRRP/CCREEE (p.6-7) como el mecanismo con nombre propio, o
  cae en la evidencia genérica de p.9 ("debería haber diálogo multiactor") que Ronda 2 identificó como el
  error típico de citar lo más fácil en vez de lo más fuerte?
- Criterio (iv) cómo hacerlo: ¿desglosa las 8 recomendaciones ítem por ítem (tally M de N), o acredita la
  lista completa como "Sí" sin revisar cada una?
- Tipología: ¿llega a primaria #6 Sostenibilidad ambiental / secundaria #11 Capacidades del Estado con
  certeza "Alta" (el ancla ya validada en [TIPOLOGIA_v0.md §3](TIPOLOGIA_v0.md)), con justificación
  anti-copia específica del documento?

**Paso 6 — Decisión**:

- Si falla el Paso 3 → no portable todavía; resolver extracción determinística primero (no es un problema de
  esta metodología, es un problema del harness).
- Si pasa el Paso 3 pero falla el Paso 5 en 2 o más puntos → la metodología escrita no alcanza sola para ese
  modelo; necesitaría sus propias rondas de calibración (como las que corrió este piloto), no asumir
  portabilidad directa.
- Si pasa ambos → portable con confianza moderada; antes de escalar a los 12 documentos restantes con ese
  harness, correr un segundo documento (recomendado: doc13, el caso de estrés con anexos y ambigüedad de
  tipología) para confirmar que no fue un acierto puntual.
