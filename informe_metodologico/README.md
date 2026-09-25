# Reporte metodológico — de la nota conceptual al borrador y los exploradores

**Estado:** planificación / scaffolding. Nada aquí es contenido final.
**Fecha de apertura:** 2026-09-25.
**Productos del proyecto:** (1) borrador ✅ concluido → (2) reporte metodológico (este) → (3) nuevo visualizador de hallazgos (sesión aparte; reemplaza al Streamlit, que queda como legacy).

## Decisiones (2026-09-25)

1. **Audiencia y largo:** versión interna, concisa; servirá de base para una nota del laboratorio en el landing.
2. **Costos:** estimar desde el usage de los proveedores con fecha de uso (rastrear por fecha).
3. **Visualizador nuevo:** reemplaza al Streamlit (legacy queda); su spec/diseño va en sesión aparte, no en este reporte.
4. **Orden de redacción:** primero caps 01–05.

## Qué es esto

Relato reproducible de todo el proceso: nota conceptual → selección de documentos → iteración con expertos → taxonomías → extracción/enriquecimiento con modelos (calibración, revisiones, costos) → normalización/EDA → síntesis → borrador → explorador Streamlit (+ spec del visualizador nuevo).

## Cómo trabajar aquí

1. `ESTRUCTURA_REPORTE.md` = outline canónico (12 capítulos + anexos). No cambiar el orden sin decisión explícita.
2. `FUENTES.md` = registro de fuentes existentes y faltantes por capítulo.
3. `capitulos/*.md` = stubs de trabajo, uno por capítulo. Cada stub trae: propósito, fuentes, preguntas a resolver y estado.
4. Reglas heredadas: no reescribir JSON canónicos de Fase 2, no descartar árbol de Fase 3, `git diff --check` limpio antes de cada commit.

## Orden de ejecución sugerido

1. Consolidar capítulos con fuente abundante (01–05: nota, corpus, expertos, taxonomías, calibración).
2. Reconstruir pipeline y operación (06–07) desde prompts, ledger y bitácoras.
3. Levantar datos faltantes: costos Gemini, tiempos, spec visualizador nuevo (08, 11).
4. Cerrar con normalización/EDA, síntesis/borrador y límites/lecciones (09, 10, 12 + anexos).
