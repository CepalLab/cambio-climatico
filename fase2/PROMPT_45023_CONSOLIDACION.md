# 45023 — consolidación final

Trabaja en una sesión limpia desde `fase2`. Consolida únicamente `11362/45023`.

Entradas obligatorias:

- `corpus/intermedios/11362/45023/PREPARACION_FUENTE.md`
- `corpus/intermedios/11362/45023/tramos/`
- `corpus/intermedios/11362/45023/indice_fuente.json`
- `corpus/intermedios/11362/45023/mapa_cortes_45023.md`
- todos los `parcial_*.json` declarados en el mapa

Lee también `codebook_v0.md`, `esquema_json_v1.md`, `GUIA_OPERATIVA_PIPELINE.md`, `OPERACION_BATCH.md`, `DIRECTRIZ_CALIDAD_EXPLICATIVA_v1.md`, `INTERPELACION_v0.md`, `big_push.md`, `CASOS_ANCLA_INTERPELACION_v1.md` y `TIPOLOGIA_v0.md`.

1. Fusiona los parciales en un único `resumen_secciones`, sin duplicados, omisiones ni cambios de título. El recorrido debe coincidir exactamente con `secciones_jerarquicas_incluidas` del manifiesto.
2. Conserva la evidencia de cada bloque y deduplica únicamente hallazgos realmente repetidos. No conviertas cada indicador en una dimensión independiente.
3. Completa `documento`, `resumen_enriquecido`, `interpelacion` y `tipologia` con evidencia del documento completo. En `como_hacerlo_concreto`, usa solo la voz normativa propia del cierre.
4. Escribe atómicamente `borrador_preprueba.json`.
5. Ejecuta la ronda final completa y guarda en UTF-8:

```bash
python3 fase2/pipeline/validar_esquema.py fase2/corpus/intermedios/11362/45023/borrador_preprueba.json > fase2/corpus/intermedios/11362/45023/reporte_validacion_esquema.txt
python3 fase2/pipeline/validar_indice.py fase2/corpus/intermedios/11362/45023/borrador_preprueba.json --indice fase2/corpus/intermedios/11362/45023/indice_fuente.json > fase2/corpus/intermedios/11362/45023/reporte_validacion_indice.txt
python3 fase2/pipeline/validar_citas.py fase2/corpus/intermedios/11362/45023/borrador_preprueba.json --page-source fase2/corpus/intermedios/11362/45023/tramos --strict-quality > fase2/corpus/intermedios/11362/45023/reporte_validacion_citas.txt
python3 fase2/pipeline/auditar_densidad.py fase2/corpus/intermedios/11362/45023/borrador_preprueba.json > fase2/corpus/intermedios/11362/45023/reporte_auditoria_densidad.txt
python3 fase2/pipeline/validar_orden_json.py fase2/corpus/intermedios/11362/45023/borrador_preprueba.json > fase2/corpus/intermedios/11362/45023/reporte_validacion_orden.txt
```

Si se modifica el JSON después de validar, repite las cinco validaciones. El reporte de orden debe ser `OK`; no reordenes automáticamente desde el validador. Actualiza la bitácora local `EJECUCION_ENRIQUECIMIENTO.md` con fuente, parciales, modelo, correcciones y resultados. No promociones ni edites el ledger.
