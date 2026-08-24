# Fase 3

Fase 3 prepara y analiza el corpus activo de publicaciones sobre cambio climático.

## Estado

La normalización v1 del corpus activo está cerrada operativamente sobre 238 documentos.
Los JSON de Fase 2 permanecen como fuente canónica. Las relaciones normalizadas v1
son derivados y pueden ajustarse mediante nuevas versiones del diccionario.

## Estructura

- `00_control/`: espacio reservado para manifiestos, auditorías, exclusiones y registros.
- `01_normalizacion/`: espacio reservado para scripts, diccionarios, muestras, salidas y revisiones.
- `02_eda/`: base SQLite, scripts y salidas del análisis exploratorio.
- `03_analisis_contenido/`: análisis de preguntas de investigación, patrones y gobernanza multinivel.

Los artefactos históricos de auditoría están agrupados en `00_control`; los documentos
de orientación en la raíz funcionan como puntos de entrada.

## Fuentes y derivados actuales

- `00_control/inventario/inventario_corpus_v1.json`: manifiesto histórico de entrada.
- `00_control/inventario/exclusiones_corpus_v1.csv`: exclusiones aplicadas.
- `01_normalizacion/salidas/corpus_activo_normalizado_v1.json`: metadatos y relaciones normalizadas.
- `01_normalizacion/salidas/normalizacion_corpus_activo_v1.json`: candidatos generados desde los JSON canónicos.
- `01_normalizacion/revision/cola_revision_metadatos_v1.csv`: refinamientos pendientes.
- `02_eda/salidas/fase3_analitica_v1.sqlite`: capa tabular para consultas y agregados.
- `02_eda/salidas/eda_descriptivo_v1.md`: lectura humana del primer EDA.
- `TRANSICION_FASE3.md`: estado, controles y comandos reproducibles.
- `CIERRE_PREFASE3_2026-08-24.md`: acta de cierre y relevo hacia el análisis.

## Convención

Cada salida declara versión, fuentes, denominador y estado de las inferencias.
Los resultados de contenido deben indicar filtros, exclusiones y versión de la base analítica.
