# Protocolo de documentos extensos y evaluación A/B v1

## Routing desde L0010

- Hasta 80 páginas: alto volumen en `medium`.
- 81–100: parciales contiguos y consolidación separada.
- Más de 100: parciales, `matriz_cobertura.json` por hoja del índice y consolidación en `gpt-5.6-luna/high` si el
  harness lo expone. Si no supera el umbral medido, usar mayor capacidad solo para consolidación/corrección.

La promoción exige `auditar_pre_promocion.py --strict-coverage` y `certificar_promocion.py --strict-coverage`.

## Evaluación A/B

En tres documentos congelados y representativos, ejecutar idénticos tramos, índice, parciales y prompt con
`gpt-5.6-luna/medium` y `gpt-5.6-luna/high`. Medir primera pasada de validaciones, cobertura, títulos limpios,
correcciones, tokens, costo y latencia. Adoptar `high` solo si la mejora es reproducible.
