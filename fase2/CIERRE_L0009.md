# Cierre L0009

**Fecha de cierre:** 2026-08-19  
**Nombre:** `lote-09-preflight`  
**Estado:** completado  
**Documentos:** 15/15 promovidos y aprobados

## Resultado

Los 15 borradores se revalidaron de forma independiente antes de promoción. Cada resultado canónico conserva
un certificado gemelo con hashes SHA-256 del JSON, índice y fuente paginada. El corpus queda con **153 aprobados**
y **91 pendientes**.

## Hallazgos

- `11362/47534`: borrador y reportes sincronizados; 57/57 citas.
- `11362/47604`: citas y páginas corregidas; 38/38 citas.
- `11362/46996`: título normalizado.
- `11362/47730`: alerta histórica de cobertura (6/57 hojas sustantivas cubiertas); pasó las compuertas de L0009,
  pero la cobertura es bloqueante desde L0010.

## Compuertas desde L0010

1. `auditar_pre_promocion.py` bloquea basura, mojibake, controles y espacios no canónicos en títulos.
2. La cobertura de hojas sustantivas se bloquea con `--strict-coverage`.
3. `certificar_promocion.py` sella hashes; `ledger.py complete` rechaza resultados sin certificado válido.
