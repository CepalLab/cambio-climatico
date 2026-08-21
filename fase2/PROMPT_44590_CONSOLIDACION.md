# 44590 — consolidación final en dos niveles

Trabaja en una sesión limpia desde `fase2`. Consolida únicamente `11362/44590`.

Entradas obligatorias:

- `corpus/intermedios/11362/44590/PREPARACION_FUENTE.md`
- `corpus/intermedios/11362/44590/tramos/`
- `corpus/intermedios/11362/44590/indice_fuente.json`
- `corpus/intermedios/11362/44590/mapa_cortes_44590.md`
- todos los `parcial_*.json` declarados en el mapa

Lee también `codebook_v0.md`, `esquema_json_v1.md`, `GUIA_OPERATIVA_PIPELINE.md`, `OPERACION_BATCH.md`, `DIRECTRIZ_CALIDAD_EXPLICATIVA_v1.md`, `INTERPELACION_v0.md`, `big_push.md`, `CASOS_ANCLA_INTERPELACION_v1.md` y `TIPOLOGIA_v0.md`.

Por el tamaño del documento, trabaja en dos niveles:

1. Verifica cada parcial contra su rango y agrúpalos por capítulos o macrosecciones del mapa.
2. Construye consolidaciones intermedias por grupo, sin perder títulos, páginas, dimensiones ni citas.
3. Fusiona las consolidaciones en el árbol final `resumen_secciones`, eliminando solapes reales y preservando el recorrido literal del índice.
4. Completa `documento`, `resumen_enriquecido`, `interpelacion` y `tipologia` con evidencia del documento completo. No confundas descripción de integración regional con recomendaciones climáticas propias.
5. En `como_hacerlo_concreto`, usa exclusivamente la voz normativa del cierre y desglosa los ítems sin inflar el tally.
6. Escribe atómicamente `borrador_preprueba.json`.
7. Ejecuta y guarda en UTF-8 los cuatro reportes finales:

```bash
python3 fase2/pipeline/validar_esquema.py fase2/corpus/intermedios/11362/44590/borrador_preprueba.json > fase2/corpus/intermedios/11362/44590/reporte_validacion_esquema.txt
python3 fase2/pipeline/validar_indice.py fase2/corpus/intermedios/11362/44590/borrador_preprueba.json --indice fase2/corpus/intermedios/11362/44590/indice_fuente.json > fase2/corpus/intermedios/11362/44590/reporte_validacion_indice.txt
python3 fase2/pipeline/validar_citas.py fase2/corpus/intermedios/11362/44590/borrador_preprueba.json --page-source fase2/corpus/intermedios/11362/44590/tramos --strict-quality > fase2/corpus/intermedios/11362/44590/reporte_validacion_citas.txt
python3 fase2/pipeline/auditar_densidad.py fase2/corpus/intermedios/11362/44590/borrador_preprueba.json > fase2/corpus/intermedios/11362/44590/reporte_auditoria_densidad.txt
python3 fase2/pipeline/validar_orden_json.py fase2/corpus/intermedios/11362/44590/borrador_preprueba.json > fase2/corpus/intermedios/11362/44590/reporte_validacion_orden.txt
```

Si se modifica el JSON después de validar, repite las cinco validaciones. El reporte de orden debe ser `OK`; no reordenes automáticamente desde el validador. Actualiza la bitácora local `EJECUCION_ENRIQUECIMIENTO.md` con modelo, fuente, parciales, consolidaciones y correcciones. No promociones ni edites el ledger.
