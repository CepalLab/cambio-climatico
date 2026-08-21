# Cierre operativo — L0006

**Fecha de cierre:** 2026-08-17  
**Nombre:** `lote-06-preflight`  
**Resultado:** 15/15 documentos aprobados y promovidos.

## Estado del corpus

- Corpus total: 244 publicaciones.
- Aprobadas y promovidas: 108.
- Pendientes: 136.
- No quedan documentos activos ni ejecuciones para retomar en L0006.

## Documentos promovidos

`44371`, `44472`, `44486`, `44487`, `44584`, `44590`, `44640`, `44970`, `44974`, `45023`, `45046`,
`45066`, `45098`, `45108` y `45111`.

## Método y trazabilidad

- Fuente de todos los documentos: `pdf_tramos` extraídos con PyMuPDF.
- Harness: Gemini CLI.
- Modelo: Gemini 3.7 Flash, confirmado para todo el lote y normalizado en las 15 bitácoras locales.
- Cada documento conserva `PREPARACION_FUENTE.md`, `indice_fuente.json`, borrador, reportes finales y
  `EJECUCION_ENRIQUECIMIENTO.md`.
- El ledger registró los checkpoints `acquisition`, `extraction`, `enrichment` y `validation`, seguidos de
  revisión y aprobación humana.

## Documentos extensos

- `45023`: 5 bloques, 73 secciones jerárquicas, 204/204 citas; 196 dimensiones en 224 páginas de cuerpo,
  densidad 0.88. La alerta de densidad fue revisada y aceptada humanamente.
- `44590`: 7 bloques y consolidación en dos niveles, 163 secciones jerárquicas, 188/188 citas; 184 dimensiones
  en 420 páginas de cuerpo, densidad 0.44.
- Para documentos de más de 80 páginas se mantuvo el flujo índice → mapa de cortes → parciales → consolidación
  → validaciones finales.
- La compuerta `validar_orden_json.py` se incorporó después del cierre de L0006. Los JSON de L0006 conservan
  algunas variantes históricas de orden de claves, sin cambios semánticos; desde L0007 el reporte
  `reporte_validacion_orden.txt` será obligatorio y bloqueante.

## Reglas para la siguiente sesión

1. Consultar siempre el ledger; no usar manifiestos históricos como cola viva.
2. Crear el lote siguiente con `ledger.py next-batch` y ejecutar su preflight antes del enriquecimiento.
3. Generar `indice_fuente.json` desde los tramos seleccionados antes de construir el borrador.
4. Mantener una sesión por documento o parcial, sin mezclar contextos.
5. Registrar Gemini CLI / Gemini 3.7 Flash en cada bitácora, sin inventar tokens o costos.
6. No promover mientras esquema, índice, citas y densidad no estén revisados; una alerta de densidad puede
   aceptarse solo con justificación humana explícita.
