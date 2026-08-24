# Resultados canónicos

Este directorio separa los productos analíticos de los artefactos auxiliares de Fase 2.

| Ruta | Contenido |
| --- | --- |
| `json/` | Resultados analíticos canónicos: un `doc_<id>.json` por publicación de producción. |
| `certificados/` | Certificados de promoción disponibles, con nombre `doc_<id>.validation.json`. |
| `archivo/` | Borradores u otros artefactos no canónicos que se conservan por trazabilidad. |

Los JSON de `json/` son la materia prima de Fase 3. La ausencia de un certificado no invalida los resultados históricos producidos antes de que esa compuerta se incorporara al pipeline. El inventario y el estado operativo se verifican contra el ledger y `documentos_definitivos_trazabilidad.csv`, no contando archivos de forma aislada.
