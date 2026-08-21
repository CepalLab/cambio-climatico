# Cierre L0012

**Fecha de cierre:** 2026-08-20  
**Nombre:** `lote-12-preflight`  
**Estado:** completado  
**Documentos:** 15/15 promovidos y aprobados

## Resultado

Los 15 documentos se promovieron a `corpus/resultados/` con certificados gemelos SHA-256.
La reconciliación idempotente del ledger deja el corpus con **198 aprobados**, **31 pendientes** y
L0013 reservado en cola.

## Revisión final

- Las 15 unidades superaron esquema, índice jerárquico, orden JSON, citas estrictas y auditoría de
  títulos/cobertura; los tres documentos de 80 o más páginas de cuerpo superaron además cobertura estricta.
- Se verificaron **490 dimensiones**, cada una con cita, y **107 citas** de interpelación: **597 citas**
  literales con página declarada.
- La densidad agregada fue 0,645 citas por página, por encima de L0011 (0,527); no se observó pobreza
  de citas sistémica. `11362/68877`, `11362/69216` y `11362/80433` conservan menor densidad relativa y
  quedan como referencia para revisión cualitativa futura, no como bloqueo.

## Correcciones y decisiones

- `11362/68657`: se restauró la jerarquía literal y se documentaron los aprendizajes de títulos multilínea.
- `11362/68796`: se reparó la jerarquía y las citas afectadas por la lectura a dos columnas.
- `11362/68686` y `11362/68712`: las auditorías semánticas corrigieron citas tangenciales, rótulos de
  tabla/figura y relaciones impropias entre dimensión y evidencia.
- En `11362/68712`, el modo opcional de cobertura estricta marca 0/0 porque su detector de palabras clave
  no clasifica resúmenes en inglés. Se aplicó la política vigente: cobertura estricta para documentos de
  80+ páginas; el documento aprobó las demás compuertas, incluidas 36/36 citas estrictas.
