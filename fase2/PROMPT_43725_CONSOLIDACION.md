# 43725 - consolidacion y cierre final

Trabaja en una sesion limpia, desde `fase2`. Consolida solamente 11362/43725.

Entradas obligatorias:
- `corpus/intermedios/11362/43725/indice_fuente.json`
- `corpus/intermedios/11362/43725/mapa_cortes_43725.md`
- `corpus/intermedios/11362/43725/parcial_capitulos_i_iii.json`
- `corpus/intermedios/11362/43725/parcial_capitulos_iv_viii.json`
- `corpus/intermedios/11362/43725/tramos/`

Lee tambien `codebook_v0.md`, `esquema_json_v1.md`, `GUIA_OPERATIVA_PIPELINE.md`, `OPERACION_BATCH.md`, `DIRECTRIZ_CALIDAD_EXPLICATIVA_v1.md`, `INTERPELACION_v0.md`, `big_push.md`, `CASOS_ANCLA_INTERPELACION_v1.md` y `TIPOLOGIA_v0.md`.

No releas sistematicamente el PDF ni rehagas los parciales. Usa tramos solo para resolver solapes, dudas puntuales y validacion final. No descargues, no edites ledger ni escribas en `corpus/resultados`.

1. Fusiona ambos parciales en un solo arbol `resumen_secciones`, sin duplicados, con los diez titulos nivel 1 literales del manifiesto y sus subsecciones reales.
2. Completa `documento`, `resumen_enriquecido`, las cuatro interpelaciones y tipologia con evidencia de ambos parciales. No fuerces veredictos positivos. Para `como_hacerlo_concreto`, usa exclusivamente la voz normativa del cierre; no uses recuadros de recomendaciones intercalados.
3. Genera atomica y definitivamente `corpus/intermedios/11362/43725/borrador_preprueba.json`.
4. Cuando JSON y manifiesto sean definitivos, ejecuta una unica ronda final de esquema, indice, citas estrictas con `--page-source tramos` y densidad. Guarda los cuatro reportes UTF-8 dentro del directorio del documento.
5. Tras cuatro reportes limpios, no edites JSON ni manifiesto. Crea/actualiza `EJECUCION_ENRIQUECIMIENTO.md` local con harness, modelo, fuente, parciales y resultados.

Condicion de termino: esquema, indice y citas estrictas limpios. No promociones el documento.
