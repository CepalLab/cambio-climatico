# 42140 ? consolidacion y cierre final

Trabaja en una sesion limpia, desde fase2. Consolida solamente 11362/42140.

Entradas obligatorias:
- corpus/intermedios/11362/42140/indice_fuente.json
- corpus/intermedios/11362/42140/mapa_modulos_42140.md
- corpus/intermedios/11362/42140/parcial_modulos_1_3.json
- corpus/intermedios/11362/42140/parcial_modulos_4_6.json
- corpus/intermedios/11362/42140/tramos/

Lee tambien codebook_v0.md, esquema_json_v1.md, GUIA_OPERATIVA_PIPELINE.md, OPERACION_BATCH.md, DIRECTRIZ_CALIDAD_EXPLICATIVA_v1.md, INTERPELACION_v0.md, big_push.md, CASOS_ANCLA_INTERPELACION_v1.md y TIPOLOGIA_v0.md.

No releas sistematicamente el PDF ni rehagas la extraccion de los parciales. Usa los tramos solo para resolver un solape, duplicado o duda puntual y para la validacion automatica final. No descargues, no edites ledger ni escribas en corpus/resultados.

1. Fusiona los dos parciales en un unico arbol resumen_secciones, sin duplicados, con los seis modulos literales como nivel 1 y los articulos como nivel 2.
2. Completa documento, resumen_enriquecido, interpelacion y tipologia con evidencia de ambos parciales. No fuerces un veredicto positivo: aplica las reglas acumulativas y cubre integramente la unidad normativa seleccionada para como_hacerlo_concreto.
3. Genera atomica y definitivamente:
   corpus/intermedios/11362/42140/borrador_preprueba.json
4. Cuando JSON y manifiesto esten definitivos, ejecuta una unica ronda final:
   python pipeline/validar_esquema.py corpus/intermedios/11362/42140/borrador_preprueba.json
   python pipeline/validar_indice.py corpus/intermedios/11362/42140/borrador_preprueba.json --indice corpus/intermedios/11362/42140/indice_fuente.json
   python pipeline/validar_citas.py corpus/intermedios/11362/42140/borrador_preprueba.json corpus/intermedios/11362/42140/texto.txt --page-source corpus/intermedios/11362/42140/tramos --strict-quality
   python pipeline/auditar_densidad.py corpus/intermedios/11362/42140/borrador_preprueba.json
5. Guarda las cuatro salidas UTF-8 como reporte_validacion_esquema.txt, reporte_validacion_indice.txt, reporte_validacion_citas.txt y reporte_auditoria_densidad.txt dentro de corpus/intermedios/11362/42140/.
6. Tras los cuatro reportes limpios, no edites JSON ni manifiesto. Crea corpus/intermedios/11362/42140/EJECUCION_ENRIQUECIMIENTO.md con harness, modelo, fuente, parciales consolidados y resultados.

Condicion de termino: esquema, indice y citas estrictas limpios; no promociones el documento.
