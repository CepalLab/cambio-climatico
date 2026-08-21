# 42140 ? indice y mapa de modulos

Trabaja en una sesion limpia, desde el directorio fase2. Procesa solamente 11362/42140.

Fuente unica: corpus/intermedios/11362/42140/tramos/ (534 paginas PDF, 22 tramos). No descargues, no regeneres la fuente, no uses OCR, no edites ledger ni resultados.

Objetivo: crear antes de toda extraccion el manifiesto literal corpus/intermedios/11362/42140/indice_fuente.json y el mapa de trabajo corpus/intermedios/11362/42140/mapa_modulos_42140.md.

1. Lee las paginas de indice del tramo tramo_001_025.txt y verifica los encabezados de modulo en el cuerpo.
2. La jerarquia obligatoria es:
   - nivel 1: Modulo 1. Biocombustibles; Modulo 2. Uso eficiente de la energia; Modulo 3. Energias renovables y desarrollo sostenible; Modulo IV. El sector energetico en el contexto del cambio climatico; Modulo V. Sostenibilidad energetica; Modulo VI. El sector energetico: caracterizacion, diagnostico y politica.
   - nivel 2: cada Articulo I.*, II.*, III.*, IV.*, V.* o VI.* literal que pertenezca al modulo.
   - niveles inferiores: los encabezados internos literales.
3. El manifiesto debe incluir solo los seis modulos como secciones nivel 1, en orden y con titulo literal. Excluye Presentacion, Premio, palabras inaugurales, resumen/abstract de cada articulo, bibliografias, anexos, cuadros, graficos, figuras y catalogos.
4. Registra en mapa_modulos_42140.md el rango PDF fisico y los articulos literales de cada modulo. El corte de los parciales es semantico: Modulos 1-3 frente a Modulos IV-VI. Confirma la pagina PDF real donde comienza Modulo IV.
5. Ejecuta validar_indice.py solo como comprobacion del manifiesto contra un esqueleto minimo si es necesario. No crees borrador_preprueba.json, parciales, tipologia ni interpelacion.

Termina informando las rutas creadas y el corte PDF confirmado.
