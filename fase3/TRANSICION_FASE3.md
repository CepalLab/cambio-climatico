# Transición operativa a Fase 3

## Estado al 2026-08-27

La Fase 3 completó el análisis de contenido y la integración editorial del
informe maestro v2. El universo activo es de 238 documentos: 244 históricos
menos 6 exclusiones aplicadas. El informe cubre 2015–2026 y el período más
reciente incluye seis publicaciones fechadas en 2026.

La fuente canónica son los JSON de Fase 2. Los derivados v1 no los reemplazan.
El punto de reanudación es
[03_analisis_contenido/CHECKPOINT_FASE3_3_2026-08-27.md](03_analisis_contenido/CHECKPOINT_FASE3_3_2026-08-27.md).
Los productos vigentes son el
[informe maestro v2](03_analisis_contenido/INFORME_MAESTRO_V2_BORRADOR.md),
el [anexo técnico](03_analisis_contenido/ANEXO_TECNICO_INFORME_V2.md), cinco
figuras reproducibles y cuatro cuadros. El trabajo pendiente es revisión humana
final y producción de una versión de circulación en el formato que defina el
equipo.

## Capas de trabajo

- JSON canónicos: documento completo, estructura, citas y evidencia.
- `01_normalizacion/salidas/normalizacion_corpus_activo_v1.json`: candidatos de normalización con valores originales.
- `01_normalizacion/salidas/corpus_activo_normalizado_v1.json`: documentos y relaciones operativas.
- `02_eda/salidas/fase3_analitica_v1.sqlite`: capa tabular para consultas y agregados.
- `02_eda/salidas/eda_descriptivo_v1.json` y `.md`: EDA reproducible.
- `01_normalizacion/revision/cola_revision_metadatos_v1.csv`: refinamientos que no bloquean el análisis v1.

## Controles ejecutados

- 238 documentos únicos.
- 2.292 relaciones normalizadas candidatas.
- 7.812 secciones.
- 8.329 dimensiones/citas.
- 952 registros de interpelación.
- 238 tipologías.
- 0 referencias relacionales inválidas.
- 0 discrepancias de hash respecto de los JSON fuente.
- Idempotencia de construcción confirmada.

## Lectura del EDA

Los conteos de países, sectores y subregiones se basan en relaciones candidatas v1. No deben presentarse todavía como codificación experta definitiva. Los 84 documentos sin tipo documental normalizado se mantienen como `Sin clasificar`.

## Comandos reproducibles

```powershell
& .venv/Scripts/python.exe fase3/01_normalizacion/scripts/normalizar_metadatos.py --limit 0 --output fase3/01_normalizacion/salidas/normalizacion_corpus_activo_v1.json --review-output fase3/01_normalizacion/revision/cola_revision_metadatos_v1.csv
& .venv/Scripts/python.exe fase3/01_normalizacion/scripts/aplicar_normalizacion_muestra.py --input fase3/01_normalizacion/salidas/normalizacion_corpus_activo_v1.json --output fase3/01_normalizacion/salidas/corpus_activo_normalizado_v1.json
& .venv/Scripts/python.exe fase3/02_eda/scripts/construir_base_analitica.py
& .venv/Scripts/python.exe fase3/02_eda/scripts/generar_eda_v1.py
```

## Estado y próximos pasos

La siguiente sesión no debe reiniciar las capas analíticas. Debe:

1. Revisar humanamente el informe maestro v2, con énfasis en tono, prioridades
   y adecuación de las figuras para circulación.
2. Definir el formato de entrega, por ejemplo Word o PDF.
3. Preparar portada, índice y estilo institucional sin cambiar evidencia,
   citas ancla ni límites metodológicos.
4. Revisar el árbol de trabajo completo antes de un commit: existen cambios
   acumulados de normalización, EDA y análisis que no deben descartarse.

Cada producto analítico debe declarar versión de la base, denominador, filtros, exclusiones y limitaciones.
