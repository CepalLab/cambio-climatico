# 43725 - indice y mapa de cortes

Trabaja en una sesion limpia, desde el directorio `fase2`. Procesa solamente 11362/43725.

Fuente unica: `corpus/intermedios/11362/43725/tramos/` (272 paginas PDF). No descargues, no regeneres la fuente, no uses OCR, no edites ledger ni resultados.

Objetivo: crear antes de toda extraccion el manifiesto literal `corpus/intermedios/11362/43725/indice_fuente.json` y el mapa `corpus/intermedios/11362/43725/mapa_cortes_43725.md`.

El indice automatico preliminar contiene ruido de maquetacion. Lee las paginas de indice y verifica el inicio de cada capitulo en el cuerpo. La jerarquia nivel 1 obligatoria es: Introduccion; I. Escenarios de referencia; II. Escenarios climaticos; III. Impactos potenciales en recursos hidricos e hidroelectricidad; IV. Impactos potenciales en agricultura: granos basicos y cafe, seguridad alimentaria y aseguramiento; V. Impactos potenciales en ecosistemas; VI. Impactos potenciales en enfermedades sensibles al clima; VII. Escenarios de emisiones de gases de efecto invernadero; VIII. Escenario de costos economicos; Conclusiones. Conserva la grafia y numeracion literal que confirme la fuente.

No asciendas a nivel 1 encabezados internos como `B. Precipitacion` o `I. Seguro indexado contra sequias`; ubicalos bajo su capitulo real. Excluye Prologo, Mensajes clave, Resumen, abreviaciones, bibliografia, anexos, cuadros, graficos, mapas, diagramas, recuadros y cabeceras repetidas.

En `mapa_cortes_43725.md` registra el rango PDF fisico, titulos literales y subsecciones de: (A) Introduccion + capitulos I-III, y (B) capitulos IV-VIII + Conclusiones. Confirma la pagina de inicio de IV y de Conclusiones.

No crees borrador_preprueba.json, parciales, tipologia ni interpelacion. Termina informando rutas y cortes confirmados.
