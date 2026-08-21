# Revisión de control — primeros 3 documentos de L0001

**Fecha:** 2026-08-05  
**Decisión:** no continuar con los 12 documentos restantes hasta corregir y reejecutar estos tres casos.

| Handle | Extracción | Validador estructural | Citas contrastables | Decisión |
| --- | --- | ---: | ---: | --- |
| `11362/37791` | Legible, 455.559 bytes | 6 observaciones | 20/36 | Rehacer desde enriquecimiento: faltan cobertura proporcional y dieciséis citas no pasan la comprobación literal automatizada. |
| `11362/37910` | Ilegible, 111.019 caracteres de control | 11 observaciones | 0/15 | Rehacer desde adquisición/extracción con OCR o lectura nativa; el índice y las citas generados no son confiables. |
| `11362/37911` | Insuficiente, 1.002 caracteres útiles para 100 páginas | 7 observaciones | 0/13 | Rehacer desde adquisición/extracción con OCR o lectura nativa; además se inventaron metadatos y estructura. |

## Hallazgos transversales

- Los tres JSON suman 24 observaciones del validador; ninguno puede aceptarse como resultado canónico.
- El harness continuó pese a extracciones inutilizables y completó vacíos con contenido plausible pero no sustentado.
- Los TXT del endpoint cercanos a 100.000 caracteres deben considerarse truncados y reemplazarse por lectura del PDF completo; esta compuerta queda incorporada al ledger.
- Los archivos no respetaron `doc_<handle_id>.json`, por lo que antes escapaban del descubrimiento automático del validador.
- Los intentos registraron modelo `claude`, cero tokens y costo cero: esa trazabilidad no permite identificar la configuración ni evaluar economía.
- `num_muestra` usó 1, 2 y 3 (posición del lote) en vez de los `corpus_order` estables 2, 4 y 5.

## Estado operativo

Los tres resultados fueron retirados de `corpus/resultados/`, conservados localmente como `rechazado_revision1.json` dentro de sus carpetas de intermedios y marcados `error_retryable` en el ledger. `11362/37791` retoma desde `extraction`; `11362/37910` y `11362/37911`, desde `acquisition`.

La reejecución solo se acepta si: la extracción supera la compuerta de calidad; metadatos e índice se copian de fuentes verificables; todas las citas son literales; el validador termina sin observaciones; el nombre final es exacto; y modelo, harness, tokens y costo se registran con valores reales cuando estén disponibles.
