# Verificación de reproducibilidad de paquetes v1

**Fecha:** 2026-08-27  
**Base:** `fase3-analitica-v1`, 238 documentos activos y 6 exclusiones.

## Resultado

La regeneración de los paquetes de evolución de enfoques y gobernanza se ejecutó contra la misma base SQLite actual. Ambos declaran el SHA-256 `2b8ffd2bab1942e84701f32f69c90e8fa725fb3ba5581e600fc55cf11f73c8e0`, que coincide con el hash físico de `fase3/02_eda/salidas/fase3_analitica_v1.sqlite`.

Ambos paquetes declaran `year_range` 2015–2026 y P3 como 2023–2026. Las métricas de coherencia entre propuestas, avances y brechas se mantienen: propuestas 92/99, 74/75 y 63/64; avances 61,6%, 66,7% y 71,9%; brechas 59,6%, 76,0% y 70,3%.

## Alcance

Esta verificación cierra la discrepancia de hashes y metadato temporal señalada en la auditoría de fichas. No aprueba todavía FE-02 ni FE-03: ambas conservan revisión humana pendiente.
