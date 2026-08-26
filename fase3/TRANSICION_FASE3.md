# Transición operativa a Fase 3

## Estado al 2026-08-24

La Fase 3 está lista para análisis agregado exploratorio y para comenzar el análisis de contenido. El universo activo es de 238 documentos: 244 históricos menos 6 exclusiones aplicadas.

La fuente canónica son los JSON de Fase 2. Los derivados v1 no los reemplazan.

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

## Próxima capa analítica

El estado consolidado de la Fase 3.3, incluidos artefactos, validaciones y
comandos de reanudacion, esta en
[03_analisis_contenido/CHECKPOINT_FASE3_3_2026-08-26.md](03_analisis_contenido/CHECKPOINT_FASE3_3_2026-08-26.md).

La Fase 3.3 inicia con el contrato documentado en
[03_analisis_contenido/ESPECIFICACION_ANALITICA_v2.md](03_analisis_contenido/ESPECIFICACION_ANALITICA_v2.md).
El informe de 30 páginas es el camino crítico; el activo analítico vivo y el
grafo son derivados incrementales del mismo trabajo de evidencia.

1. Crear formatos de preguntas, conceptos, hallazgos, decisiones y grafo.
2. Construir paquetes de evidencia reproducibles por pregunta.
3. Ejecutar los pilotos de evolución de enfoques y gobernanza multinivel.
4. Estabilizar el protocolo y responder las nueve preguntas de investigación.
5. Redactar el informe y habilitar el visor de evidencia y relaciones.
6. Refinar en paralelo relaciones y generar versiones posteriores cuando
	corresponda.

Cada producto analítico debe declarar versión de la base, denominador, filtros, exclusiones y limitaciones.
