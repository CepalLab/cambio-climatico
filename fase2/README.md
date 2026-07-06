# Fase 2 — Análisis estructurado del corpus climático

**Fecha de inicio**: 2026-07-06
**Estado**: Propuesta v0, pendiente de validación con el equipo del curso (Valeria, Santiago Lorenzo/VTL)
**Contexto**: insumo de apoyo al curso "Innovar para la complejidad: Estrategias del sector público
para abordar el cambio climático en América Latina" (Montevideo, 1–4 sept. 2026). Ver
[nota_conceptual.docx](nota_conceptual.docx) para el documento original del equipo del curso.

Esta carpeta reúne el trabajo de la Fase 2: pasar del corpus de 244 documentos (construido en
Fase 1, ver [../SEGUNDA_FASE.md](../SEGUNDA_FASE.md) y
[../DOCUMENTOS_EXCLUIDOS_DEFINITIVO.md](../DOCUMENTOS_EXCLUIDOS_DEFINITIVO.md)) a un análisis
estructurado a nivel de fragmento, guiado por las preguntas de investigación de la nota conceptual.

Contenido:
- [codebook_v0.md](codebook_v0.md) — propuesta de codificación (dimensiones analíticas y variables).
- [muestra_calibracion.csv](muestra_calibracion.csv) — 14 documentos seleccionados para calibrar el
  codebook antes de escalar a los 244.

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
[../SEGUNDA_FASE.md](../SEGUNDA_FASE.md), [../DOCUMENTOS_EXCLUIDOS_DEFINITIVO.md](../DOCUMENTOS_EXCLUIDOS_DEFINITIVO.md)
y `../documentos_definitivos_trazabilidad.csv`). Lo que sí depende del dominio —la Fase 2
propiamente— no se puede automatizar a ciegas justamente por estas indefiniciones. La salida
práctica: construir un codebook borrador con la propia terminología de la nota, probarlo en una
muestra chica, y usar ese artefacto concreto para forzar la precisión conceptual que falta.

## 2. Intercambio con Valeria (2026-07-06)

Valeria pidió avanzar a Fase 2: pasar de documento completo a fragmentos codificados por dimensión
analítica, agregar variables de nivel de aplicación y cobertura geográfica, y traducir las 8
preguntas de investigación en criterios de búsqueda (keywords + filtros). El pedido delega buena
parte de las decisiones de contenido ("todas las sugerencias son bienvenidas, ustedes son los
expertos") al Lab, que aporta la capacidad técnica pero no la experticia de dominio en política
climática — esa le corresponde al equipo del curso.

**Respuesta acordada:** en vez de diseñar los criterios de búsqueda para las 244 publicaciones de
una vez, se propuso:

1. Lab construye una primera propuesta de codificación ([codebook_v0.md](codebook_v0.md)) y la
   aplica sobre una muestra acotada ([muestra_calibracion.csv](muestra_calibracion.csv)).
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

## 3. Próximos pasos

1. Enviar [codebook_v0.md](codebook_v0.md) y [muestra_calibracion.csv](muestra_calibracion.csv) al
   equipo del curso.
2. Pedir el groundtruth: clasificación manual independiente de los 14 documentos de la muestra por
   el equipo del curso, usando sus propias definiciones de cada dimensión y variable.
3. Lab corre el codebook v0 vía IA sobre la misma muestra a nivel de párrafo.
4. Reunión de calibración: comparar resultados, afinar definiciones, reglas de decisión y palabras
   clave por pregunta de investigación.
5. Escalar el pipeline calibrado a los 244 documentos del corpus definitivo.

## Historial

- **2026-07-06** — creación de esta carpeta, codebook v0 y muestra de calibración; housekeeping de
  archivos sueltos en la raíz del repo (ver commit `945ebda` y siguientes).
