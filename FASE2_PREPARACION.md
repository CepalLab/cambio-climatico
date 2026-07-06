# Preparación de Fase 2 — Análisis estructurado del corpus climático

**Fecha**: 2026-07-06
**Estado**: Propuesta v0, pendiente de validación con el equipo del curso (Valeria, Santiago Lorenzo/VTL)
**Contexto**: insumo de apoyo al curso "Innovar para la complejidad: Estrategias del sector público
para abordar el cambio climático en América Latina" (Montevideo, 1–4 sept. 2026). Ver
[nota_conceptual.docx](nota_conceptual.docx) para el documento original del equipo del curso.

---

## 1. Revisión crítica de la nota conceptual

La nota conceptual da el marco general (antecedentes, marco conceptual CEPAL, objetivo, preguntas
de investigación, metodología en 6 etapas) pero deja sin definir varios elementos que son
indispensables para diseñar un proceso de codificación/extracción de información. Puntos concretos:

- **Preguntas de investigación solapadas.** "Estado actual del cambio climático y sus impactos"
  (P1) y "diagnóstico estructural" (P2) tienen un límite conceptual borroso: un mismo párrafo sobre
  vulnerabilidad hídrica puede calzar en ambas. La nota no da una regla de decisión para asignar un
  fragmento a una u otra.
- **Dimensiones de codificación sin codebook.** La Etapa 3 (sección 7) lista 7 dimensiones (estado
  de situación, diagnóstico estructural, propuestas, avances/brechas, tendencias, desafíos,
  oportunidades) sin definiciones operativas, ejemplos, ni criterio de exclusividad mutua.
- **Unidad de análisis ambigua.** Se habla de "párrafos, secciones o hallazgos específicos"
  indistintamente — son tres granularidades técnicamente muy distintas y no se resuelve cuál usar.
- **"Nivel de aplicación" y "cobertura geográfica" sin taxonomía cerrada.** Se mencionan como
  variables a incorporar pero sin lista de valores (¿qué cuenta como subnacional? ¿"regional" es
  toda ALC o subregiones?).
- **Sin protocolo de validación experta.** Se nombra a Santiago Lorenzo (VTL) como responsable de
  "validación experta" en dos etapas, pero no hay tamaño de muestra, métrica de acuerdo, ni proceso
  para cuando el experto discrepe del resultado automatizado.
- **Cronograma ajustado dado el alcance real.** Mayo–junio 2026 para extracción a nivel de
  fragmento sobre 244 documentos, diseño de criterios de búsqueda para 8 preguntas, validación
  experta y síntesis de 30 páginas — sin colchón para iteración, pese a que el propio documento
  reconoce (sección 8, observaciones finales) que el proceso "debe mantenerse iterativo".
- **Sin definición de "hecho".** No se especifica qué constituye un resultado aceptable en la
  Etapa 3 (¿% de cobertura del corpus etiquetado? ¿qué tasa de acuerdo con el experto es suficiente?).

**Por qué avanzamos igual con los 244 documentos:** la construcción del corpus (filtrado por tema,
exclusión de duplicados/administrativos, agregación de los 14 documentos estratégicos) no depende
de estas ambigüedades — es un criterio documental objetivo, ya resuelto y trazable (ver
[SEGUNDA_FASE.md](SEGUNDA_FASE.md), [DOCUMENTOS_EXCLUIDOS_DEFINITIVO.md](DOCUMENTOS_EXCLUIDOS_DEFINITIVO.md)
y `documentos_definitivos_trazabilidad.csv`). Lo que sí depende del dominio —la Fase 2 propiamente—
no se puede automatizar a ciegas justamente por estas indefiniciones. La salida práctica: construir
un codebook borrador con la propia terminología de la nota, probarlo en una muestra chica, y usar
ese artefacto concreto para forzar la precisión conceptual que falta.

## 2. Intercambio con Valeria (2026-07-06)

Valeria pidió avanzar a Fase 2: pasar de documento completo a fragmentos codificados por dimensión
analítica, agregar variables de nivel de aplicación y cobertura geográfica, y traducir las 8
preguntas de investigación en criterios de búsqueda (keywords + filtros). El pedido delega buena
parte de las decisiones de contenido ("todas las sugerencias son bienvenidas, ustedes son los
expertos") al Lab, que aporta la capacidad técnica pero no la experticia de dominio en política
climática — esa le corresponde al equipo del curso.

**Respuesta acordada:** en vez de diseñar los criterios de búsqueda para las 244 publicaciones de
una vez, se propuso:

1. Lab construye una primera propuesta de codificación (este documento, sección 3) y la aplica
   sobre una muestra acotada (sección 4).
2. En paralelo, se le pide al equipo del curso (idealmente con Santiago Lorenzo) que haga su propia
   lectura y clasificación manual de esa misma muestra — el groundtruth — con definiciones propias
   de cada dimensión y de las variables de nivel de aplicación/cobertura geográfica.
3. Se comparan ambos resultados en una reunión, se afinan definiciones y criterios de búsqueda, y
   recién ahí se escala al corpus completo.

División de responsabilidades explícita: **Lab** = pipeline técnico de extracción/codificación y
calibración; **equipo del curso** = precisión conceptual de las dimensiones y validación de
contenido sobre la muestra. Esto evita que el Lab termine tomando decisiones analíticas de dominio
que no le corresponden, y obliga a que las definiciones que la nota conceptual dejó abiertas se
resuelvan con casos concretos en la mano.

## 3. Propuesta de codificación v0

Codebook construido a partir de las 7 dimensiones nombradas en la nota conceptual (sección 7,
Etapa 3), con las reglas de decisión y ejemplos que el documento original no incluye. Es un punto de
partida para la calibración, no una versión definitiva.

### 3.1 Dimensiones analíticas (multi-etiqueta a nivel de párrafo/fragmento)

| Dimensión | Definición operativa | Regla de decisión | Marcadores típicos |
|---|---|---|---|
| **Estado de situación** | Describe QUÉ está pasando (impactos, vulnerabilidad, riesgos observados), sin explicar causas | Si el fragmento describe un fenómeno/impacto sin atribuir causa estructural → esta etiqueta | Datos, estadísticas, "los impactos observados son...", "la vulnerabilidad es mayor en..." |
| **Diagnóstico estructural** | Explica POR QUÉ ocurre lo anterior, atribuyendo el fenómeno a factores estructurales (modelo productivo, matriz energética, institucionalidad, desigualdad) | Si hay conector causal ("debido a", "esto se explica por", "producto de") ligando el fenómeno a un factor sistémico → esta etiqueta. Puede coexistir con "estado de situación" en el mismo párrafo | Atribución causal, referencia a modelo de desarrollo/estructura productiva |
| **Propuestas e instrumentos de política** | Recomendaciones o instrumentos concretos (leyes, fondos, impuestos al carbono, taxonomías, planes) | Verbo prescriptivo ("se recomienda", "es necesario", "debería") + sustantivo de instrumento | Nombra un instrumento específico o una acción recomendada |
| **Avances de implementación** | Evidencia de una acción/política YA implementada con resultado observado | Verbo en pasado/presente perfecto + país/territorio + resultado | "Chile implementó...", "se ha logrado..." |
| **Brechas de implementación** | Ausencia, insuficiencia o falla respecto de algo que se esperaría dado un compromiso o política ya anunciada | Requiere referencia (explícita o implícita) a una política/compromiso previo que no se cumplió | "pese a los compromisos NDC, persiste...", "no se ha traducido en..." |
| **Tendencias** | Patrón de evolución temporal 2015–2025 | Comparación explícita o implícita entre períodos | "ha aumentado", "se observa una consolidación de..." |
| **Desafíos** | Obstáculo estructural o futuro para la acción climática, sin estar atado a una política específica ya intentada (a diferencia de "brecha") | Framing prospectivo/genérico de dificultad, no retrospectivo de una política puntual | "coordinar múltiples niveles de gobierno sigue siendo complejo" |
| **Oportunidades** | Condición favorable o ventana no explotada, framing positivo | Verbo de potencial ("permite", "abre la posibilidad de"), sin ser recomendación prescriptiva concreta (eso sería "propuesta") | "representa una oportunidad para...", "podría catalizar..." |

**Nota de diseño:** estado de situación/diagnóstico y avances/brechas son los pares más propensos a
confusión — por eso llevan regla de decisión explícita y permiten doble etiqueta en vez de forzar
exclusividad.

### 3.2 Variables adicionales

| Variable | Valores | Cómo se resuelve |
|---|---|---|
| **Nivel de aplicación** | Regional (ALC en conjunto) / Nacional / Subnacional (territorio, ciudad, sector) | Se toma el nivel más específico mencionado; multi-tag si el fragmento cubre varios |
| **Cobertura geográfica** | Lista cerrada: 33 países ALC + subregiones (Centroamérica, Caribe, Cono Sur, Andina) + "regional" | Se resuelve técnicamente vía extracción de entidades (NER); requiere solo que el equipo del curso confirme la lista de valores |
| **Tipo de instrumento** (solo si la dimensión es "propuestas") | Planificación / Regulación / Financiamiento / Gobernanza / Información-monitoreo | Es la taxonomía más débil hoy — requiere confirmación del equipo del curso |

## 4. Muestra de calibración (14 documentos)

Seleccionada de `documentos_definitivos_trazabilidad.csv` (244 docs) con tres criterios de
representatividad: (a) cobertura de los tres períodos usados en el PPT de coocurrencias
(2015–2018, 2019–2022, 2023–2026), (b) diversidad de división/oficina (para capturar variación de
nivel nacional vs. subregional), y (c) mezcla de origen (`corpus_original` vs. `agregado_fase2`,
para probar el codebook también en los documentos estratégicos/institucionales).

| # | Año | Período | División | Origen | Título | Handle |
|---|---|---|---|---|---|---|
| 1 | 2015 | 2015–2018 | Desarrollo Sostenible y AA.HH. | corpus_original | Efectos del cambio climático en la costa de América Latina y el Caribe: dinámicas, tendencias... | [11362/3955](https://hdl.handle.net/11362/3955) |
| 2 | 2015 | 2015–2018 | Desarrollo Sostenible y AA.HH. | corpus_original | Ocho tesis sobre el cambio climático y el desarrollo sostenible en América Latina | [11362/39840](https://hdl.handle.net/11362/39840) |
| 3 | 2017 | 2015–2018 | Desarrollo Económico | corpus_original | The rise of green bonds: Financing for development in Latin America and the Caribbean | [11362/42230](https://hdl.handle.net/11362/42230) |
| 4 | 2017 | 2015–2018 | México (subregional) | corpus_original | Economía del Cambio Climático en Honduras: documento técnico 2017 | [11362/42355](https://hdl.handle.net/11362/42355) |
| 5 | 2017 | 2015–2018 | CEPAL - SE - Institucional | agregado_fase2 | Informe anual sobre el progreso y los desafíos regionales de la Agenda 2030... | [11362/41173](https://hdl.handle.net/11362/41173) |
| 6 | 2020 | 2019–2022 | Desarrollo Sostenible y AA.HH. | corpus_original | La tragedia ambiental de América Latina y el Caribe | [11362/46101](https://hdl.handle.net/11362/46101) |
| 7 | 2019 | 2019–2022 | Desarrollo Sostenible y AA.HH. | corpus_original | Cuarto informe sobre financiamiento para el cambio climático en América Latina y el Caribe | [11362/44487](https://hdl.handle.net/11362/44487) |
| 8 | 2021 | 2019–2022 | Recursos Naturales | corpus_original | Reflexiones sobre la gestión del agua en América Latina y el Caribe | [11362/46792](https://hdl.handle.net/11362/46792) |
| 9 | 2022 | 2019–2022 | Puerto España (subregional) | corpus_original | Building a climate resilient power sector in the context of the Caribbean small island developing states | [11362/48603](https://hdl.handle.net/11362/48603) |
| 10 | 2022 | 2019–2022 | CEPAL - SE - Institucional | agregado_fase2 | Una década de acción para un cambio de época. Quinto informe sobre el progreso... | [11362/47745](https://hdl.handle.net/11362/47745) |
| 11 | 2025 | 2023–2026 | Desarrollo Sostenible y AA.HH. | corpus_original | El impacto del cambio climático en la pobreza infantil y juvenil de América Latina | [11362/82426](https://hdl.handle.net/11362/82426) |
| 12 | 2023 | 2023–2026 | Recursos Naturales | corpus_original | Acción climática en la agricultura: la experiencia de países miembros de la Plataforma... | [11362/48724](https://hdl.handle.net/11362/48724) |
| 13 | 2023 | 2023–2026 | México (subregional) | corpus_original | Comercio, cambio climático y el impuesto fronterizo al carbono | [11362/68639](https://hdl.handle.net/11362/68639) |
| 14 | 2024 | 2023–2026 | CEPAL - SE - Institucional | agregado_fase2 | América Latina y el Caribe ante las trampas del desarrollo: transformaciones indispensables | [11362/80727](https://hdl.handle.net/11362/80727) |

## 5. Próximos pasos

1. Enviar esta propuesta (secciones 3 y 4) al equipo del curso.
2. Pedir el groundtruth: clasificación manual independiente de los 14 documentos de la muestra por
   el equipo del curso, usando sus propias definiciones de cada dimensión y variable.
3. Lab corre el codebook v0 vía IA sobre la misma muestra a nivel de párrafo.
4. Reunión de calibración: comparar resultados, afinar definiciones, reglas de decisión y palabras
   clave por pregunta de investigación.
5. Escalar el pipeline calibrado a los 244 documentos del corpus definitivo.

## 6. Housekeeping del repositorio (2026-07-06)

En el marco de esta sesión se hizo limpieza del repositorio:

- Se corrigieron dos archivos trackeados por error: `~$datos_dashboard_final.xlsx` (lock file de
  Excel) y `seleccion_revision.json` (que CLAUDE.md ya documentaba como ignorado, pero no lo
  estaba). Se agregaron reglas `~$*`, `*.7z` y `seleccion_revision.json` al `.gitignore`.
- Se eliminaron ~17 scripts sueltos de exploración/depuración de la construcción del corpus de
  Fase 1 (`debug_*`, `investigar_*`, `test_*`, `recap_segunda_fase.py`, `agregar_*`,
  `analizar_documentos_a_agregar.py`, `explorar_datos.py`, `generar_listado_depurado.py`,
  `normalizar_topic_spa.py`, `validar_datos_segunda_fase.py`, `verificar_documentos_correctos.py`,
  `verificar_por_que_no_en_base.py`, `verificar_topics_agregados.py`, `temp_output.txt`,
  `listado_depurado.csv`), que no estaban referenciados en ninguna documentación y quedaron
  obsoletos tras el refactor de `datos.py`/`segunda_fase.py`. Se conservaron los 4 scripts que sí
  están citados como verificación documentada (`listar_excluidos.py`, `verificar_sustantivos.py`,
  `verificar_busqueda.py`, `verificar_documentos.py`).
- Se agregaron al control de versiones los entregables ya generados en sesiones previas:
  `coocurrencias_periodos.pptx`, `generar_pptx_cocurrencias.py`, `generar_trazabilidad.py`,
  `documentos_definitivos_trazabilidad.csv` y `nota_conceptual.docx`.
- **Pendiente, no resuelto en esta sesión:** `SEGUNDA_FASE.md` y `DOCUMENTOS_EXCLUIDOS_DEFINITIVO.md`
  referencian funciones que ya no existen en el código actual (`excluir_documentos`,
  `agregar_documentos`, `buscar_documento_inteligente` vs. las actuales `_excluir_documentos`,
  `cargar_documentos_definitivos`, `DOCUMENTOS_A_AGREGAR` en `datos.py`/`segunda_fase.py`). Quedan
  desactualizados tras el refactor y conviene revisarlos aparte.
- Hay cambios sin commitear en `datos.py`, `explorador.py`, `segunda_fase.py`, `visualizaciones.py`
  y `requirements.txt` (refactor de la vista de segunda fase, nueva dependencia `adjustText`) que no
  se tocaron en esta sesión por ser trabajo en curso ajeno a este análisis.
