# Resumen del Preflight del Lote L0011

## Tabla resumen de los 15 documentos procesados

| # | Handle | Título | Páginas | Extractor | Score | Layout | Páginas 2col | Requiere OCR | Revisión Visual |
|---|--------|--------|---------|-----------|-------|--------|--------------|--------------|-----------------|
| 1 | 11362/48413 | Acción climática con igualdad de género: hacia una recuperación transformadora para la sostenibilidad y la igualdad de género en América Latina y el Caribe | 156 | pypdf | 77.9 | mixed | 6 (3.8%) | No | No |
| 2 | 11362/48491 | Diagnóstico situacional de los sistemas nacionales de inversión pública: Panamá 2020 | 150 | pypdf | 70.65 | mixed | 26 (17.3%) | No | No |
| 3 | 11362/48524 | Impactos macroeconómicos del cambio climático en América Latina y el Caribe: revisión de la literatura, 2010-2021 | 58 | pypdf | 55.63 | mixed | 24 (41.4%) | No | No |
| 4 | 11362/48541 | Enfoques y prácticas de gobernanza en América Latina y el Caribe para el cambio transformativo a favor de la biodiversidad | 95 | pypdf | 67.41 | mixed | 8 (8.4%) | No | No |
| 5 | 11362/48543 | Experiencias de integración de la biodiversidad en los sectores productivos, económicos y financieros de América Latina y el Caribe | 88 | pypdf | 71.05 | mixed | 7 (8.0%) | No | No |
| 6 | 11362/48555 | Potential trade implications of Latin America and the Caribbean’s climate commitments under the Paris Agreement | 45 | pypdf | 58.27 | mixed | 9 (20.0%) | No | No |
| 7 | 11362/48611 | Diagnóstico situacional de los sistemas nacionales de inversión pública: Nicaragua 2020 | 122 | pypdf | 71.37 | mixed | 21 (17.2%) | No | No |
| 8 | 11362/48736 | Diagnóstico situacional de los sistemas nacionales de inversión pública: Honduras 2020 | 151 | pypdf | 71.18 | mixed | 28 (18.5%) | No | No |
| 9 | 11362/48880 | Costos asociados a la inacción frente al cambio climático en Chile: síntesis | 75 | pypdf | 61.67 | mixed | 14 (18.7%) | No | No |
| 10 | 11362/48901 | Estudo comparativo sobre normas e critérios de patenteabilidade de invenções biotecnológicas. Sumário executivo | 60 | pypdf | 59.65 | mixed | 25 (41.7%) | No | No |
| 11 | 11362/48958 | Advancing geospatial information management for disaster risk management in the Caribbean | 59 | pypdf | 59.69 | mixed | 9 (15.3%) | No | No |
| 12 | 11362/49053 | Estándares y certificaciones internacionales voluntarias en materia de minería sostenible en los países andinos | 88 | pypdf | 72.96 | mixed | 16 (18.2%) | No | No |
| 13 | 11362/67979 | Los efectos del cambio climático en la actividad económica de América Latina y el Caribe: una perspectiva empírica | 57 | pypdf | 57.0 | mixed | 8 (14.0%) | No | No |
| 14 | 11362/68644 | Modelo conceptual para integrar la reducción del riesgo de desastres y la adaptación sostenible e incluyente al cambio climático en la inversión pública | 50 | pypdf | 65.75 | mixed | 10 (20.0%) | No | No |
| 15 | 11362/68648 | Análisis de vulnerabilidad agrícola al cambio climático para la región del Sistema de la Integración Centroamericana (SICA) | 124 | pypdf | 60.7 | mixed | 25 (20.2%) | No | No |

## Estadísticas resumen

- **Total de documentos**: 15
- **Total de páginas**: 1,328
- **Extractor utilizado**: pypdf (todos los documentos)
- **Score promedio**: 65.7 (rango: 55.63 – 77.9)
- **Layout detectado**: mixed (todos los documentos)
- **Páginas en dos columnas promedio**: 16.1 por documento (15.9% del total)
- **Requieren OCR**: 0 documentos
- **Requieren revisión visual**: 0 documentos

## Archivos generados por documento

Cada documento tiene en `corpus/intermedios/11362/<id>/`:
- `texto.txt` — texto del endpoint
- `preflight_endpoint.json` — diagnóstico reproducible del endpoint text
- `tramos/` — tramos extraídos del PDF
  - `preflight.json` — diagnóstico del PDF
  - `tramo_*.txt` — fragmentos de texto
- `PREPARACION_FUENTE.md` — documento de preparación de fuente

## Observaciones

1. **Endpoint text no utilizable para citas**: Todos los documentos requirieron fallback a PDF porque el endpoint text no contiene saltos de página utilizables, es demasiado breve o está truncado.
2. **Layout mixto**: Todos los documentos tienen layout mixto (una combinación de páginas de una y dos columnas).
3. **Calidad de extracción**: Los scores varían entre 55.63 y 77.9, indicando calidad variable pero aceptable para análisis.
4. **No requieren OCR**: Ningún documento requiere reconocimiento óptico de caracteres.
5. **No requieren revisión visual**: Ningún documento requiere revisión visual adicional.

## Harness
- **Herramienta**: MiMo/OpenCode
- **Modelo**: no registrado (modelo no expuesto en sesión)

---
*Generado: 2026-08-20*
