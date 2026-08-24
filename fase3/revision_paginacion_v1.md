# Revisión de paginación v1

**Fecha:** 2026-08-24
**Alcance:** alertas de paginación de la validación exhaustiva del esquema v1.

## Criterio de esta fase

Se conserva un rango de página aproximado y reproducible. No se intenta reconciliar de forma exhaustiva la página impresa del PDF, el contador del visor ni la paginación del TXT. Una alerta solo se corrige si demuestra que la cita está fuera del cuerpo del documento o carece de anclaje.

## Resultado

Se revisaron los **11 avisos** relacionados con paginación:

- **7** alertas de ítems del desglose fuera del rango heurístico de recomendaciones.
- **4** alertas de retroceso en el orden de rangos de subsecciones.
- **0** correcciones de JSON.
- **11** casos aceptados como `mantener`.

### Hallazgos

Las alertas de rango son falsos positivos de la heurística cuando `desglose_items` reúne recomendaciones de varios capítulos o módulos, mientras el validador toma el mínimo y máximo de secciones cuyos títulos contienen palabras como “conclusiones”, “propuesta” o “recomendaciones”.

Los retrocesos son solapamientos normales: una subsección puede comenzar antes de que termine el rango de la subsección anterior. No implican que la página de la cita haya sido modificada o que esté desanclada.

El detalle por documento y la decisión quedan en [revision_paginacion_v1.csv](revision_paginacion_v1.csv).

## Decisión operativa

Los JSON canónicos permanecen sin cambios. Las 11 observaciones de paginación continúan visibles en `validacion_esquema_activo_v1.json` como alertas heurísticas, pero no bloquean el inicio de la normalización. La reconciliación fina de numeración queda diferida a una etapa futura.
