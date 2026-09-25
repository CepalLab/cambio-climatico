# Registro de fuentes (v0 — 2026-09-25)

Dónde está cada insumo y qué falta. Marcar `[OK]` existente, `[LEVANTAR]` pendiente.

## Existentes por capítulo

- **01 nota:** `[OK]` `nota_conceptual.docx` (raíz), `fase2/README.md` §1, `PLAN_ANALISIS_PROFUNDO.md` §1.5 (9 preguntas).
- **02 corpus:** `[OK]` `SEGUNDA_FASE.md`, `DOCUMENTOS_EXCLUIDOS_DEFINITIVO.md`, `documentos_definitivos_trazabilidad.csv`, `segunda_fase.py`, `datos_dashboard_final.xlsx`.
- **03 expertos:** `[OK]` `fase2/README.md` §2, `fase2/para_equipo_curso/` (nota + 3 anexos + memo Ronda 9). `[LEVANTAR]` fechas/actas de reuniones con equipo del curso si existen fuera del repo.
- **04 taxonomías:** `[OK]` `codebook_v0.md`, `TIPOLOGIA_v0.md`, `INTERPELACION_v0.md`, `esquema_json_v1.md`, `big_push.md`, `CASOS_ANCLA_INTERPELACION_v1.md`.
- **05 calibración:** `[OK]` `PLAN_ANALISIS_PROFUNDO.md` (bitácora rondas), `muestra_calibracion.csv`, `PROMPT_SESION_REVISOR_CIEGO.md`, `pilot/revision/ADJUDICACION_RONDA9.md`, `para_equipo_curso/MEMO_CALIBRACION_RONDA9.md`.
- **06 pipeline:** `[OK]` `GEMINI.md`, `GUIA_OPERATIVA_PIPELINE.md`, `fase2/PROMPT_*.md` + `temp_prompt_*.md` (versionados por doc), `pipeline/*.py`, `ENTORNO_PDF.md`, `PROTOCOLO_LARGOS_Y_AB_v1.md`.
- **07 operación:** `[OK]` `OPERACION_BATCH.md`, `LEDGER_ENRIQUECIMIENTO.md`, `EJECUCION_ENRIQUECIMIENTO.md`, `CIERRE_L*.md`, `RELEVO_FASE3.md`, `pipeline/ledger.py`, `pipeline/validar_*.py`, `corpus/resultados/json/` + `certificados/`.
- **09 normalización/EDA:** `[OK]` `fase3/01_normalizacion/salidas/`, `fase3/02_eda/salidas/fase3_analitica_v1.sqlite`, scripts `construir_*`, `verificar_ejes_canonicos_v1.py`.
- **10 síntesis:** `[OK]` informe congelado + anexo + `revisiones/` + `CIERRE_FASE3_V2_2026-08-28.md` + `MANIFIESTO_CONGELACION*` + `circulacion/`.
- **11 explorador v1:** `[OK]` `app.py`, `explorador.py`, `visualizaciones.py`, `revision_piloto.py`, `datos.py`, `seleccion.py`, `comentarios_piloto.py`, `requirements.txt`, `CLAUDE.md` (despliegue).

## Faltantes (a levantar antes o durante la redacción)

1. **08 costos Gemini:** estimar desde usage de proveedores con fecha de uso (decisión 2026-09-25). Solo existe análisis puntual Claude Code Ronda 7.
2. **08 tiempos:** duración por lote, horas humanas de revisión/adjudicación/auditoría. → pedir bitácoras o estimar con equipo.
3. **11 spec visualizador nuevo:** audiencia, casos de uso, datos fuente, tech stack, relación con Streamlit actual (¿reemplaza/convive?). → requiere decisión del equipo; registrar como capítulo de especificación, no de historia.
4. **03 actas/fechas:** intercambios con Valeria / Santiago / equipo curso fuera de memos. → rescatar mails/actas o declarar solo lo versionado.
5. **06 modelos exactos por lote:** bitácoras mezclan `gemini-3.7-flash` y `gemini-2.5-pro`; normalización a 3.7 Flash declarada en cierres tardíos. → tabla modelo×lote desde bitácoras locales.
6. **10 figuras:** scripts `generar_figuras_informe_v1.py` OK; verificar que `circulacion/` final = figuras del congelamiento.
