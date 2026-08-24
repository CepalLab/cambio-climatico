# Cierre de prefase 3

**Fecha:** 2026-08-24

## Decisión

La prefase 3 queda cerrada operativamente. El proyecto puede avanzar al análisis agregado exploratorio y al análisis de contenido sin modificar los JSON canónicos de Fase 2.

La versión de trabajo es v1. Los refinamientos posteriores se incorporarán como versiones nuevas y no invalidan la trazabilidad existente.

## Avances

- Se consolidó el manifiesto histórico de 244 documentos.
- Se definió el corpus activo de 238 documentos tras 6 exclusiones aplicadas.
- Se verificaron handles únicos, correspondencia con el CSV y hashes de los JSON fuente.
- Se cerró la auditoría transversal: 0 anomalías estructurales.
- Se documentaron y aceptaron 11 alertas heurísticas de paginación.
- Se conservaron las dimensiones y citas auditadas: 7.812 secciones y 8.329 dimensiones/citas.
- Se definió la normalización de tipos documentales y de ámbitos regional, subregional, nacional, subnacional y multinivel.
- Se construyó una capa SQLite para consultas y agregados.
- Se generó el primer EDA descriptivo reproducible.
- Se ordenó físicamente `fase3` en control, normalización, EDA y análisis de contenido.

## Cambios principales

- Los JSON canónicos de `fase2` siguen siendo la fuente de evidencia y retrieval.
- La normalización v1 conserva valores originales, candidatos, métodos, estados y hashes.
- SQLite aplana secciones anidadas con relaciones padre-hijo y mantiene dimensiones, citas, interpelación y tipología.
- Se separaron los niveles `regional` y `subregional`.
- `multinivel` se reserva para documentos con escala subnacional explícita combinada con escala nacional u otra escala superior.
- La autoría, los países, sectores, organizaciones y ámbitos se modelan como relaciones revisables.

## Productos de trabajo

- `00_control/inventario/`
- `00_control/auditorias/`
- `00_control/revisiones/`
- `01_normalizacion/salidas/`
- `01_normalizacion/revision/`
- `02_eda/salidas/fase3_analitica_v1.sqlite`
- `02_eda/salidas/eda_descriptivo_v1.md`
- `02_eda/salidas/eda_descriptivo_v1.json`

## Pendientes no bloqueantes

- La cola de normalización contiene 2.668 pendientes: autoría, organizaciones, países, sectores, subregiones, ámbitos y tipos documentales.
- Existen 84 documentos sin tipo documental normalizado en v1; se reportan como `Sin clasificar`.
- Las relaciones geográficas y sectoriales son candidatas, no codificación experta definitiva.
- La auditoría heurística de dimensiones conserva 44 candidatos para revisión semántica posterior.
- Debe desarrollarse el análisis de preguntas de investigación, patrones del diagnóstico CEPAL, evolución de enfoques y gobernanza multinivel.

## Controles de cierre

- Documentos SQLite: 238.
- Relaciones SQLite: 2.292.
- Secciones SQLite: 7.812.
- Dimensiones SQLite: 8.329.
- Tipologías SQLite: 238.
- Referencias relacionales inválidas: 0.
- Hashes de origen discrepantes: 0.
- Idempotencia: confirmada.
- Scripts reorganizados: sin errores de análisis.

## Próximo ciclo

El análisis debe declarar siempre la versión `fase3-analitica-v1`, el denominador de 238 documentos activos, las 6 exclusiones aplicadas, los filtros utilizados y la naturaleza candidata de las relaciones geográficas y sectoriales.
