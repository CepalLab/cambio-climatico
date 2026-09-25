# Estructura del reporte metodológico (canónica v0)

12 capítulos + anexos. Cada capítulo → `capitulos/NN_*.md`.

## 00 Resumen ejecutivo y ficha técnica
Qué se hizo, con qué corpus, con qué modelos, qué salió (borrador + explorador), límites en una página. Ficha: corpus 244→238, período 2015–2026, modelos, validadores, hashes de congelamiento.

## 01 Mandato y nota conceptual
Curso Montevideo (1–4 sept 2026), 9 preguntas P1–P9, 6 etapas propuestas, ambigüedades detectadas (solapamientos P1/P2, unidad de análisis, taxonomías abiertas, sin protocolo de validación). Fuente: `nota_conceptual.docx`, `fase2/README.md` §1.

## 02 Selección y construcción del corpus
Filtro `cepal.topicSpa` = cambio climático, exclusiones (duplicados, administrativos, revistas, accesibles), 14 agregados de Períodos de Sesiones/Foro, trazabilidad 244→238 con 6 exclusiones. Fuentes: `SEGUNDA_FASE.md`, `DOCUMENTOS_EXCLUIDOS_DEFINITIVO.md`, `documentos_definitivos_trazabilidad.csv`, `segunda_fase.py`, `datos.py`.

## 03 Iteración con expertos
Valeria (alcance Fase 2), Santiago Lorenzo (validación experta), equipo del curso (groundtruth muestra, confirmación 3 reglas Ronda 9), directriz de no-suplantar experticia de dominio. Fuentes: `fase2/README.md` §2, `para_equipo_curso/`, `MEMO_CALIBRACION_RONDA9.md`.

## 04 Taxonomías y codebook
codebook v0 (7 dimensiones + contexto), esquema_json_v1 (reglas 1–9), tipología (11 Grandes Transformaciones, primaria/secundaria), interpelación (4 criterios + modos de falla + umbral mayoría), big_push.md, casos ancla. Fuentes: `fase2/codebook_v0.md`, `TIPOLOGIA_v0.md`, `INTERPELACION_v0.md`, `esquema_json_v1.md`.

## 05 Calibración
Muestra 14→17, rondas 1–9, cambio párrafo→apartado, revisor ciego (prompt agnóstico), adjudicación 66%→85%, 3 reglas confirmadas mismo día. Fuentes: `PLAN_ANALISIS_PROFUNDO.md`, `PROMPT_SESION_REVISOR_CIEGO.md`, `pilot/revision/ADJUDICACION_RONDA9.md`, `INSTRUCCIONES_REVISOR_EXTERNO.md`.

## 06 Pipeline de extracción y enriquecimiento
Modelos (gemini-3.7-flash default, 2.5-pro en bitácoras), harness Gemini CLI (`--yolo`, aislamiento de sesión), prompts versionados por documento (`temp_prompt_*`, `PROMPT_*`), flujo extensos (índice→mapa→parciales→consolidación), PDF nativo vs OCR, tramos, `canonical_fixer.py`. Fuentes: `fase2/GEMINI.md`, `GUIA_OPERATIVA_PIPELINE.md`, `PROMPT_*`, `pipeline/`.

## 07 Operación por lotes y control de calidad
Ledger SQLite recuperable (L0001–L0015), preflight, 4 validadores (esquema, índice, citas literales estrictas, densidad), certificados gemelos, promoción con revisión humana, bitácoras `EJECUCION_ENRIQUECIMIENTO.md`, cierres `CIERRE_L*.md`. Fuentes: `OPERACION_BATCH.md`, `LEDGER_ENRIQUECIMIENTO.md`, `pipeline/ledger.py`, `pipeline/validar_*.py`.

## 08 Costos y tiempos
⚠️ Brecha conocida: `_analisis_costo_sesiones.py` cubre solo Claude Code Ronda 7, NO costos Gemini del enriquecimiento masivo. Levantar: llamadas/sesiones Gemini, tiempos por lote, horas humanas (revisión, adjudicación, auditoría), tabla reproducible. Estado: pendiente de levantamiento.

## 09 Normalización y EDA (Fase 3)
Limpieza metadatos, `fase3_analitica_v1.sqlite`, perfiles documentales, matriz candidata, paneles, tensiones dialécticas, verificación ejes (pérdidas y daños, transición justa, CBDR). Fuentes: `fase3/01_normalizacion/`, `fase3/02_eda/`, `fase3/03_analisis_contenido/scripts/construir_*`.

## 10 Síntesis y borrador
Bloques narrativos → informe maestro v2 (7.600 palabras, 5 figuras reproducibles, 4 cuadros), compuerta revisión, auditoría independiente, congelamiento SHA `500114FB…`, circulación docx/pdf/html. Fuentes: `fase3/03_analisis_contenido/INFORME_MAESTRO_V2_CONGELADO_2026-08-28.md`, `ANEXO_TECNICO_INFORME_V2.md`, `revisiones/`, `CIERRE_FASE3_V2_2026-08-28.md`.

## 11 Exploradores
(a) Streamlit actual: `app.py`, `explorador.py`, `visualizaciones.py`, `revision_piloto.py`, `datos.py`, `seleccion.py` (persistencia GitHub/JSON), deployment Community Cloud. (b) Visualizador nuevo de hallazgos: reemplaza al Streamlit (legacy queda); spec en sesión aparte. Decisión 2026-09-25.

## 12 Límites, decisiones y lecciones
Qué NO se afirma (codificación ≠ experticia definitiva; presencia ≠ adopción/eficacia/causalidad; pérdidas y daños separado; CBDR cualitativo), decisiones registradas, riesgos y recomendaciones de replicabilidad.

## Anexos
A. Cronología (2026-07-06 → 2026-08-28 → hoy). B. Glosario (ledger, preflight, parciales, compuerta, certificado…). C. Inventario de artefactos y dónde viven. D. Prompts canónicos (revisor ciego, consolidación). E. Tabla de costos (cuando exista). F. Hashes y handles de congelamiento.
