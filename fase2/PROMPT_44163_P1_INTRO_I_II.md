# 44163 ? parcial P1: Introducci?n, I y II

Trabaja ?nicamente en `fase2/corpus/intermedios/11362/44163/`. Lee `PREPARACION_FUENTE.md`, `indice_fuente.json`, `texto.txt` y `tramos/`.

Crea at?micamente `parcial_44163_p1.json`, una lista JSON con estas secciones y toda su descendencia literal del manifiesto, en el mismo orden:

- `Introducci?n`
- `I. Contexto econ?mico, producci?n y rendimientos hist?ricos, comercio y precios`
- `II. La producci?n de caf? en la Rep?blica Dominicana`, incluyendo como subsecci?n `I. Pol?ticas regionales y nacionales` y sus cinco pol?ticas numeradas.

Reglas:

- Conserva t?tulo, puntuaci?n, numeraci?n, nivel y orden exactamente como aparecen en `secciones_jerarquicas_incluidas`.
- Cada nodo debe tener las seis claves can?nicas: `seccion`, `nivel`, `paginas`, `resumen`, `dimensiones`, `subsecciones`.
- Resume cada hoja con contenido verificable de su rango; no uses texto de ?ndice, encabezados repetidos ni afirmaciones ajenas a la secci?n.
- Toda dimensi?n debe llevar cita literal autosuficiente y p?gina correcta. No inventes dimensiones.
- No incluyas abreviaturas, bibliograf?a, anexos, cuadros ni encabezados corridos.
- No modifiques `borrador_preprueba.json`, otros parciales, el manifiesto ni la carpeta de resultados.
